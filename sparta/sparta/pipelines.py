# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
from sparta.spiders.sparta_db import mysql
from sparta.items import *
#import sparta.sparta.sparta_define

'''
index_tag -> hot_article
		  -> author_url  -> gzh
		  				 -> article_url -> article
'''

class SpartaPipeline(object):
	def process_item(self, item, spider):
		if spider.name == 'sparta_index':
			if item:
				item_article = SpartaTagArticleInfoItem()
				item_gzh = SpartaTagGzhInfoItem()

				item_article['wechat_name'] = item['wechat_name']
				item_article['content_url'] = item['content_url']
				item_article['content_img_url'] = item['content_img_url']
				item_article['title'] = item['title']
				item_article['content'] = item['content']
				item_article['if_spider'] = 0

				item_gzh['wechat_name'] = item['wechat_name']
				item_gzh['author_link'] = item['author_link']
				item_gzh['author_img_url'] = item['author_img_url']
				item_gzh['qrcode_img_url'] = item['qrcode_img_url']
				item_gzh['category'] = item['category']
				item_gzh['if_spider'] = 0

				self.m.table('index_article_info').add(item_article) # 插入
				self.m.table('index_gzh_info').add(item_gzh) # 插入
		elif spider.name == 'sparta_url':
			if item:
				true_content_link = item['true_content_link']
				content_url = item['content_url']

				if true_content_link != "":
					self.m.table('article').add(item) # 插入

				self.m.table('tmp_article_info').where({"content_url":content_url}).save({"if_spider":1}) # 更新
		elif spider.name == 'sparta_gzh_url':
			if item:
				uin = item['uin']

				if uin == "":
					return item

				ret = item['ret']

				if ret == "link_over_time":
					spider_ret = 2
				elif ret == "link_ping_error":
					return item
				else:
					spider_ret = 1

				author_link = item['author_link']

				self.m.table('index_gzh_info').where({"author_link":author_link}).save({"if_spider":spider_ret}) # 更新

				if ret == "link_ping_succ":

					item_gzh = SpartaGzhItem()

					item_gzh['uin'] = uin
					item_gzh['wechat_id'] = item['wechat_id']
					item_gzh['wechat_name'] = item['wechat_name']
					item_gzh['introduce'] = item['introduce']
					item_gzh['renzhen'] = item['renzhen']
					item_gzh['account_subject'] = item['account_subject'] 
					item_gzh['qrcode_img_url'] = item['qrcode_img_url']
					item_gzh['author_img_url'] = item['author_img_url']
					item_gzh['category'] = item['category']
					item_gzh['author_link'] = item['author_link']

					self.m.table('gzh').add(item_gzh) # 插入

					item_article = SpartaTmpArticleInfoItem()

					for i in range(len(item['content_url'])):

						item_article['uin'] = uin
						item_article['content_url'] = item['content_url'][i]
						item_article['wechat_name'] = item['wechat_name']
						item_article['content_img_url'] = item['content_img_url'][i]
						item_article['title'] = item['title'][i]
						item_article['content'] = item['content'][i]
						item_article['if_spider'] = 0

						self.m.table('tmp_article_info').add(item_article) # 插入
		elif spider.name == 'sparta_search':
			if item:
				wechat_id = item['wechat_id']

				self.m.table('gzh').where({"wechat_id":wechat_id}).save({"update_time":"null"}) # 更新update_time

				item_gzh = SpartaTagGzhInfoItem()

				item_gzh['wechat_name'] = item['wechat_name']
				item_gzh['author_link'] = item['author_link']
				item_gzh['author_img_url'] = item['author_img_url']
				item_gzh['qrcode_img_url'] = item['qrcode_img_url']
				item_gzh['category'] = item['category']
				item_gzh['if_spider'] = 3 #需要更新

				self.m.table('index_gzh_info').add(item_gzh) # 插入
		else:
			return item

		return item

	def __init__(self):
		self.m = mysql(0,'index')
		
	def spider_closed(self,spider):
		pass
