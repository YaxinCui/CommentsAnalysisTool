from base_class.comment_analysis import CommentAnalyse
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from math import ceil
import requests
import re
import time

"""
评论分析基本流程
1. 获取评论，并将其存入csv
2. 对评论进行分析，目前包括是否为建议，是消极还是积极，提取关键词信息
3. 可视化展示，存入文件
"""

class AmazonComment(CommentAnalyse):

    def __init__(self, url, columns=['comment', 'is_suggestion', 'sentiment']):
        """
        :param length: comments表格长度
        :param columns: comments类型为文本，表示评论文本，is_suggestion为是否为评论，类型为数字0.0-1.0，sentiment为是积极还是消极，类型为数字0.0-1.0
        """
        comment_list = self.get_comments(url)
        super().__init__(comment_list, columns)
        print('初始化后各列的类型', self.comments)

    def exact_info(self, info):  # 提取单个评论信息
        #print('抽取的html', info)
        comment = re.findall(r'<div class="a-row a-spacing-small review-data">([\s\S]*?)</div><div class=', info)
        #print('抽取的评论模块', comment)
        comment = re.findall(r'<span class="">([\s\S]*?)</span>', comment[0])
        #print('抽取的评论文字', comment)
        return comment[0]

    def exact_vector(self, entity_id, page_Number, page_size=20):
        # 提取一次请求的信息
        ajax_url = 'https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref'
        headers = {
            'accept': 'text/html,*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.18 Safari/537.36 Edg/75.0.139.4',
            'x-requested-with': 'XMLHttpRequest',

            'cookie': 'session-id=143-3613170-9632013; session-id-time=2082787201l; sp-cdn="L5Z9:CN"; ubid-main=130-9668493-3956104; x-wl-uid=14qOfaRoNNRz67CJH6Daz+wrAcQMHU/eEu70af+HkSNU6j6aqjdiwC4p26JiCqHqehnyE3FU3nNA=; lc-main=en_US; i18n-prefs=USD; session-token=4lSSdRWDhP99v0ihAoLS2bZLa0Vh8cThGMUzuerC2TAbWORMr1Vhegm0bFm27bX2eivf9se4jc0AqxaXpvnk3NHxCDIwwtuzoTyXQYDN/7LW5ewRarzi+auCM+fvJEZGMRJdhNxJqefnoaAh0eRgdJgk2ZPufvGUVJQ1z5/4Y8aicYcCdXmzZ18KZYMJnebo; csm-hit=tb:043ME4QKEVJVC2EJSG17+s-043ME4QKEVJVC2EJSG17|1556990812911&t:1556990812911&adb:adblk_no',
            'origin': 'https://www.amazon.com',
            'referer': 'https://www.amazon.com/Kindle-Oasis-reader-High-Resolution-International/product-reviews/B06XDFJJRS/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'


        }
        data = {
            'pageNumber': str(page_Number),
            'pageSize': str(page_size),
            'asin': entity_id
        }
        r = requests.post(ajax_url, headers=headers, data=data)
        # print(r.text) # 打印请求
        response = r.text.split('&&&')
        this_page = None
        all_page = None
        comments = []
        for info in response:
            if '["append","#cm_cr-review_list","<div id=' in info:
                #print('获得评论信息')
                info = info.replace('["append","#cm_cr-review_list","', '').replace(']', '').replace('\\n', '').replace('\\', '')
                comments.append(self.exact_info(info))
            elif 'cr-filter-info-review-count' in info:
                # print('获得页码信息')
                this_page = round(int(re.findall(r'-([\d]*?) ', info)[0]) / page_size)
                all_page = ceil(int(re.findall(r'of ([\d]*?) review', info)[0]) / page_size)
        # print(comments)
        return comments, this_page, all_page


    def get_comments(self, url):
        """为comments表添加评论，其中列名为comments
        :return:
        """
        id = re.findall(r'dp/([\s\S]*?)/ref=', url)[0]  # 通过链接获取商品ID
        # print('获得商品id为', id)
        this_page = 0
        comment_list = []
        while True:
            comments, this_page, all_page = self.exact_vector(entity_id=id, page_Number=this_page+1)
            comment_list.extend(comments)

            time.sleep(0.1)
            #print(comments)
            #print('this_page', this_page)
            #print('all_page', all_page)
            if this_page is None or all_page is None:
                print('爬取过程遇到反爬系统，部分页面未爬取')
                break
            elif this_page >= all_page:
                break
        return comment_list

    def analyse_comments(self):
        pass
