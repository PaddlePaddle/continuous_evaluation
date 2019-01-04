#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
"""
File: wiki_api.py
Author: guochaorong(guochaorong@baidu.com)
Date: 2018/08/19 13:45:30
"""
import numpy as np

import urllib
import urllib2
import re
from bs4 import BeautifulSoup
from datetime import datetime

import sys
reload(sys)
#for UnicodeEncodeError  
sys.setdefaultencoding("utf8")


def SaveFile(content, filename):
    f = open("wikiData/" + filename, "a")
    f.write(str(content) + "\n")
    f.close()


def SpideWiki():
    """spide daily report for this week"""
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    record_info = ''
    mm_str = datetime.now().strftime("%Y-%m")
    try:
        url = "https://github.com/PaddlePaddle/continuous_evaluation/wiki/%s" % mm_str
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        wikiHtml = response.read()
        soup = BeautifulSoup(
            str(wikiHtml), 'html.parser', from_encoding='utf-8')
        div = soup.find(name='div', id='wiki-body')
        ps = div.find_all(
            name='p', limit=100, recursive=True)  #only direct children  
        for p in ps:
            pText = p.get_text()
            record_info += (pText.encode('utf-8').strip())
        import re
        result = re.split("值班人：", record_info)
        infos = ''
        for x in result[1:6]:
            print x
            infos += x + '<br><br>'
        return infos
    except urllib2.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


records = SpideWiki()
with open("wiki.txt", 'w') as f:
    f.write(records)
