import requests

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'supakit.kr@ku.th'
}


def get_page(url):
    global headers
    text = ''
    try:
        r = requests.get(url, headers=headers, timeout=2)
        text = r.text
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print('Get Page Error!')
    return text.lower()


text = get_page('http://www.ku.ac.th/web2012/')
print(text)
