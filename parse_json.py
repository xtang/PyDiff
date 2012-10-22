import simplejson
from bs4 import BeautifulSoup
import urllib
import re

def parse_json(read_filename, fetcher_filename):
    readability_text = {}
    fetcher_text = {}

    with open('json-result-fetcher.json') as f:
        jsons = f.readlines()
    cnt = 0
    for json in jsons:
        token = simplejson.loads(json)
        if token['errorCode'] is '0':
            cnt += 1
            data = token['payload'][0]
            if 'article' in data and 'url' in data:
                url = data['url']
                encode_utf8 = token['payload'][0]['article'].encode('utf8')
                soup = BeautifulSoup(encode_utf8)
                clean_text = re.sub(r'[\t\n\r]', '', soup.get_text().encode('utf8'))
                clean_text = re.sub(r' +', ' ', clean_text)
                fetcher_text[url] = clean_text.strip()

    with open('json-result.json') as f:
        jsons = f.readlines()
        cnt = 0
        for json in jsons:
            token = simplejson.loads(json)
            content = urllib.unquote(token['content'].encode('utf8'))
            soup = BeautifulSoup(content)
            url = token['url']
            clean_text = re.sub(r'[\t\n\r]', '', soup.get_text().encode('utf8'))
            clean_text = re.sub(r' +', ' ', clean_text)
            readability_text[url] = clean_text.strip()

    with open('url-content-read.json', 'w') as f:
        print >> f, simplejson.dumps(readability_text)

    with open('url-content-fetcher.json', 'w') as f:
        print >> f, simplejson.dumps(fetcher_text)
