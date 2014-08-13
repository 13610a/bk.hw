# -*- coding: utf-8 -*-
from flask import render_template, request, flash, url_for, redirect
from sqlalchemy import desc
from apps import app, db

from apps.models import Article, Comment

@app.route('/', methods=['GET'])
def article_list():

	context = {}

	context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()

	return render_template("home.html", context=context, active_tab='timeline')

@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
	if request.method == 'GET':
		return render_template('article/create.html', active_tab='article_create')
	elif request.method == 'POST':
		article_data = request.form

		article = Article(
			title = article_data['title'],
			author = article_data['author'],
			category = article_data['category'],
			content = article_data['content']
		)

		db.session.add(article)
		db.session.commit()

		flash(u'너의 흔적이 남았당..후후.', 'success')

		return redirect(url_for('article_list'))


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
	article = Article.query.get(id)

	if request.method == 'GET':
		return render_template('article/update.html',article = article)


	elif request.method == 'POST':
		article_data = request.form
		
		article = Article.query.get(id)

		article.title = article_data['title']
		article.author = article_data['author']
		article.category = article_data['category']
		article.content = article_data['content']

		db.session.commit()

		flash(u'수정되었다능! 이제 만족하냐??.', 'success')
		return redirect(url_for('article_detail', id=id))


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
	
	article = Article.query.get(id)


	if request.method == 'GET': 	
		return render_template('article/delete.html')

	elif request.method == 'POST':
		db.session.delete(article)
		db.session.commit()

	flash(u'우리의 추억을 삭제했다..ㅜ', 'success')
	return redirect(url_for('article_list'))

@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
	article = Article.query.get(id)

	comments = article.comments.order_by(desc(Comment.likeit)).all()

	return render_template('article/detail.html', article=article, comments=comments)

#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
	if request.method =='GET':
		return render_template('comment/create.html')
	elif request.method == 'POST':

		comment_data = request.form

		comment = Comment(
			
			author = comment_data['author'],
			email = comment_data['email'],
			content = comment_data['content'],
			password = comment_data['password'],
			article = Article.query.get(article_id)
		)

		db.session.add(comment)
		db.session.commit()

		flash(u'댓글을 작성했다.참견하니 속이 후련하냐?', 'success')
		return redirect(url_for('article_detail', id=article_id))

@app.route('/comment/likeit/<int:comment_id>')
def comment_likeit(comment_id):
	comment = Comment.query.get(comment_id)
	comment.likeit += 1
	db.session.commit()
	return redirect(url_for('article_detail', id=comment.article_id))

#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
	return render_template('500.html'), 500


