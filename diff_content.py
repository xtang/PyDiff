# -*- coding: utf-8 -*-
#!/bin/python

__author__ = 'xtang@avos.com'

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
    tmp_len = 2
    tmp_text = ''
    while (read_text_len+tmp_len) < l_len:
        tmp_text = l_content[read_text_len:(read_text_len+tmp_len)]
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
