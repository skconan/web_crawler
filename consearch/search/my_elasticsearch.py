import os
import gzip
from elasticsearch import Elasticsearch
import sys
import json
import time


class ElasticSearch():
    def __init__(self):
        self.es = None
        self.connect_elasticsearch()
        self.index_name = "concert"
        self.doc_type = "webpage"

    def connect_elasticsearch(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if self.es.ping():
            print('Connected')
        else:
            print('Not connect!')

    def create_index(self):
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
                        },
                        "city": {
                            "type": "text",
                        },
                        # "html": {
                        #     "type": "text",
                        # },
                        "date": {
                            "type": "date",
                            "format": "yyyy-mm-dd"
                        },
                    }
                }
            }
        }
        try:
            if not self.es.indices.exists(self.index_name):
                self.es.indices.create(
                    index=self.index_name, ignore=400, body=settings)
                print('Created Index')
        except Exception as ex:
            print(str(ex))

    def store_record(self, record):
        try:
            outcome = self.es.index(
                index=self.index_name, doc_type=self.doc_type, body=record)
            print(outcome)
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))

    def search(self, concert_name="", city=""):
        search_object = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "concert_name": str(concert_name)
                            }
                        },
                        {
                            "match": {
                                "city": str(city)
                            }
                        }
                    ]
                }
            }
        }
        res = self.es.search(index=self.index_name, body=search_object)
        table_header = ['concert_name','city','date','url'] 
        table_data = []
        # {'_index': 'concert', '_type': 'webpage', '_id': 'AWc9g9YeADGmbvgB0CxZ', 
        # '_score': 19.478054, 
        # '_source': {'url': 'https://www.livenation.co.uk/show/1187472/only-girl/london/2018-11-20/en', 
        # 'concert_name': 'only-girl', 'city': 'london', 'date': '2018-11-20'}}
        if len(res['hits']['hits']) > 0:
            for dct in res['hits']['hits']:
                data = dct['_source']
                table_data.append([data['concert_name'],data['city'],data['date'],data['url']])
        return table_header, table_data

        # print(res['hits']['hits'][0]['_source'])


if __name__ == '__main__':
    es = ElasticSearch()
    es.create_index()
    f = open(
        r"C:\Users\skconan\Desktop\web_crawler\consearch\search\log_webpage.txt", 'r')
    lines = f.readlines()
    for line in lines:
        print(line)
        es.store_record(line)

    # search(es, 'concert', json.dumps(search_object))
