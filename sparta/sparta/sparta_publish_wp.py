# -*- coding: utf-8 -*- 
#!/usr/bin/python

import sys
sys.path.append(".")
from spiders.sparta_db import mysql
from items import *
reload(sys)  
sys.setdefaultencoding("utf8") 

def initWpPosts(sContent,wechat_name,title,brief_content,replease_date):
	item = SpartaWpPostsItem()

	sContent = sContent.replace('\"', 'guaibyco')
	sContent = sContent.replace('\'', 'guaibyco')
	sContent = sContent.replace('guaibyco', '\\\"')
	sContent = sContent.replace('data-src', 'src')
	sContent = sContent.replace('src=\\\"', 'src=\\\"http://read.html5.qq.com/image?src=forum&q=5&r=0&imgflag=7&imageUrl=')

	sNowTime = "2016-11-15 18:12:00"
	item['post_author']= 1
	item['post_date']= replease_date
	item['post_date_gmt']= replease_date
	item['post_content']= sContent
	item['post_title']= title
	item['post_excerpt']= brief_content
	item['post_status']= "publish"
	item['comment_status']= "open"
	item['ping_status']= "open"
	item['post_password']= ""
	item['post_name']= wechat_name
	item['to_ping']= ""
	item['pinged']= ""
	item['post_modified']= replease_date
	item['post_modified_gmt']= replease_date
	item['post_content_filtered']= ""
	item['post_parent']= 0
	item['guid']= "11"
	item['menu_order']= 0
	item['post_type']= "post";
	item['post_mime_type']= "";
	item['comment_count']= 0

	return item

def getSpartaArticle(get_nums=1):

	m = mysql(0,'article')
	row=m.table('article').field(['author','wechat_name','introduce','qrcode_img_url','tag','title','brief_content','content','replease_date','publish_exact_tm']).where({"uin":'MzA5OTA0NDIyMQ=='}).find(get_nums) #读取

	if get_nums == 1:
		if not row:
			print("no data")
			return

		title = row['title']
		content = row['content']
		wechat_name = row['wechat_name']
		brief_content = row['brief_content']
		replease_date = row['replease_date']

		print(title)

		info = initWpPosts(content,wechat_name,title,brief_content,replease_date)

		m_wp = mysql(1,'posts')

		m_wp.table('posts').add(info)
		
	else:
		if not row:
			print("no data")
			return

		for sig_row in row:
			title = sig_row['title']
			content = sig_row['content']
			print(title)

getSpartaArticle(1) 