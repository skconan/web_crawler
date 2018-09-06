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
        self.url_posfix = ['ku.ac.th']

    def result(self, boolean=False, result=''):
        # print(boolean, result)
        
        return [boolean, result]

    def link_parser(self, raw_html):
        urls = []
        pattern_start = '<a href="'
        pattern_end = '"'
        index = 0
        length = len(raw_html)

        while index < length:
            start = raw_html.find(pattern_start, index)
            if start > 0:
                start = start + len(pattern_start)
                end = raw_html.find(pattern_end, start)
                link = raw_html[start:end]
                if len(link) > 0:
                    if link not in urls:
                        urls.append(link)
                index = end
            else:
                break
        return urls

    def get_hostname(self, url):
        hostname = ''
        for prefix in self.url_prefix:
            if prefix in url:
                for posfix in self.url_posfix:
                    if posfix in url:
                        hostname = url.split(prefix)[0]
                        print(hostname)
                        print(1)
                        # if hostname == 'ku.ac.th':
                        #     return self.result(True, hostname)
                        hostname = hostname.split(posfix)[0] + posfix
                        print(2)
                        print(hostname)
                        return self.result(True, hostname)
        return self.result()

    def get_html(self, url):
        for posfix in self.url_posfix:
            if posfix in url:
                html = url.split(posfix)[1]
                if '.html' in url:
                    html = html.split('.html')[0] + '.html'
                    return self.result(True, html)
                elif 'htm' in url:
                    html = html.split('.htm')[0] + '.htm'
                    return self.result(True, html)
        return self.result()

    def url_normalization(self, base_url, link):
        return urljoin(base_url, link)


    def get_robot(self, hostname):
        hostname = endwith_slash(hostname)
        try:
            req = urllib.request.urlopen(hostname + "robots.txt", data=None)
            data = io.TextIOWrapper(req, encoding='utf-8')
            return self.result(True, data.read())
        except:
            return self.result()

    def get_sitemap(self, hostname):
        hostname = endwith_slash(hostname)
        try:
            req = urllib.request.urlopen(hostname + "sitemap.xml", data=None)
            data = io.TextIOWrapper(req, encoding='utf-8')
            return self.result(True, data.read())
        except:
            return self.result()


if __name__ == '__main__':
    dl = Downloader()
    text = dl.get_page('http://www.ku.ac.th/web2012/')[1]
    print(text)
    al = Analyzer()
    urls = al.link_parser(text)
    # print(urls)
    for url in urls:
        # print('1=-----------')
        # print(url)
        res = al.get_html(url)
        # print('2=-----------')
        if(res[0]):
            print(res[1])
        # print('3=-----------')
    # print(len(urls))
    # print(al.get_robot('http://reddit.com')[0])
    # print(al.get_robot('http://google.co.th/')[0])
    # print(al.get_sitemap('http://reddit.com')[0])
    # print(al.get_sitemap('http://google.co.th/')[0])
