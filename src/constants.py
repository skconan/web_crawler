'''
    File name: constants.py
    Author: skconan
    Date created: 2018/09/06
    Python Version: 3.6.1
'''
import os
import sys

PATH_PROJECT = os.path.dirname(os.path.abspath(__file__)).replace("src", "")[:-1]
PATH_HTML = PATH_PROJECT+r'\html'
PATH_TXT = PATH_PROJECT+r'\txt'
PATH_ROBOT = PATH_TXT+r'\list_robots.txt'
PATH_SITEMAP = PATH_TXT+r'\list_sitemap.txt'
PATH_FRONTIER = PATH_TXT+r'\list_frontier.txt'
PATH_VISITED = PATH_TXT+r'\list_visited.txt'
PATH_COUNT = PATH_TXT+r'\number_of_html.txt'
PATH_LOG = PATH_TXT+r'\log_webpage.txt'