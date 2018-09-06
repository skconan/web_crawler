'''
    File name: downloader.py
    Author: skconan
    Date created: 2018/09/06
    Python Version: 3.6.1
'''

import requests

class Downloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Bot by 5810500145 subject 01204453',
            'From': 'supakit.kr@ku.th'
        }

    def get_page(self,url):
        text = ''
        try:
            r = requests.get(url, headers=self.headers, timeout=2)
            text = r.text
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print('Get Page Error!')
        return text.lower()

if __name__ == '__main__':
    dl = Downloader()
    text = dl.get_page('http://www.ku.ac.th/web2012/')
    print(text)
