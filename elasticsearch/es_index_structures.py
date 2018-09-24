"""
    Some constant
"""

TranscribeStructure = {
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
        "transcripts": {
            "dynamic": "strict",
            "properties": {
                "transcript": {
                    "type": "text"
                }
            }
        },
        "records": {
            "dynamic": "strict",
            "properties": {
                "jobName": {
                    "type": "text"
                },
                "accountId": {
                    "type": "text"
                },
                "status": {
                    "type": "text"
                },
            }
        }
    }
}


def read_record_wrappup(elastic_object, search_str, index=0):
    search_object = [{"query": {
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
    ids = search(elastic_object, search_object[index])

    return [source['_source'] for source in ids['hits']['hits']]


def search(es_object, search_object, index_name='podcast'):
    """ Common search API """
    search_res = es_object.search(index=index_name, body=search_object)

    return search_res


def read_record_transcribe(elastic_object, index=0, search_str="Hello"):
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
                            "query": {
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
