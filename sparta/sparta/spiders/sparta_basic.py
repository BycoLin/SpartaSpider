# -*- coding: utf-8 -*-
import random
import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request
from lxml import etree

class SpartaBasic(Spider):

	def __init__(self):
		
		self.agent = [
			"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
			"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
			"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
			"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
			"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
			"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
			"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
			"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
			"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
			"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
		]

	def get(self, url, host='', referer=''):
		"""
			封装request库get方法
		Args:
			url: 请求url
			host: 请求host
			referer: 请求referer
		Returns:
			text: 请求url的网页内容
		"""

		headers = {
			"User-Agent": self.agent[random.randint(0, len(self.agent) - 1)],
			'Host': host if host else 'weixin.sogou.com',
			"Referer": referer if referer else 'http://weixin.sogou.com/',
		}

		return Request(url,headers=headers,dont_filter=True)

	def get_html_and_carry_item(self, url, host='', referer='',item=''):
		"""
			封装request库get方法
		Args:
			url: 请求url
			host: 请求host
			referer: 请求referer
			item: 携带参数
		Returns:
			text: 请求url的网页内容
		"""

		headers = {
			"User-Agent": self.agent[random.randint(0, len(self.agent) - 1)],
			'Host': host if host else 'weixin.sogou.com',
			"Referer": referer if referer else 'http://weixin.sogou.com/',
		}

		request = Request(url,headers=headers,dont_filter=True)
		request.meta['item'] = item
		return request

	def get_html_and_carry_items(self, url, host='', referer='',item='',item2=''):
		"""
			封装request库get方法
		Args:
			url: 请求url
			host: 请求host
			referer: 请求referer
			item: 携带参数
		Returns:
			text: 请求url的网页内容
		"""

		headers = {
			"User-Agent": self.agent[random.randint(0, len(self.agent) - 1)],
			'Host': host if host else 'weixin.sogou.com',
			"Referer": referer if referer else 'http://weixin.sogou.com/',
		}

		request = Request(url,headers=headers,dont_filter=True)
		request.meta['item'] = item
		request.meta['item2'] = item2
		return request

	def getElemText(self, elem):
		"""抽取lxml.etree库中elem对象中文字

		Args:
			elem: lxml.etree库中elem对象

		Returns:
			elem中文字
		"""
		rc = []
		for node in elem.itertext():
			rc.append(node.strip())
		return ''.join(rc)

	def getSearchGzhText(self, name, page=1):
		"""通过搜狗搜索获取关键字返回的文本

		Args:
			name: 搜索关键字
			page: 搜索的页数

		Returns:
			text: 返回的文本
			urllib2.request.quote(
		"""
		request_url = 'http://weixin.sogou.com/weixin?query=' + name + '&_sug_type_=&_sug_=n&type=1&page=' + str(page) + '&ie=utf8'

		return request_url

	def replace_html(self, s):
		"""替换html‘&quot;’等转义内容为正常内容

		Args:
			s: 文字内容

		Returns:
			s: 处理反转义后的文字
		"""
		s = s.replace('&quot;','"')
		s = s.replace('&amp;','&')
		s = s.replace('amp;','')
		s = s.replace('&lt;','<')
		s = s.replace('&gt;','>')
		s = s.replace('&nbsp;',' ')
		s = s.replace(u'\xa0',u' ')
		s = s.replace('\\',' ')
		s = s.replace('\'','\\\'')
		s = s.replace('  ','')
		s = s.replace('😊','')
		
		return s