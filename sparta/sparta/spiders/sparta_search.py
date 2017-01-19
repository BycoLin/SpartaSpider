# -*- coding: utf-8 -*-
import sparta_api
import sparta_define
# -*- coding: utf-8 -*-
from sparta.items import *
from sparta.spiders.sparta_basic import SpartaBasic
from sparta.spiders.sparta_db import mysql
import sys  
reload(sys)  
sys.setdefaultencoding("utf8") 

class SpartaSpider(SpartaBasic):
	name = "sparta_search"
	allowed_domains = ["http://weixin.sogou.com/"]

	def start_requests(self):
		#yield self.make_requests_from_url(self.getSearchGzhText("逻辑思维"))

		get_nums = 1
		
		m = mysql(0,'gzh')
		row=m.table('gzh').field(['wechat_id','category']).order({'update_time':'asc'}).find(get_nums) #读取

		if get_nums == 1:

			if not row:
				print("no data")
				return

			search_text = row['wechat_id']
			category = row['category']
			yield self.make_requests_from_url(self.getSearchGzhText(search_text),search_text,category)
		else:
			if not row:
				print("no data")
				return

			for sig_row in row:
				search_text = sig_row['wechat_id']
				category = sig_row['category']
				yield self.make_requests_from_url(self.getSearchGzhText(search_text),search_text,category)
		
	def make_requests_from_url(self,url,search_text,category):
		return self.get_html_and_carry_items(url,"","",search_text,category)

	def parse(self,respose):
		items = []
		cSapi = sparta_api.SpartaApi()
		search_text = respose.meta['item']
		category = respose.meta['item2']
		info = cSapi.getSearchGzhFirstInfo(respose,items,search_text)
		if info:
			info['category'] = category
			return info

		return False

		