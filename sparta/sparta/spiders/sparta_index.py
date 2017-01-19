# -*- coding: utf-8 -*- 
import sparta_api
import sparta_define
from sparta.spiders.sparta_basic import SpartaBasic

class SpartaIndex(SpartaBasic):
	name = "sparta_index"
	allowed_domains = ["http://weixin.sogou.com/"]
	index_url = 'http://weixin.sogou.com/pcindex/pc/{type}/{idx}.html'

	#http://weixin.sogou.com/pcindex/pc/pc_0/pc_0.html
	def start_requests(self):
		for tag_type in sparta_define.SOGOU_TAG_TYPE_TEST:
			for tag_idx in range(0,sparta_define.SOGOU_MAX_PAG):
				url_tag_type = "pc_"+tag_type
				if tag_idx == 0:
					url_tag_idx = url_tag_type
				else:
					url_tag_idx = tag_idx

				url = self.index_url.format(type=url_tag_type,idx=url_tag_idx)

				yield self.make_requests_from_url(url,tag_type)

	def make_requests_from_url(self,url,category):
		return self.get_html_and_carry_item(url,'','',category)

	def parse(self,respose):
		items = []
		cSapi = sparta_api.SpartaApi()
		category = respose.meta['item']
		cSapi.getSpartaTagInfo(respose,items,category)

		return items


