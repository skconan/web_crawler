'''
    File name: lib.py
    Author: skconan
    Date created: 2018/09/07
    Python Version: 3.6.1
'''

import time
import codecs


def endwith_slash(text):
    return text + ('/' * (int(text.endswith('/')) ^ 1))


def endwith_backslash(text):
    return text + ('\\' * (int(text.endswith('\\')) ^ 1))


def slash2backslash(text):
    return text.replace('/', '\\')


def alert(msg='', delay_time=0, sound=False):
    print('!! ' + msg + ' !!')
    # time.sleep(delay_time)


def reader(file_path):
    f = codecs.open(file_path, 'r', 'utf-8')
    lines = f.readlines()
    f.close()
    return lines


def writer(file_path='', data='', mode='replace'):
    if file_path == '':
        return False
    if mode == 'replace':
        print(file_path)
        f = codecs.open(file_path, 'w+', 'utf-8')
    elif mode == 'append':
        f = codecs.open(file_path, 'a+', 'utf-8')
    f.write(data)
    f.close()
    return True
