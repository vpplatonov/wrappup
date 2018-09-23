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


def read_record(elastic_object, index=0, search_str="Hello"):
    search_object = [
    {"query": {
        "match": {"accountId": "888736911809"}
      }
    },
    {"query": {
        "nested" : {
            "path": "results",
            "query": {
                "nested" : {
                    "path": "results.transcripts",
                    "query": {
                      "bool": {
                        "must": {
                            "match" : {"results.transcripts.transcript" : search_str}
                        }
                      }
                    }
                }
            }
        }
    }},
    {"query": {
        "nested" : {
            "path": "results",
            "query": {
                "nested" : {
                    "path": "results.items",
                    "query":{
                        "nested" : {
                            "path": "results.items.alternatives",
                            "filter": {
                              "bool": {
                                "must": {
                                    "match" : {"results.items.alternatives.content" : search_str}
                                }
                              }
                            }
                        }
                    }

                }
            }
        }
    }}
    ]
    ids = search(elastic_object, search_object[index])
    # ids = search(elastic_object, json.dumps(search_object))

    # return ids['hits']['hits'][0]['_source']['results']['transcripts'][0]['transcript']
    return ids['hits']['hits'][0]['_source']['results']['items']


def store_record(elastic_object, record, index_name='podcast'):
    try:
        outcome = elastic_object.index(index=index_name, doc_type='records', body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))


def read_transcript_from_file():
    _es = connect_elasticsearch()
    create_index_aws(_es)

    with open(File, 'rb') as fl:
        tscribe_json = json.load(fl)

    return tscribe_json['results']['transcripts'][0]['transcript']


def create_index_aws(es_object, index_name='podcast'):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "records": {
                "dynamic": "strict",
                "properties": {
                    "jobName": {
                        "type": "text"
                    },
                    "accountId": {
                        "type": "text"
                    },
                    "results": {
                        "type": "nested",
                        "properties": {
                            "transcripts": {
                                "type": "nested",
                                "properties": {
                                    "transcript": {
                                        "type": "text"
                                    }
                                }
                            },
                            "items": {
                                "type": "nested",
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
                        }
                    },
                    "status": {
                        "type": "text"
                    },
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    es_obj = connect_elasticsearch()
    # create_index_aws(es_obj)
    #
    # with open(File, 'rb') as f:
    #     transcribeJSON = json.load(f)
    #
    # # Save your job on ES index
    # store_record(es_obj, transcribeJSON)

    search_str = "Hello"

    res = read_record(es_obj, 2, search_str)
    # res = transcribeJSON['results']['transcripts'][0]['transcript']
    print(res)
