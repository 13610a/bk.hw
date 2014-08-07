#-*- coding: utf-8 -*-
# JTBC 뉴스 속보 xml문서 파싱하기

import urllib
from xml.etree.ElementTree import parse

xml = urllib.urlopen('http://fs.jtbc.joins.com/RSS/newsflash.xml')	# 속보

tree = parse(xml)		# xml 파싱하여 나뭇가지 구조 얻기
root = tree.getroot()	# root태그 얻어오기

for parent in root.getiterator():	# root태그부터 시작하여 모든 태그를 반복
	for child in parent.findall("item"):	# item 태그를 모두 반복

		# 뉴스 제목 보기
		print child.find("title").text
#		print child.findtext("title")
		
		# 뉴스 내용 보기
#		print child.findtext("description")
