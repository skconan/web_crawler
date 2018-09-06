'''
    File name: analyzer.py
    Author: skconan
    Date created: 2018/09/06
    Python Version: 3.6.1
'''

from urllib.parse import urljoin
from downloader import Downloader
from bs4 import BeautifulSoup
import urllib.request
import io


class Analyzer:
    def __init__(self):
        pass

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

    def url_normalization(self, base_url, link):
        return urljoin(base_url, link)

    def endwith_slash(self, url):
        return url + ('/' * (int(url.endswith('/')) ^ 1))

    def get_robot(self, hostname):
        hostname = self.endwith_slash(hostname)
        print(hostname)
        try:
            req = urllib.request.urlopen(hostname + "robots.txt", data=None)
            data = io.TextIOWrapper(req, encoding='utf-8')
            return [True, data.read()]
        except:
            return [False, '']

    def get_sitemap(self, hostname):
        hostname = self.endwith_slash(hostname)
        try:
            req = urllib.request.urlopen(hostname + "sitemap.xml", data=None)
            data = io.TextIOWrapper(req, encoding='utf-8')
            return [True, data.read()]
        except:
            return [False, '']


if __name__ == '__main__':
    dl = Downloader()
    text = dl.get_page('http://www.ku.ac.th/web2012/')
    print(text)
    al = Analyzer()
    urls = al.link_parser(text)
    print(urls)
    print(len(urls))
    print(al.get_robot('http://reddit.com')[0])
    print(al.get_robot('http://google.co.th/')[0])
    print(al.get_sitemap('http://reddit.com')[0])
    print(al.get_sitemap('http://google.co.th/')[0])
