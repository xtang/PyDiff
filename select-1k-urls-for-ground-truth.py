#!/bin/python

import sys
import tldextract
import time
import random

def foo():
    with open('./urls.txt') as f:
        urls = f.readlines();
    total = 0
    domain_counter = {}
    for url in urls:
        url = url.strip()
        if url.endswith(('.gif', '.jpg', '.tiff')): continue
        result = tldextract.extract(url)
        domain = '.'.join(result[:2])
        domain_counter[domain] = 1 + domain_counter.get(domain, 0)
        total += 1;

    print total
    domain_selected = {}
    url_selected = {}
    is_running = True
    iterater_num = 1
    while is_running:
        print '%dth iterater left %d url to select' % (iterater_num, 1000 - len(url_selected))
        iterater_num += 1
        for url in urls:
            url = url.strip()
            if url.endswith(('.gif', '.jpg', '.tiff')): continue
            if url_selected.has_key(url): continue
            result = tldextract.extract(url)
            domain = '.'.join(result[:2])
            domain_cnt = domain_counter.get(domain, 1)
            pro = 1.0 * domain_cnt / total
            rand = random.random()
            if rand < pro:
                url_selected[url] = 1
                if len(url_selected) >= 1000:
                    is_running = False
                    break
                decrement = domain_selected.get(domain, 0)
                if decrement == 0:
                    decrement = domain_cnt / 10
                    domain_selected[domain] = decrement
                domain_cnt -= decrement
                domain_counter[domain] = domain_cnt
                total -= decrement
    
    with open('./selected-urls.txt', 'w') as f:
        for key, value in url_selected.items():
            print >> f, key
    
def time_wrap():
    start = time.time();
    foo();
    print 'cost', time.time() - start, 's'

def main():
    time_wrap()

if __name__ == '__main__':
    main()
