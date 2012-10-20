import simplejson
from bs4 import BeautifulSoup
import time
import urllib
import re

readability_text = {}
fetcher_text = {}
'''
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
        # print readability_text[url]

with open('url-content-read.json', 'w') as f:
    print >> f, simplejson.dumps(readability_text)

with open('url-content-fetcher.json', 'w') as f:
    print >> f, simplejson.dumps(fetcher_text)

'''
with open('url-content-read.json') as f:
    readability_text = simplejson.load(f)

with open('url-content-fetcher.json') as f:
    fetcher_text = simplejson.load(f)


cnt = 0
for key, value in readability_text.items():
    if key in fetcher_text:
        rc = re.sub(r' ', '', value)
        read_text_len = int(len(rc) / 2);
        tmp_text = rc[read_text_len:(read_text_len+10)]
        fc = re.sub(r' ', '', fetcher_text[key])
        if read_text_len == 0:
            continue
        if tmp_text in fc:
            index_fc = fc.index(tmp_text)
            index_rc = read_text_len
            while (index_fc >= 0 and index_rc >= 0
                   and fc[index_fc] == rc[index_rc]):
                index_fc -= 1
                index_rc -= 1
            if index_fc == -1 and index_rc == -1:
                print 'head equal'
            elif index_fc == -1:
                if index_rc > 100:
                    print '---------------------'
                    print fc.encode('utf8')
                    print '****************************************'
                    print rc.encode('utf8')
                    print '---------------------'
                else:
                    print 'less head, ', rc[:index_rc].encode('utf8')
            elif index_rc == -1:
                print 'more head, ', fc[:index_fc].encode('utf8')
            '''
            print index
            print tmp_text.encode('utf8')
            print '==========================='
            print fc.encode('utf8')
            print '****************************************'
            print rc.encode('utf8')
            print '==========================='
            '''
print cnt
