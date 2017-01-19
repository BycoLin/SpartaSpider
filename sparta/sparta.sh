#!/bin/bash

help()
{
	echo "欢迎使用sparta"
	echo "使用方法说明如下："
	echo "(1):  ./sparta.sh sparta_index    //爬取搜狗微信主页各类别各页数据入临时公众号表和热点文章表中"
	echo "(2):  ./sparta.sh sparta_gzh_url  //临时公众号表取特定数目公众号url爬取公众号具体信息和文章临时信息"
	echo "(3):  ./sparta.sh sparta_url      //临时文章表取特定数目文章url爬取文章具体信息"
	echo "(4):  ./sparta.sh sparta_search   //搜索特定关键字返回的信息"
}

if [ $# != 1 ];
then
	help
	exit 1
else
	cd ./sparta/spiders/
	scrapy crawl $1
fi 