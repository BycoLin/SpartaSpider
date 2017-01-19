# -*- coding: utf-8 -*-
import sparta_api
from sparta.spiders.sparta_basic import SpartaBasic
from sparta.spiders.sparta_db import mysql
import sys  
reload(sys)  
sys.setdefaultencoding("utf8") 

class SpartaSpider(SpartaBasic):
	name = "sparta_gzh_url"
	allowed_domains = ["http://mp.weixin.qq.com/"]
	start_urls = ["http://mp.weixin.qq.com/profile?src=3&timestamp=1478245988&ver=1&signature=aS-ypIlb8aVQzyKGhwpMmbYF5iiz5ND0Y4xQIlRvjZx4xfzNpcWY5IbGSwI4B5qhmYZwiOvV9zdTmv0bHn8amQ=="]
	
	#scrapy crawl sparta_gzh_url -a spiderType=3 更新公众号信息
	#scrapy crawl sparta_gzh_url -a spiderType=0 或 scrapy crawl sparta_gzh_url 热门公众号信息拉取
	def __init__(self, spiderType=0, *args, **kwargs):
		super(SpartaSpider, self).__init__(*args, **kwargs)
		self.spiderType = spiderType

	def start_requests(self):

		''' 测试
		for url in self.start_urls:
			yield self.make_requests_from_url(url,1)
		'''

		get_nums = 1
		
		m = mysql(0,'index_gzh_info')
		row=m.table('index_gzh_info').field(['author_link','category']).where({"if_spider":self.spiderType}).find(get_nums) #读取

		if get_nums == 1:

			if not row:
				print("no data")
				return

			url = row['author_link']
			category = row['category']
			yield self.make_requests_from_url(url,category)
		else:
			if not row:
				print("no data")
				return

			for sig_row in row:
				url = sig_row['author_link']
				category = sig_row['category']
				yield self.make_requests_from_url(url,category)
		

	def make_requests_from_url(self,url,category):
		return self.get_html_and_carry_item(url,"mp.weixin.qq.com","http://mp.weixin.qq.com/",category)

	def parse(self,respose):
		items = []
		cSapi = sparta_api.SpartaApi()
		category = respose.meta['item']
		cSapi.getSpartaGzhInfo(respose,items,respose.url,category)

		return items