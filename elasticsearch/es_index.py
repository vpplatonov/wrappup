"""
    Create Elastic Search Index according to AWS Transcribe format
    {
      "jobName":"job ID",
      "accountId":"account ID",
      "results": {
         "transcripts":[
            {
               "transcript":" that's no answer",
               "confidence":1.0
            }
         ],
         "items":[
            {
               "start_time":"0.180",
               "end_time":"0.470",
               "alternatives":[
                  {
                     "confidence":0.84,
                     "content":"that's"
                  }
               ]
            },
         ]
      }
    }
"""

from __future__ import print_function
import json
from elasticsearch import Elasticsearch
import logging

WrappupStructure = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "items": {
            "dynamic": "true",
            "properties": {
                "start_time": {
                    "type": "float"
                },
                "end_time": {
                    "type": "float"
                },
                "alternatives": {
                    "type": "nested",
                    "properties": {
                        "confidence": {
                            "type": "float"
                        },
                        "content": {
                            "type": "text"
                        },
                    },
                }
            }
        },
    },
    # "mappings": {
    #     "transcripts": {
    #         "dynamic": "strict",
    #         "properties": {
    #             "transcript": {
    #                 "type": "text"
    #             }
    #         }
    #     },
    # },
    # "mappings": {
    #     "records": {
    #         "dynamic": "strict",
    #         "properties": {
    #             "jobName": {
    #                 "type": "text"
    #             },
    #             "accountId": {
    #                 "type": "text"
    #             },
    #             "status": {
    #                 "type": "text"
    #             },
    #         }
    #     }
    # }
}


# import json
# from time import sleep
# import requests
# from bs4 import BeautifulSoup
#
# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

File = './files/asrOutput.json'
DOC_TYPE = 'records'


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def aws_parse_json(transcribe_json):
    transcribe = json.loads(transcribe_json)
    return transcribe


def search(es_object, search_object, index_name='podcast'):
    """ Common search API """
    search_res = es_object.search(index=index_name, body=search_object)

    return search_res


def store_record_transcribe(elastic_object, record, doc_type='records', index_name='podcast'):
    try:
        outcome = elastic_object.index(index=index_name, doc_type=doc_type, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))


def read_transcript_from_file():
    _es = connect_elasticsearch()
    create_index_aws(_es)

    with open(File, 'rb') as fl:
        tscribe_json = json.load(fl)

    return tscribe_json['results']['transcripts'][0]['transcript']


def create_index_aws(es_object, index_name):
    created = False
    # index settings
    settings = WrappupStructure

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name,  body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def read_record_wrappup(elastic_object, search_str, index=0):
    search_object = [
    {"size": 100,
     "query": {
        "nested" : {
            "path": "alternatives",
            "query": {
              "bool": {
                "must": {
                    "match" : {"alternatives.content" : search_str}
                    }
                  }
                }
            }
    }}]
    ids = search(elastic_object, search_object[index], 'wrappup')

    return [source['_source'] for source in ids['hits']['hits']]


def find_best_interval(es_obj, search_str, interval=15):
    res = read_record_wrappup(es_obj, index=0, search_str=search_str)

    # # res = transcribeJSON['results']['transcripts'][0]['transcript']
    res_words = []
    r_words = {}
    max_nb = None
    for r in res:
        word = r['alternatives'][0]['content']
        for k in res:
            kword = k['alternatives'][0]['content']
            if word != kword and abs(float(r['start_time']) - float(k['start_time'])) < interval:
                if 'nb' in r:
                    r['nb'] = r['nb'] + 1
                else:
                    r['nb'] = 1

        res_words.append(r)
        if max_nb is None or ('nb' in r and max_nb['nb'] < r['nb']):
            max_nb = r

        word = r['alternatives'][0]['content']
        if word not in r_words:
            r_words[word] = 1
        else:
            r_words[word] = r_words[word] + 1
    max_nb['start_time'] = float(max_nb['start_time']) - interval
    max_nb['end_time'] = float(max_nb['end_time']) + interval

    return max_nb


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    es_obj = connect_elasticsearch()
    # create_index_aws(es_obj, index_name='podcast', settings=TranscribeStructure)
    create_index_aws(es_obj, index_name='wrappup')

    with open(File, 'rb') as f:
        transcribeJSON = json.load(f)

    # Save your job on ES index
    for item in transcribeJSON['results']['items']:
        store_record_transcribe(es_obj, item, index_name='wrappup', doc_type="items")

    # Topic example from analyze module
    search_str = ['network see idea might paper work net new effect abl', 'well effect confid way think build network idea comput vision']
    interval = 15  # 15 sec

    for sstr in search_str:
        max_nb = find_best_interval(es_obj, sstr, interval=15)

        print(max_nb)
