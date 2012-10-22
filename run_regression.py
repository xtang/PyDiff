#!/bin/python
import argparse
import simplejson
from diff_match_patch import diff_match_patch
from diff_content import dif_content
from parse_json import parse_json
import re

#__author__ == 'xtang@avos.com'

def set_parser():
    parser = argparse.ArgumentParser(description='fetcher regression.')
    parser.add_argument('--file', '-f', nargs=2, type=str, help='parse json result from readability and fetcher, args should be file name')
    parser.add_argument('--run', '-r', action='store_true', help='run directly')
    return parser

def run_compare():
    with open('url-content-read.json') as f:
        readability_text = simplejson.load(f)

    with open('url-content-fetcher.json') as f:
        fetcher_text = simplejson.load(f)

    cnt = 0
    z_cnt = 0
    dmp = diff_match_patch()
    rets = []
    for key, value in readability_text.items():
        if key in fetcher_text:
            cnt += 1
            rc = re.sub(r' ', '', value)
            fc = re.sub(r' ', '', fetcher_text[key])
            l_len = len(rc)
            r_len = len(fc)
            retval = dif_content(rc, fc)
            retval_ground = 0
            results = dmp.diff_main(rc, fc)
            for res in results:
                if res[0] == 0:
                    retval_ground += len(res[1])
            print cnt, ': ', l_len, r_len, retval, retval_ground
            real_ret = max(retval, retval_ground)
            rets.append((cnt, l_len, r_len, real_ret))

    with open('diff_result_1', 'w') as f:
        for res in rets:
            print >> f, res[0], ': ', res[1], res[2], res[3]

if __name__ == '__main__':
    parser = set_parser()
    ops = parser.parse_args()
    if not ops.run:
        read_json_filename = ops.file[0]
        fetcher_json_filename = ops.file[1]
        print read_json_filename, fetcher_json_filename
        parse_json(read_json_filename, fetcher_json_filename)
    run_compare()

    

