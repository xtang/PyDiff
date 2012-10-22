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

def dif_content(l_content, r_content):
    if len(l_content) == 0 or len(r_content) == 0:
        return 0
    l_len = len(l_content)
    r_len = len(r_content)
    
    if l_len > r_len:
        l_content, r_content = r_content, l_content
        l_len, r_len = r_len, l_len
    
    read_text_len = int(len(l_content) / 2);
    if read_text_len == 0:
        return 0
    tmp_len = 5
    tmp_text = ''
    while (read_text_len+tmp_len) < l_len:
        tmp_text = l_content[read_text_len:(read_text_len+tmp_len)]
        print tmp_text.encode('utf8')
        occ_count = r_content.count(tmp_text)
        if occ_count == 0:
            return 0
        if occ_count == 1:
            break
        tmp_len += 1
    if tmp_text == '': return 0
    r_index = r_content.index(tmp_text) - 1
    l_index = read_text_len - 1
    retval = len(tmp_text)
    while (l_index >= 0 and r_index >= 0
           and r_content[r_index] == l_content[l_index]):
        l_index -= 1
        r_index -= 1
        retval += 1

    if l_index != -1 and r_index != -1:
        retval += dif_content(l_content[:l_index], r_content[:r_index])

    r_index = r_content.index(tmp_text) + tmp_len
    l_index = read_text_len + tmp_len
    while (r_index < r_len and l_index < l_len
           and r_content[r_index] == l_content[l_index]):
        l_index += 1
        r_index += 1
        retval += 1

    if l_index != r_len and r_index != l_len:
        retval += dif_content(l_content[l_index:], r_content[r_index:])
    return retval

with open('url-content-read.json') as f:
    readability_text = simplejson.load(f)

with open('url-content-fetcher.json') as f:
    fetcher_text = simplejson.load(f)

cnt = 0
z_cnt = 0
for key, value in readability_text.items():
    if key in fetcher_text:
        cnt += 1
        rc = re.sub(r' ', '', value)
        fc = re.sub(r' ', '', fetcher_text[key])
        l_len = len(rc)
        r_len = len(fc)
        retval = dif_content(rc, fc)
        print cnt, ': ', l_len, r_len, retval
        if cnt == 5:
            print rc.encode('utf8')
            print '****************************************'
            print fc.encode('utf8')
        if retval == 0:
            z_cnt += 1
            print rc.encode('utf8')
            print '****************************************'
            print fc.encode('utf8')
            break

print cnt
print z_cnt

