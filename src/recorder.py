'''
    File name: recorder.py
    Author: skconan
    Date created: 2018/09/07
    Python Version: 3.6.1
'''

import constants as CONST
from lib import *


class Recoder():
    def __init__(self):
        self.count = 0

    def counting():
        if not self.count % 10:
            self.record_count(self.count)

    def writer(self, file_path='', data='', mode='replace'):
        if file_path == '':
            return False
        if mode == 'replace':
            f = open(file_path, 'w+')
        elif mode == 'append':
            f = open(file_path, 'a+')
        f.write(data)
        f.close()
        return True

    def record_count(self, count):
        if not self.writer(CONST.PATH_COUNT, str(count)):
            alert('Cannot record # of html '+str(count),5)

    # def record_html(self, url):

if __name__ == '__main__':
    r = Recoder()
    r.record_count(11)