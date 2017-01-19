# -*- coding: utf-8 -*- 

#sparta_index定义

#取特定标签类别最大页数
SOGOU_MAX_PAG = 1

#搜狗微信标签类别代号
SOGOU_TAG_TYPE=[
				"0",#热门
				"1",#推荐
				"2",#段子手
				"3",#养生堂
				"4",#私房话
				"5",#八卦精
				"6",#爱生活
				"7",#财经迷
				"8",#汽车迷
				"9",#科技咖
				"10",#潮人帮
				"11",#辣妈帮
				"12",#点赞党
				"13",#旅行家
				"14",#职场人
				"15",#美食家
				"16",#古今通
				"17",#学霸族
				"18",#星座控
				"19",#体育迷
				]

SOGOU_TAG_TYPE_TEST=[
					"0",#热门
					]

#sparta_api定义
QRCODE_IMG_URL_PRE = "http://mp.weixin.qq.com/mp/qrcode?scene=10000004&size=102&__biz="

WEIXIN_QQ_URL_PRE = "http://mp.weixin.qq.com"

#链接已过期
LINK_OVER_TIME = "link_over_time"
#链接访问失败
LINK_PING_ERROR = "link_ping_error"
#链接访问成功
LINK_PING_SUCC = "link_ping_succ"

#临时文章url加上这个参数可找到真实url(其实只要直接&uin=xxxxx即可)
TMP_URL_2_TRUE_URL_1="&devicetype=Windows-QQBrowser&version=61030004&pass_ticket=qMx7ntinAtmqhVn+C23mCuwc9ZRyUp20kIusGgbFLi0=&uin="
TMP_URL_2_TRUE_URL_2="&ascene=1"
