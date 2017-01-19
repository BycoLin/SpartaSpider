# -*- coding: utf-8 -*-
from sparta.items import *
from sparta.spiders.sparta_basic import SpartaBasic
from lxml import etree
import re
import sparta_define
import json
import sys  
reload(sys)  
sys.setdefaultencoding("utf8") 

class SpartaApi(SpartaBasic):

	#获取搜狗微信标签类别页详细内容[一页20篇]
	'''原来搜狗微信首页旧版本页面解析代码
	def getSpartaTagInfo(self,respose,items,category):
		"""
		Returns:
			wechat_name：公众号名称
			author_link：作者链接
			content：简要内容
			content_url：文章url
			title：文章标题
			author_img_url：作者头像url
			content_img_url：文章首图url
			qrcode_img_url：二维码url
		"""

		wechat_name = list()
		author_link = list()
		author_img_url = list()
		qrcode_img_url =list()
		content_img_url = list()
		content = list()
		content_url = list()
		title = list()

		print("ok")

		for hotinfo in respose.xpath(u'//div[@class="pos-wxrw"]'):
			try:
				wechat_name.append(hotinfo.xpath(u'a/p[2]/text()').extract()[0])
			except Exception,e:
				wechat_name.append(u"helloworld")

				print(wechat_name)

			try:
				author_link.append(hotinfo.xpath(u'a/@href').extract()[0])
			except Exception,e:
				author_link.append(u"helloworld")

			try:
				author_img_url.append(hotinfo.xpath(u'a/p/img/@src').extract()[0])
			except Exception,e:
				author_img_url.append(u"helloworld")

			try:
				qrcode_img_url.append(hotinfo.xpath(u'div/div[@class="pos-box"]/img/@src').extract()[0])
			except Exception,e:
				qrcode_img_url.append(u"helloworld") 

		for hotinfo in respose.xpath(u'//div[@class="wx-img-box"]/a/img'):

			try:
				content_img_url.append(hotinfo.xpath(u'@src').extract()[0])
			except Exception,e:
				content_img_url.append(u"helloworld") 

		for hotinfo in respose.xpath(u'//div[@class="wx-news-info2"]'):

			try:
				content.append(hotinfo.xpath(u'a/text()').extract()[0])
			except Exception,e:
				content.append(u"helloworld")

			try:
				content_url.append(hotinfo.xpath(u'a/@href').extract()[0])
			except Exception,e:
				content_url.append(u"helloworld") 

			try:
				title.append(hotinfo.xpath(u'h4/a/text()').extract()[0])
			except Exception,e:
				title.append(u"helloworld") 

		for x in range(len(wechat_name)):

			item = SpartaTagInfoItem()

			item['wechat_name'] = wechat_name[x]
			item['author_link'] = author_link[x]
			item['content'] = content[x]
			item['content_url'] = content_url[x]
			item['title'] = title[x]
			item['author_img_url'] = author_img_url[x]
			item['content_img_url'] = content_img_url[x]
			item['qrcode_img_url'] = qrcode_img_url[x]
			item['category'] = category

			items.append(item)

		return items
	'''

	#获取搜狗微信标签类别页详细内容[一页20篇]（新版本的搜狗微信）
	#没有作者头像url和二维码url
	def getSpartaTagInfo(self,respose,items,category):
		"""
		Returns:
			wechat_name：公众号名称
			author_link：作者链接
			content：简要内容
			content_url：文章url
			title：文章标题
			author_img_url：作者头像url
			content_img_url：文章首图url
			qrcode_img_url：二维码url
		"""

		wechat_name = list()
		author_link = list()
		content_img_url = list()
		content = list()
		content_url = list()
		title = list()

		for hotinfo in respose.xpath(u'//a[@class="account"]'):
			print(hotinfo)
			try:
				wechat_name.append(hotinfo.xpath(u'text()').extract()[0])
			except Exception,e:
				wechat_name.append(u"helloworld")

			try:
				author_link.append(hotinfo.xpath(u'@href').extract()[0])
			except Exception,e:
				author_link.append(u"helloworld")

		for hotinfo in respose.xpath(u'//img[@onload="resizeImage(this)"]'):

			try:
				content_img_url.append(hotinfo.xpath(u'@src').extract()[0])
			except Exception,e:
				content_img_url.append(u"helloworld") 

		for hotinfo in respose.xpath(u'//p[@class="txt-info"]'):

			try:
				content.append(hotinfo.xpath(u'text()').extract()[0])
			except Exception,e:
				content.append(u"helloworld")

		for x in range(len(wechat_name)):
			pc_tag_type = "pc_"+category

			idx = str(x)

			title_tag_type = pc_tag_type + "_" + idx + "_title"

			x_title = '//a[@uigs=\"'+title_tag_type+'\"]'

			for hotinfo in respose.xpath(x_title):

				try:
					content_url.append(hotinfo.xpath(u'@href').extract()[0])
				except Exception,e:
					content_url.append(u"helloworld") 

				try:
					title.append(hotinfo.xpath(u'text()').extract()[0])
				except Exception,e:
					title.append(u"helloworld") 

		for x in range(len(wechat_name)):

			item = SpartaTagInfoItem()

			item['wechat_name'] = wechat_name[x]
			item['author_link'] = author_link[x]
			item['content'] = content[x]
			item['content_url'] = content_url[x]
			item['title'] = title[x]
			item['author_img_url'] = ""
			item['content_img_url'] = content_img_url[x]
			item['qrcode_img_url'] = ""
			item['category'] = category

			items.append(item)

		return items

	#获取搜狗微信文章url对应的详细内容
	def getSpartaArticleInfo(self,respose,items,content_url):
		"""
		Returns:
			author：作者
			content：内容（包括格式）
			true_content_link：真实的文章url
			title：标题
			brief_content:简要内容
			qrcode_img_url：二维码url
			wechat_id：公众号id
			wechat_name：公众号名称
			introduce：介绍
			tag：标签
			replease_date：发布日期
			publish_exact_tm: 发布确切时间
			content_url：文章临时url
			content_img_url ：文章首图url
			official_web_url : 官网url
		"""

		for hotinfo in respose.xpath(u'//h2[@id="activity-name"]'):

			try:
				title = hotinfo.xpath(u'text()').extract()[0]
			except Exception,e:
				title = "helloworld" 

			title = self.replace_html(title)
			title = title.replace('\r', '')
			title = title.replace('\n', '')
			print(title)

		for hotinfo in respose.xpath(u'//div[@class="rich_media_meta_list"]'):

			try:
				author = hotinfo.xpath(u'em[2]/text()').extract()[0]
			except Exception,e:
				author = "" 

			print(author)

			try:
				tag = hotinfo.xpath(u'span[@id="copyright_logo"]/text()').extract()[0]
			except Exception,e:
				tag = "" 

			print(tag)

			try:
				replease_date = hotinfo.xpath(u'em[@id="post-date"]/text()').extract()[0]
			except Exception,e:
				replease_date = "helloworld" 

			print(replease_date)

			try:
				wechat_name = hotinfo.xpath(u'div[@id="js_profile_qrcode"]/div/strong[@class="profile_nickname"]/text()').extract()[0]
			except Exception,e:
				wechat_name = "helloworld" 

			print(wechat_name)

			try:
				wechat_id = hotinfo.xpath(u'div[@id="js_profile_qrcode"]/div/p[1]/span/text()').extract()[0]
			except Exception,e:
				wechat_id = "helloworld" 

			print(wechat_id)

			try:
				introduce = hotinfo.xpath(u'div[@id="js_profile_qrcode"]/div/p[2]/span/text()').extract()[0]
			except Exception,e:
				introduce = "helloworld" 

			introduce = self.replace_html(introduce)
			print(introduce)		

		for hotinfo in respose.xpath(u'//div[@id="js_content"]'):

			try:
				content = hotinfo.extract()
			except Exception,e:
				content = "helloworld" 

			content = self.replace_html(content)

		for hotinfo in respose.xpath(u'//*[@id="activity-detail"]/script[4]'):

			try:
				true_content_link = hotinfo.xpath(u'text()').extract()[0]

				msg = "msg_link = "
				leng = len(msg)+1

				appuin_tmp = true_content_link
				img_cdn_url = true_content_link
				ct_tmp = true_content_link
				brief_tmp = true_content_link

				true_content_link = true_content_link[true_content_link.rfind(msg)+leng:-1] 
				true_content_link = true_content_link[0:true_content_link.find("\"")] 
				true_content_link = true_content_link.replace('amp;', '')

				print(true_content_link)

				biz_find = true_content_link
				biz = "__biz="
				biz_len = len(biz)

				if biz_find.find(biz) >= 0 :
					biz_find = biz_find[biz_find.rfind(biz)+biz_len:biz_find.rfind("&mid")] 
				else:
					true_content_link = ""
					msg_app_uin = "appuin = \"\"||\""
					app_uin_len = len(msg_app_uin)

					appuin_tmp = appuin_tmp[appuin_tmp.rfind(msg_app_uin)+app_uin_len:-1] 
					appuin_tmp = appuin_tmp[0:appuin_tmp.find("\"")] 

					if  len(appuin_tmp) > 0 :
						biz_find = appuin_tmp

				cdn_url = "msg_cdn_url = "
				cdn_leng = len(cdn_url)+1

				img_cdn_url = img_cdn_url[img_cdn_url.rfind(cdn_url)+cdn_leng:-1] 
				img_cdn_url = img_cdn_url[0:img_cdn_url.find("\"")] 

				content_img_url = img_cdn_url

				exact_tm = "ct = "
				exact_tm_leng = len(exact_tm)+1

				ct_tmp = ct_tmp[ct_tmp.rfind(exact_tm)+exact_tm_leng:-1] 
				ct_tmp = ct_tmp[0:ct_tmp.find("\"")] 

				publish_exact_tm = ct_tmp

				desc_tmp = "msg_desc = "
				desc_tmp_leng = len(desc_tmp)+1

				brief_tmp = brief_tmp[brief_tmp.rfind(desc_tmp)+desc_tmp_leng:-1] 
				brief_tmp = brief_tmp[0:brief_tmp.find("\"")] 

				brief_content = brief_tmp
				brief_content = self.replace_html(brief_content)

			except Exception,e:
				true_content_link = "" 
				biz_find = ""
				content_img_url = ""
				publish_exact_tm = ""
				brief_content = ""

			print(true_content_link)

		qrcode_img_url = sparta_define.QRCODE_IMG_URL_PRE+biz_find
		uin = biz_find

		item = SpartaArticleItem()

		item['uin'] = uin
		item['true_content_link'] = true_content_link
		item['author'] = author
		item['content'] = content
		item['title'] = title
		item['qrcode_img_url'] = qrcode_img_url
		item['wechat_id'] = wechat_id
		item['wechat_name'] = wechat_name
		item['introduce'] = introduce
		item['tag'] = tag
		item['replease_date'] = replease_date
		item['publish_exact_tm'] = publish_exact_tm
		item['content_url'] = content_url
		item['content_img_url'] = content_img_url
		item['brief_content'] = brief_content
		item['official_web_url'] = ""
		
		items.append(item)	

		return items

	#获取搜狗微信搜索公众号返回的详细内容
	def getSearchGzhInfo(self,respose,items):
		"""
		Returns:
			wechat_name: 公众号名称
			wechat_id: 公众号id
			author_link: 作者链接
			introduce: 介绍
			renzhen: 认证，为空表示未认证
			qrcode_img_url: 二维码
			author_img_url: 头像图片
			content_url: 最近文章地址
			category: 类别
		"""

		author_img_url 	= list()
		content_url 	= list()
		wechat_name		= list()
		wechat_id 		= list()
		introduce		= list()
		renzhen 		= list()
		qrcode_img_url  = list()
		author_link     = list()

		ht = respose.text
		page = etree.HTML(ht)
		
		info_imgs = page.xpath(u"//div[@class='img-box']/img")
		for info_img in info_imgs:
			author_img_url.append(info_img.attrib['src'])
		
		info_urls = page.xpath(u"//div[@target='_blank']")
		for info_url in info_urls:
			content_url.append(info_url.attrib['href'])

		author_links = page.xpath(u"//div[@class='wx-rb bg-blue wx-rb_v1 _item']")
		for author_link_tmp in author_links:
			author_link.append(author_link_tmp.attrib['href'])
		
		info_instructions = page.xpath(u"//div[@class='txt-box']")
		for info_instruction in info_instructions:
			cache = self.getElemText(info_instruction)
			cache = cache.replace('red_beg', '').replace('red_end', '')
			cache_list = cache.split('\n')
			cache_re = re.split(u'微信号：|功能介绍：|认证：|最近文章：', cache_list[0])			
			wechat_name.append(cache_re[0])
			wechat_id.append(cache_re[1])

			leng = len(cache_re)

			if leng >= 4 and "authnamewrite" in cache_re[2]:
				introduce.append(re.sub("authnamewrite\('[0-9]'\)", "", cache_re[2]))
				renzhen.append(cache_re[3])
			else:
				if leng >= 3:
					introduce.append(cache_re[2])
				else:
					introduce.append('')

				renzhen.append('')
		
		info_qrcodes = page.xpath(u"//div[@class='pos-ico']/div/img")
		for info_qrcode in info_qrcodes:
			qrcode_img_url.append(info_qrcode.attrib['src'])

		for i in range(len(qrcode_img_url)):
			item = SpartaSearchItem()

			item['wechat_name']=wechat_name[i]
			item['wechat_id']=wechat_id[i]
			item['author_link'] = author_link[i]
			item['introduce']=introduce[i]
			item['renzhen']=renzhen[i]
			item['qrcode_img_url']=qrcode_img_url[i]
			item['author_img_url']=author_img_url[i]
			item['content_url']=content_url[i]
			item['category'] = 0

			items.append(item)

		return items 

	def getSearchGzhFirstInfo(self,respose,items,wechatid):
		"""获取公众号微信号wechatid的信息

		因为wechatid唯一确定，所以第一个就是要搜索的公众号

		Args:
			wechatid: 公众号id

		Returns:
			wechat_name: 公众号名称
			wechat_id: 公众号id
			introduce: 介绍
			renzhen: 认证，为空表示未认证
			qrcode_img_url: 二维码
			author_img_url: 头像图片
			content_url: 最近文章地址
		"""
		
		self.getSearchGzhInfo(respose,items)

		if items:
			info = items[0]
			if info['wechat_id'] == wechatid:
				return info
		
		return False

	#获取搜狗微信作者url对应的详细内容
	def getSpartaGzhInfo(self,respose,items,author_link,category):
		"""
		Returns:
			uin ：uin
			wechat_id ：公众号id
			wechat_name ：公众号名称
			introduce ：介绍
			renzhen：认证，为空表示未认证
			account_subject：账号主体
			qrcode_img_url：二维码
			author_img_url：头像图片
			category：类别
			author_link：作者链接

			content_url ：文章url
			content_img_url : 文章首图url
			title ：文章标题
			content ：简要内容
			if_spider ：是否已爬取
		"""

		uin = ""				#uin
		wechat_id = ""			#公众号id
		wechat_name = ""		#公众号名称
		introduce = ""			#介绍
		renzhen = ""			#认证，为空表示未认证，为1表示认证
		account_subject = ""    #账号主体
		qrcode_img_url = ""	    #二维码
		author_img_url = ""	    #头像图片

		content_url = list()			#文章url
		content_img_url = list()		#文章首图url
		title = list()					#文章标题
		content = list()				#简要内容

		try: 
			error_msg = respose.xpath(u'//div[@class="global_error_msg warn"]/text()').extract()[0]
		except Exception,e:
			error_msg = ""

		item = SpartaGzhArticleInfoItem()

		#链接已过期
		if error_msg != "":
			print(error_msg)
			item['author_link'] = author_link
			item['ret'] = sparta_define.LINK_OVER_TIME
			items.append(item)
			return items

		try: 
			str_biz = respose.xpath(u'body/script[5]/text()').extract()[0]

			article_info = str_biz

			msg = "biz = "
			leng = len(msg)+1

			str_biz = str_biz[str_biz.rfind(msg)+leng:-1] 
			str_biz = str_biz[0:str_biz.find("\"")] 

			print(str_biz)

			article_info = article_info.replace('&quot;','"')

			msglist = "msgList = "
			msglist_len = len(msglist)+1

			article_info = article_info[article_info.find(msglist)+msglist_len:-1] 
			article_info = article_info[0:article_info.rfind(";")] 
			article_info = article_info[0:article_info.rfind(";")-1] 

			json_data = json.loads(article_info)

			for j in json_data['list']:
				title2 = j['app_msg_ext_info']['title']
				title2 = self.replace_html(title2)
				title2 = title2.replace('&quot;', '\"')
				title2 = title2.replace('\r', '')
				title2 = title2.replace('\n', '')
				title.append(title2)

				digest = j['app_msg_ext_info']['digest']
				digest = self.replace_html(digest)
				digest = digest.replace('&quot;', '\"')
				digest = digest.replace('\r', '')
				digest = digest.replace('\n', '')
				content.append(digest)

				tmp_content_url = j['app_msg_ext_info']['content_url']
				tmp_content_url = tmp_content_url.replace('\\','')
				tmp_content_url = tmp_content_url.replace('&amp;','&')
				tmp_content_url = tmp_content_url.replace('amp;','')
				tmp_content_url = sparta_define.WEIXIN_QQ_URL_PRE+tmp_content_url
				content_url.append(tmp_content_url)

				cover = j['app_msg_ext_info']['cover']
				cover = cover.replace('\\','')
				content_img_url.append(cover)

				for m in j['app_msg_ext_info']['multi_app_msg_item_list']:
					title2 = m['title']
					title2 = self.replace_html(title2)
					title2 = title2.replace('&quot;', '\"')
					title2 = title2.replace('\r', '')
					title2 = title2.replace('\n', '')
					title.append(title2)

					digest = m['digest']
					digest = self.replace_html(digest)
					digest = digest.replace('&quot;', '\"')
					digest = digest.replace('\r', '')
					digest = digest.replace('\n', '')
					content.append(digest)

					tmp_content_url = m['content_url']
					tmp_content_url = tmp_content_url.replace('\\','')
					tmp_content_url = tmp_content_url.replace('&amp;','&')
					tmp_content_url = tmp_content_url.replace('amp;','')
					tmp_content_url = sparta_define.WEIXIN_QQ_URL_PRE+tmp_content_url
					content_url.append(tmp_content_url)

					cover = m['cover']
					cover = cover.replace('\\','')
					content_img_url.append(cover)

		except Exception,e:
			str_biz = ""

		#链接访问失败,下次重访问即可
		if str_biz == "s.use(":
			item['ret'] = sparta_define.LINK_PING_ERROR
			items.append(item)
			return items

		qrcode_img_url = sparta_define.QRCODE_IMG_URL_PRE+str_biz
		uin = str_biz

		for hotinfo in respose.xpath(u'//div[@class="profile_info_area"]'):

			try:
				author_img_url = hotinfo.xpath(u'div[@class="profile_info_group"]/span/img/@src').extract()[0]
			except Exception,e:
				author_img_url = "" 

			print(author_img_url)

			try:
				wechat_name = hotinfo.xpath(u'div[@class="profile_info_group"]/div/strong/text()').extract()[0]
			except Exception,e:
				wechat_name = "" 

			wechat_name = self.replace_html(wechat_name)
			wechat_name = wechat_name.replace('\r', '')
			wechat_name = wechat_name.replace('\n', '')
			wechat_name = wechat_name.replace('  ', '')

			print(wechat_name)

			try:
				wechat_id = hotinfo.xpath(u'div[@class="profile_info_group"]/div/p/text()').extract()[0]
			except Exception,e:
				wechat_id = "" 

			wechat_id = wechat_id.replace('微信号: ', '')

			print(wechat_id)

			try:
				introduce = hotinfo.xpath(u'ul[@class="profile_desc"]/li[1]/div[@class="profile_desc_value"]/text()').extract()[0]
			except Exception,e:
				introduce = "" 

			introduce = self.replace_html(introduce)

			print(introduce)

			try:
				renzhen = hotinfo.xpath(u'ul[@class="profile_desc"]/li[2]/div[@class="profile_desc_value"]/img[@class="icon_verify success"]/@src').extract()[0]
			except Exception,e:
				renzhen = "" 

			if renzhen != "":
				renzhen = 1
			else:
				renzhen = 0

			print(renzhen)

			try:
				account_subject = hotinfo.xpath(u'ul[@class="profile_desc"]/li[2]/div[@class="profile_desc_value"]/text()').extract()[0]
			except Exception,e:
				account_subject = "" 

			account_subject = self.replace_html(account_subject)

			print(account_subject)
		
		item['uin'] = uin
		item['wechat_id'] = wechat_id
		item['wechat_name'] = wechat_name
		item['introduce'] = introduce
		item['renzhen'] = renzhen
		item['account_subject'] = account_subject
		item['qrcode_img_url'] = qrcode_img_url
		item['author_img_url'] = author_img_url
		item['category'] = category
		item['author_link'] = author_link
		item['ret'] = sparta_define.LINK_PING_SUCC

		item['content_url'] = list()
		item['content_img_url']  = list()
		item['title']  = list()
		item['content']  = list()

		for i in range(len(content_url)):
			item['content_url'].append(content_url[i])
			item['content_img_url'].append(content_img_url[i])
			item['title'].append(title[i])
			item['content'].append(content[i])

		items.append(item)	

		return items
