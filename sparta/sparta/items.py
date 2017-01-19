# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item,Field

'''
公众号这个功能点，就是一个公众号列表（有序），列表项内容是：
1. 公众号id(sst_id)
2. 公众号名字(sst_name)
3. 公众号头像(sst_profile)
4. 文章的id
5. 文章要可以找到对应的公众号，反过来也要

index_tag -> hot_article
		  -> author_url -> index_gzh_info -> gzh
		  								  -> article_url -> article

search -> author_url -> gzh

#更新公众号信息，并顺便增加和更新其文章
gzh -> uin -> search -> author_url -> index_gzh_info -> gzh
												     -> article_url -> article
'''

#类别信息临时结构
class SpartaTagInfoItem(scrapy.Item):
	wechat_name = Field()		#公众号名称
	content_url = Field()		#文章url
	author_link = Field()		#作者链接
	author_img_url = Field()	#作者头像url
	qrcode_img_url = Field()	#二维码url
	content_img_url = Field()	#文章首图url
	title = Field()				#文章标题
	content = Field()			#简要内容
	category = Field()			#类别

#类别公众号表
class SpartaTagGzhInfoItem(scrapy.Item):
	wechat_name = Field()		#公众号名称
	author_link = Field()		#作者链接
	author_img_url = Field()	#作者头像url
	qrcode_img_url = Field()	#二维码url
	category = Field()			#类别
	if_spider = Field()			#是否已爬取 0表示未爬取 1表示已爬取 2表示链接已过期 3表示更新公众号

#热文记录表
class SpartaTagArticleInfoItem(scrapy.Item):
	wechat_name = Field()		#公众号名称
	content_url = Field()		#文章url
	content_img_url = Field()	#文章首图url
	title = Field()				#文章标题
	content = Field()			#简要内容
	if_spider = Field()			#是否已爬取

#文章临时存储
class SpartaTmpArticleInfoItem(scrapy.Item):
	uin = Field()				#uin
	content_url = Field()		#文章url
	wechat_name = Field()		#公众号名称
	content_img_url = Field()	#文章首图url
	title = Field()				#文章标题
	content = Field()			#简要内容
	if_spider = Field()			#是否已爬取

#文章表
class SpartaArticleItem(scrapy.Item):
	uin = Field()				#uin
	true_content_link = Field()	#真实的文章url
	wechat_id = Field()			#公众号id
	author = Field()			#作者
	wechat_name = Field()		#公众号名称
	introduce = Field()			#介绍
	qrcode_img_url = Field()	#二维码url
	tag = Field()				#标签
	title = Field()				#标题
	brief_content = Field()		#简要内容
	content = Field()			#内容（包括格式）
	replease_date = Field()		#发布日期
	publish_exact_tm = Field()	#发布确切时间
	content_url = Field()		#文章临时url
	content_img_url = Field()	#文章首图url
	official_web_url = Field()	#官网url

#公众号表
class SpartaGzhItem(scrapy.Item):
	uin = Field()				#uin
	wechat_id = Field()			#公众号id
	wechat_name = Field()		#公众号名称
	introduce = Field()			#介绍
	renzhen = Field()			#认证，为空表示未认证，为1表示认证
	account_subject = Field()   #账号主体
	qrcode_img_url = Field()	#二维码
	author_img_url = Field()	#头像图片
	category = Field()			#类别
	author_link = Field()		#作者链接

#公众号主页的具体信息
class SpartaGzhArticleInfoItem(scrapy.Item):
	#公众号主页信息
	uin = Field()				#uin
	wechat_id = Field()			#公众号id
	wechat_name = Field()		#公众号名称
	introduce = Field()			#介绍
	renzhen = Field()			#认证，为空表示未认证，为1表示认证
	account_subject = Field()   #账号主体
	qrcode_img_url = Field()	#二维码
	author_img_url = Field()	#头像图片
	category = Field()			#类别
	author_link = Field()		#作者链接
	#公众号主页的文章信息
	content_url = Field()		#文章url
	content_img_url = Field()	#文章首图url
	title = Field()				#文章标题
	content = Field()			#简要内容
	#爬取结果
	ret = Field()               #结果

#搜索表
class SpartaSearchItem(scrapy.Item):
	wechat_name = Field()		#公众号名称
	wechat_id = Field()			#公众号id
	author_link = Field()		#作者链接
	introduce = Field()			#介绍
	renzhen = Field()			#认证，为空表示未认证
	qrcode_img_url = Field()	#二维码
	author_img_url = Field()	#头像图片
	content_url = Field()		#最近文章地址
	category = Field()			#类别

#wordpress的wp_posts文章表
class SpartaWpPostsItem(scrapy.Item):
	ID = Field()				#自增唯一ID
	post_author= Field()		#对应作者ID
	post_date= Field()			#发布时间
	post_date_gmt= Field()		#发布时间（GMT+0时间）
	post_content= Field()		#正文
	post_title= Field()			#标题
	post_excerpt= Field()		#摘录
	post_status= Field()		#文章状态（publish/auto-draft/inherit等）
	comment_status= Field()		#评论状态（open/closed）
	ping_status= Field()		#PING状态（open/closed）
	post_password= Field()		#文章密码
	post_name= Field()			#文章缩略名
	to_ping= Field()			#未知
	pinged= Field()				#已经PING过的链接
	post_modified= Field()		#修改时间
	post_modified_gmt= Field()	#修改时间（GMT+0时间）
	post_content_filtered= Field()	#未知
	post_parent= Field()		#父文章，主要用于PAGE
	guid= Field()				#未知
	menu_order= Field()			#排序ID
	post_type= Field()			#文章类型（post/page等）
	post_mime_type= Field()		#MIME类型
	comment_count= Field()		#评论总数

#wordpress的wp_term_relationships文章关系表
class SpartaWpTermRelationShipsItem(scrapy.Item):	
	object_id = Field()
	term_taxonomy_id = Field()
	term_order = Field()