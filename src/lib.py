'''
    File name: lib.py
    Author: skconan
    Date created: 2018/09/07
    Python Version: 3.6.1
'''

import time


def alert(msg='', delay_time=0, sound=False):
    for i in range(3):
        print('!! ' + msg + ' !!')
    time.sleep(delay_time)
