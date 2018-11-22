import os
import gzip
import constants as CONST
from elasticsearch import Elasticsearch
import sys
import json
import time

es = None


def connect_elasticsearch():
    global es
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
        print('Connected')
    else:
        print('Not connect!')
    return es


def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "webpage": {
                "dynamic": "strict",
                "properites": {
                    "url": {
                        "type": "keyword"
                    },
                    "concert_name": {
                        "type": "text",
                        "analyzer": "Thai"
                    },
                    "city": {
                        "type": "text",
                        "analyzer": "Thai"
                    },
                    "date": {
                        "type": "date",
                        "format": "yyyy-mm-dd"
                    },
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(
                index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(
            index=index_name, doc_type='webpage', body=record)
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))


def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    print(res)


connect_elasticsearch()
create_index(es, 'concert')

# data = {"url": "https://www.livenation.co.uk/show/1103135/paul-foot-image-conscious/colchester/2019-05-16/en\n",
#         "concert_name": "paul-foot-image-conscious", "city": "colchester", "date": "2019-05-16"}
data ={"url": "https://www.livenation.co.uk/show/1072892/the-mersey-beatles-get-back-the-2018-uk-tour/lydney/2018-11-21/en\n", "concert_name": "the-mersey-beatles-get-back-the-2018-uk-tour", "city": "lydney", "date": "2018-11-21"}
 
store_record(es, "concert", data)
# search_object = {"explain": True, 'query': {
#     'match': {'concert_name': 'paul-foot-image-conscious'}}}
# print()
# search_object = {"explain": True, 'query': {'multi_match': {
#     "query": 'paul-foot-image-conscious colchester', "fields": ['concert_name', 'city']}}}
print()
search_object = {
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "concert_name": "paul-foot-image-conscious"
                    }
                },
                {
                    "match": {
                        
                            "city": "colchester"
                        
                    }
                }
            ]
        }
    }
}
search(es, 'concert', json.dumps(search_object))
