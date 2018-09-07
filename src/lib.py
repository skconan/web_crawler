'''
    File name: lib.py
    Author: skconan
    Date created: 2018/09/07
    Python Version: 3.6.1
'''

import time


def endwith_slash(text):
    return text + ('/' * (int(text.endswith('/')) ^ 1))

def endwith_backslash(text):
    return text + ('\\' * (int(text.endswith('\\')) ^ 1))

def slash2backslash(text):
    return text.replace('/','\\')
    
def alert(msg='', delay_time=0, sound=False):
    for i in range(3):
        print('!! ' + msg + ' !!')
    time.sleep(delay_time)
