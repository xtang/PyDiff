#/bin/python

import urllib2
import urllib
import time
import sys
import simplejson

def main(args):
    if len(args) != 2:
        return
    fileName = args[0]
    url = args[1]
    if len(fileName) <= 0 or len(url) <=0:
        return
    data = ''
    results = []
    with open(fileName, 'r') as f:
        datas = f.readlines()
        prefix = ''
        if fileName == 'querys_utf8':
            prefix = 'fq=saver:3&fl=url,md5,title&hl=true&hl.fl=title,snippet&wt=json&start=0&rows=30&q='
        elif fileName == 'test-urls.txt':
            prefix = 'u='
        start = time.time()
        for data in datas:
            data = data.strip()
            data = urllib.quote(data)
            data = prefix + data
            clen = len(data)
            request =  urllib2.Request(url, data)
            retval = urllib2.urlopen(request)
            results.append(simplejson.loads(retval.read()))
        end = time.time()
        print 'cost: %fs request %d queries' % (end - start, len(datas))
    with open('json-result-fetcher.json', 'w') as f:
        for result in results:
            print >> f, simplejson.dumps(result);

if __name__ == '__main__':
    main(sys.argv[1:])
