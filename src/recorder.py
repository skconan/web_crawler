'''
    File name: recorder.py
    Author: skconan
    Date created: 2018/09/07
    Python Version: 3.6.1
'''

import constants as CONST
from downloader import Downloader
from analyzer import Analyzer
from lib import *
import os
import codecs

class Recoder():
    def __init__(self):
        self.count = self.get_count()
        self.analyzer = Analyzer()
        self.downloader = Downloader()

    def get_count(self):
        f = codecs.open(CONST.PATH_COUNT, 'r', 'utf-8')
        line = f.readlines()
        return int(line[0])

    def counting(self):
        self.count += 1

        if not self.count % 10:
            self.record_count(self.count)

    def writer(self, file_path='', data='', mode='replace'):
        if file_path == '':
            return False
        if mode == 'replace':
            f = codecs.open(file_path, 'w+', 'utf-8')
        elif mode == 'append':
            f = codecs.open(file_path, 'a+', 'utf-8')

        f.write(data)
        f.close()
        return True

    def record_count(self, count):
        if not self.writer(CONST.PATH_COUNT, str(count)):
            alert('Cannot record # of html '+str(count))

    def get_subdirectory(self, url):
        return url.split('/')[1:-1]
         

    def record_html(self, url):
        text = self.downloader.get_page(url)[1]
        hostname = self.analyzer.get_hostname(url)[1]
        html = self.analyzer.get_html(url)
        if not html[0]:
            alert('Analyzer::get_html Error')
        else:
            html = html[1]
            print(html)
            current_path = CONST.PATH_HTML
            list_dir_expected = self.get_subdirectory(html)
            list_dir_expected = [hostname] + list_dir_expected

            list_dir_current = os.listdir(current_path)
            print(list_dir_expected)
            for dir_expected in list_dir_expected:
                current_path = endwith_backslash(current_path) + dir_expected
                if not dir_expected in list_dir_current:
                    print('-',dir_expected,'=',list_dir_current)
                    os.makedirs(current_path)
                list_dir_current = os.listdir(current_path)
            abs_path = endwith_backslash(CONST.PATH_HTML) + slash2backslash(hostname + html)
            f = self.writer(abs_path,str(text))
            self.counting()
    
    def record_robot(self, url):
        self.writer(CONST.PATH_ROBOT, str(url), mode='append')

    def record_sitemap(self, url):
        self.writer(CONST.PATH_SITEMAP, str(url), mode='append')

if __name__ == '__main__':
    r = Recoder()

    # r.record_count(11)
    # r.get_count()
    r.record_html('https://offic.src.ku.ac.th/rub_tong.html')