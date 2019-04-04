import os
import gzip
from elasticsearch import Elasticsearch
import sys
import json
import time
from operator import itemgetter


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
                self.doc_type: {
                    "dynamic": "strict",
                    "properites": {
                        "url": {
                            "type": "keyword",

                        },
                        "concert_name": {
                            "type": "text",


                        },
                        "city": {
                            "type": "text",

                        },
                        "html": {
                            "type": "text",
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

    # def search_by_date(self, start, end):
    #     "range": {
    #         "created": {
    #             "gte": start,
    #             "lte": end
    #         }
    #     }

    def search(self, key=[], value=[], start_date="2018-01-01", end_date="2020-01-01"):
        table_header = ['concert_name', 'city', 'date', 'url', 'score']
        table_data = []
        print(key)
        print(value)
        print(start_date)
        print(end_date)
        if len(key) == 0 or len(key) != len(value):
            search_object = {
                "query": {
                    "match_all": {
                        # key[0]: value[0]
                    }
                }
            }
        elif len(key) == 1:
            print("=========== 11 ==============")
            search_object = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    key[0]: value[0]
                                }
                            },
                            {"range": {"date": {"gte": start_date, "lte": end_date}}}
                        ],
                        # "filter": {
                        #     "range": {
                        #         "date": {
                        #             "gte": start_date,
                        #             "lte": end_date,
                        #             # "type": "date",
                        #             "format": "yyyy-mm-dd"
                        #         }
                        #     }
                        # }
                    }


                }
            }
        # elif
        else:
            # if ranking:
            print(key, value)
            print(start_date, end_date)
            search_object = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    key[0]: value[0]
                                }
                            },
                            {
                                "match": {
                                    key[1]: value[1]
                                }
                            },

                            {"range": {"date": {"gte": start_date, "lte": end_date}}}
                        ]
                    }


                }
            }
            # else:
            #     search_object = {
            #         "query": {
            #             "bool": {
            #                 "should": [
            #                     {
            #                         "match": {
            #                             key[0]: value[0]
            #                         }
            #                     },
            #                     {
            #                         "match": {
            #                             key[1]: value[1]
            #                         }
            #                     }
            #                 ]
            #             }
            #         }
            #     }
        res = self.es.search(index=self.index_name,
                             body=search_object, size=200)

        # {'_index': 'concert', '_type': 'webpage', '_id': 'AWc9g9YeADGmbvgB0CxZ',
        # '_score': 19.478054,
        # '_source': {'url': 'https://www.livenation.co.uk/show/1187472/only-girl/london/2018-11-20/en',
        # 'concert_name': 'only-girl', 'city': 'london', 'date': '2018-11-20'}}
        # print(res['hits']['total'])
        # print(res)
        # print("Len",len(res['hits']['hits']))
        if len(res['hits']['hits']) > 0:
            for dct in res['hits']['hits']:
                data = dct['_source']
                score = dct['_score']
                table_data.append(
                    [data['concert_name'], data['city'], data['date'], data['url'], score])
            # table_data_sorted = sorted(table_data,key=itemgetter(-1),reverse=True)
            # if ranking:
            #     for t in table_data_sorted:
            #         table_data_new.append(t[:])
            # else:
            #     for t in table_data:
            #         table_data_new.append(t[:])
        return table_header, table_data

        # print(res['hits']['hits'][0]['_source'])


if __name__ == '__main__':
    es = ElasticSearch()
    es.create_index()
    f = open(
        r"C:\Users\skconan\Desktop\web_crawler\consearch\search\log_webpage.txt", 'r')
    lines = f.readlines()
    ct = 0
    for line in lines:
        print(ct)
        # print(line)
        es.store_record(line)
        ct += 1
