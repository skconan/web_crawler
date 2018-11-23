'''
    File name: scheduler.py
    Author: skconan
    Date created: 2018/09/06
    Python Version: 3.6.1
'''

from downloader import Downloader
from analyzer import Analyzer
from recorder import Recoder
from lib import *
import constants as CONST
import codecs

class Scheduler:
    def __init__(self):
        self.dl = Downloader()
        self.alz = Analyzer()
        self.rec = Recoder()

        self.frontier_q = []
        self.visited_q = []

        print('Press\n1: Replace\n2: Continue')
        self.mode = int(input())
        self.select_mode()

    def select_mode(self):
        if self.mode == 1:
            self.frontier_q = [
                'https://www.livenation.co.uk/event/allevents'
            ]
            self.visited_q = []
            self.rec.count = 0
            self.rec.new_file()

        elif self.mode == 2:
            self.read_frontier_q()
            self.read_visited_q()
            self.rec.read_count()
        else:
            print('Please select 1 or 2')
            exit(0)

    def read_frontier_q(self):
        lines = reader(CONST.PATH_FRONTIER)
        for l in lines:
            self.frontier_q.append(l)

    def read_visited_q(self):
        lines = reader(CONST.PATH_VISITED)
        for l in lines:
            self.visited_q.append(l)

    def run(self):
        while len(self.frontier_q) > 0:
            current_url = self.frontier_q[0]
            self.frontier_q = self.frontier_q[1:]

            if current_url in self.visited_q and not self.alz.filter_link(current_url):
                print('cont')
                continue

            text = self.dl.get_page(current_url)[1]
            extracted_links = self.alz.link_parser(text)
            print('\n')
            print('Queue:', len(self.frontier_q))
            print('Current URL:', current_url)
            print('# of webpage:', self.rec.count)

            self.rec.record_html(current_url)
            
            self.visited_q.append(current_url)
            self.rec.record_visited(current_url)

            print('Extracted_links')
            for link in extracted_links:
                # print("Link:",link)
                link = self.alz.url_normalization(current_url, link)
                # print(link in self.frontier_q ,link in self.visited_q)
                if not link in self.frontier_q and not link in self.visited_q:
                    self.frontier_q.append(link)
                    self.rec.record_frontier(link)
            print("FRONTEIR")
            print(self.frontier_q)
      
        print('Finish')
    
   

if __name__ == '__main__':
    sc = Scheduler()
    sc.run()
