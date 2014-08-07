from flask import render_template, Flask, request
from apps import app

# app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
	get = None
	naver = ""
	daum = ""
	google = ""
	
	if request.args:
		get = request.args['text_get']
		naver = "http://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ie=utf8&query="+get+"&x=0&y=0"
		google = "https://www.google.co.kr/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#newwindow=1&q="+get
		daum = "http://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&o=&q="+get

	return render_template("index.html", naver=naver, daum=daum, google=google)

# if __name__ == "__main__":
# 	app.run(port = 5010)