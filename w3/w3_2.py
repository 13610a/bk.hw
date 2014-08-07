# -*- coding:utf-8 -*-
import urllib
from bs4 import BeautifulSoup

#htmltext변수 안에 html문서 저장
##########################"                      인터넷 주소                      "부분을 수정하세요!
htmltext = urllib.urlopen("http://www.ilbe.com/fear").read()

#뷰티플수프 형식으로 저장
soup = BeautifulSoup(htmltext, from_encoding="utf-8")

#제목을 저장할 배열 선언
titles = []

#soup에 있는 데이터를 파싱해서 title 배열 안에 저장
########################" .클래스이름 "부분을 수정하세요!
for item in soup.select(".title"):
#class = t_subject인 테그의 하위 태그를 item에 저장
	titles.append(item.get_text())#get_text함수 : 테그(<>)를 제외한 글자만 저장

#출력
for title in titles:
	print title.encode('utf-8')