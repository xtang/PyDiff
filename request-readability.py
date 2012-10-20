#!/bin/python

import sys
import urllib2
import urllib
import simplejson

endpoint_prefix = 'https://readability.com/api/content/v1/parser?format=json&token=e74d3637befb99273e179331c177e797fdd75d4a&url='
total = 0
results = []
with open('selected-urls.txt') as f:
    for url in f.readlines():
        total += 1;
        url = url.strip();
        url_encoded = urllib.quote(url)
        endpoint = endpoint_prefix + url_encoded
        # request
        req = urllib2.Request(endpoint)
        opener = urllib2.build_opener()
        res = opener.open(req)
        result = simplejson.load(res)
        results.append(result)
        print "processed %dth link %s" % (total, url)

with open('json-result.json', 'w') as f:
    for result in results:
        print >> f, simplejson.dumps(result)
