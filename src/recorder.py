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
import json
import os


class Recoder():
    def __init__(self):
        self.count = 0
        self.analyzer = Analyzer()
        self.downloader = Downloader()

    def read_count(self):
        line = reader(CONST.PATH_COUNT)
        self.count = int(line[0])

    def counting(self):
        self.count += 1
        self.record_count(self.count)

    def get_subdirectory(self, url):

        url = url.lower()
        url = url.replace('//','/')
        url = url.replace('\n','')
        url = url.replace('?','/')
        url = url.replace('=','/')
        return url.split('/')[1:]

    def record_html(self, url):
        # https://www.livenation.co.uk/event/allevents?page=2
        # https://www.livenation.co.uk/show/1058621/the-australian-pink-floyd-show-time-30-years-of-celebrating-pink-floyd/guildford/2018-11-19/en
        filename = ""

        if url.find('allevents?') > 0:
            filename = 'allevents_page_'+ url.split('=')[1]  +'.html'
        elif url.find('allevents') > 0:
            filename = 'allevents_page_1.html'
            url = "https://www.livenation.co.uk/event/allevents?page=1"
        else:
            # filename = url.split('/')[5]+'.html'
            filename = 'detail.html'
            self.record_log_json(url)

        text = self.downloader.get_page(url)[1]
      
        current_path = CONST.PATH_HTML.replace('~','')
        
        hostname = self.analyzer.get_hostname(url)[1]
        print("host:",hostname)
        list_dir_expected = self.get_subdirectory(url)
        list_dir_expected = [hostname] + list_dir_expected
        
        list_dir_current = os.listdir(current_path)
        list_dir_expected = list_dir_expected[1:]
        print("list_dir_expected:",list_dir_expected)
        for dir_expected in list_dir_expected:
            current_path = endwith_backslash(current_path) + dir_expected
            if not dir_expected in list_dir_current:
                
                os.makedirs(current_path)
            print('current path',current_path)
            list_dir_current = os.listdir(current_path)
        
        path1 = ''
        for i in list_dir_expected:
            path1 += '\\' + i
        abs_path = CONST.PATH_HTML + path1
        # print
        print(filename)
        # print(abs_path.replace('\','))
        f = writer(abs_path+'\\'+filename, str(text))
        self.counting()

    def record_count(self, count):
        writer(CONST.PATH_COUNT, str(count))

    def record_robot(self, url):
        writer(CONST.PATH_ROBOT, str(url)+'\n', mode='append')

    def record_sitemap(self, url):
        writer(CONST.PATH_SITEMAP, str(url)+'\n', mode='append')

    def record_frontier(self, url):
        writer(CONST.PATH_FRONTIER, str(url)+'\n', mode='append')

    def record_visited(self, url):
        writer(CONST.PATH_VISITED, str(url)+'\n', mode='append')
    
    def record_log_json(self,url):
        # https://www.livenation.co.uk/show/1085415/stewart-francis-into-the-punset-/worthing/2018-11-20/en
        url_tmp = url
        url = url.split('/')
        data = {
            "url": url_tmp,
            "concert_name" : url[5],
            "city" : url[6],
            "date": url[7],
        }
        writer(CONST.PATH_LOG, json.dumps(data)+'\n', mode='append')

    def new_file(self):
        writer(CONST.PATH_ROBOT, str(''))
        writer(CONST.PATH_SITEMAP, str(''))
        writer(CONST.PATH_FRONTIER, str(''))
        writer(CONST.PATH_VISITED, str(''))
        writer(CONST.PATH_COUNT, str(''))
        writer(CONST.PATH_LOG, str(''))


if __name__ == '__main__':
    # r = Recoder()

    # # r.record_count(11)
    # # r.read_count()
    # r.record_html('https://offic.src.ku.ac.th/rub_tong.html')
    pass