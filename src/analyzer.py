'''
    File name: analyzer.py
    Author: skconan
    Date created: 2018/09/06
    Python Version: 3.6.1
'''

from urllib.parse import urljoin
from downloader import Downloader
from bs4 import BeautifulSoup
from lib import *
import urllib.request
import io


class Analyzer:
    def __init__(self):
        self.url_prefix = ['http://', 'https://']
        self.url_posfix = ['']

    def result(self, boolean=False, result=''):
        return [boolean, result]

    def filter_link(self, link):
        # https://www.livenation.co.uk/event/allevents?page=2
        # https://www.livenation.co.uk/show/1058621/the-australian-pink-floyd-show-time-30-years-of-celebrating-pink-floyd/guildford/2018-11-19/en       
        if (link.split('?')[0] == '/event/allevents') or (link.find('/show') > 0 and link.find('/en') > 0):
            return True
        return False

    def fix_link(self, link):
        remove_text = [':8000', ':8080']
        for txt in remove_text:
            link = link.replace(txt, '')
        return link

    def link_parser(self, raw_html):
        # print(raw_html)
        urls = []
        
        pattern_start = 'href="'
        pattern_end = '"'
        index = 0
        length = len(raw_html)
        raw_html = raw_html.replace('\t','')
        raw_html = raw_html.replace('\r','')
        raw_html = raw_html.replace('\n','')
       
        while index < length:
            start = raw_html.find(pattern_start, index)
            if start > 0:
                start = start + len(pattern_start)
                end = raw_html.find(pattern_end, start)
                link = raw_html[start:end]

                if len(link) > 0 and self.filter_link(link):
                        # link = self.fix_link(link)
                        urls.append(link)
                index = end
            else:
                break
        print("============== DEBUG URLS =============")
        print(urls)
        # exit(0)
        return urls

    def get_hostname(self, url):
        hostname = url.split('//')[1].split('/')[0]
        return [True, hostname]

    # def get_html(self, url):
    #     return True, url 

    def url_normalization(self, base_url, link):
        return urljoin(base_url, link)

   


if __name__ == '__main__':
    dl = Downloader()
    text = dl.get_page('https://www.livenation.co.uk/event/allevents')[1]
    print(text)
    al = Analyzer()
    urls = al.link_parser(text)
    print(urls)
   