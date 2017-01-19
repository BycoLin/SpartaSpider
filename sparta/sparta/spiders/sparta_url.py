# -*- coding: utf-8 -*-
import sparta_api
from sparta.spiders.sparta_basic import SpartaBasic
from sparta.spiders.sparta_db import mysql
import sparta_define
import sys  
reload(sys)  
sys.setdefaultencoding("utf8") 

class SpartaSpider(SpartaBasic):
	name = "sparta_url"
	allowed_domains = ["http://mp.weixin.qq.com/"]
	start_urls = ["http://mp.weixin.qq.com/s?src=3&timestamp=1478659327&ver=1&signature=yEdplXSs70z7S1BLD34EGgV3l4IQqSlurmD1IqFi-MDSIb-6S2rxLgnv2Z0EOqq7aVVuM4JStk0lxkTnRxAI82inJKtHFB4yr7idRsCzucJEYzdwI-q9-EWEGfUVCaF0S39xe-8IE7C5kHTMKIZRWKiU-h6VE9SwYVXp5V-0VTE="]
	
	def start_requests(self):

		''' test
		for url in self.start_urls:
			true_url = url + sparta_define.TMP_URL_2_TRUE_URL_1 + "MjM5NTQ4NDY2MA==" + sparta_define.TMP_URL_2_TRUE_URL_2
			yield self.make_requests_from_url(true_url,url)
		'''
		
		get_nums = 5

		m = mysql(0,'tmp_article_info')
		row=m.table('tmp_article_info').field(['uin','content_url']).where({"if_spider":0}).find(get_nums) #读取

		if get_nums == 1:
			if not row:
				print("no data")
				return

			uin = row['uin']
			url = row['content_url']
			true_url = url + sparta_define.TMP_URL_2_TRUE_URL_1 + uin + sparta_define.TMP_URL_2_TRUE_URL_2
			yield self.make_requests_from_url(true_url,url)
		else:
			if not row:
				print("no data")
				return

			for sig_row in row:
				uin = sig_row['uin']
				url = sig_row['content_url']
				true_url = url + sparta_define.TMP_URL_2_TRUE_URL_1 + uin + sparta_define.TMP_URL_2_TRUE_URL_2
				yield self.make_requests_from_url(true_url,url)		

	def make_requests_from_url(self,url,content_url):
		return self.get_html_and_carry_item(url,"mp.weixin.qq.com","http://mp.weixin.qq.com/",content_url)

	def parse(self,respose):
		items = []
		cSapi = sparta_api.SpartaApi()
		content_url = respose.meta['item']
		cSapi.getSpartaArticleInfo(respose,items,content_url)

		return items