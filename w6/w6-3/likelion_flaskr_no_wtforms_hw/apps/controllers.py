# -*- coding: utf-8 -*-
from kstime import kstime
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import desc
from apps import app, db

from apps.models import (
    Aarticle,
    Ccomment
)


@app.route('/', methods=['GET'])
def article_list():
    context = {}

    context['article_list'] = Aarticle.query.order_by(desc(Aarticle.date_created)).all()

    return render_template("home.html", context=context, active_tab='timeline')


@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    if request.method == 'GET':
        return render_template('article/create.html', active_tab='article_create')
    elif request.method == 'POST':
        article_data = request.form

        article = Aarticle(
            title=article_data['title'],
            author=article_data['author'],
            category=article_data['category'],
            content=article_data['content'],
            date_created = kstime(9)
        )

        db.session.add(article)
        db.session.commit()

        flash(u'게시글이 작성되었습니다.', 'success')

        return redirect(url_for('article_list'))


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    article = Aarticle.query.get(id)
    comments = Ccomment.query.order_by(desc(Ccomment.date_created)).filter_by(article_id=article.id)

    return render_template('article/detail.html', article=article, comments=comments)


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    if request.method == 'GET':
        article = Aarticle.query.get(id)

        return render_template('article/update.html', article=article)
    elif request.method == 'POST':
        article_data = request.form

        article = Aarticle.query.get(id)
        article.title = article_data['title']
        article.author = article_data['author']
        article.category = article_data['category']
        article.content = article_data['content']

        db.session.commit()

        return redirect(url_for('article_detail', id=id))


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'POST':
        article = Aarticle.query.get(id)
        db.session.delete(article)
        db.session.commit()

        flash(u'게시글을 삭제하였습니다.', 'success')
        return redirect(url_for('article_list'))
    return render_template('article/delete.html', article_id=id)


@app.route('/article/like/<int:id>', methods=['GET'])
def article_like(id):
    article = Aarticle.query.get(id)
    article.like += 1

    db.session.commit()

    return redirect(url_for('article_detail', id=id))


@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    if request.method == 'GET':
        return render_template('comment/create.html')
    elif request.method == 'POST':
        comment_data = request.form

        comment = Ccomment(
            author=comment_data['author'],
            email=comment_data['email'],
            content=comment_data['content'],
            password=comment_data['password'],
            date_created = kstime(9),
            article_id=article_id
        )

        db.session.add(comment)
        db.session.commit()

        flash(u'댓글을 작성하였습니다.', 'success')
        return redirect(url_for('article_detail', id=article_id))


@app.route('/comment/delete/<int:id>', methods=['GET', 'POST'])
def comment_delete(id):
    if request.method == 'POST':
        comment = Ccomment.query.get(request.form['comment_id'])

        if request.form['password'] == comment.password:
            article_id = comment.article_id
            db.session.delete(comment)
            db.session.commit()

            flash(u'댓글을 삭제하였습니다.', 'success')
            return redirect(url_for('article_detail', id=article_id))
        else:
            flash(u'비밀번호가 일치하지 않습니다. 다시 한번 입력해주세요.', 'danger')
            return render_template('comment/delete.html', comment_id=request.form['comment_id'])

    elif request.method == 'GET':
        flash(u'경고! 댓글이 완전히 삭제되니, 다시 한번 확인하시기 바랍니다.', 'warning')
        return render_template('comment/delete.html', comment_id=id)


@app.route('/comment/like/<int:id>', methods=['GET'])
def comment_like(id):
    comment = Ccomment.query.get(id)
    article_id = comment.article_id
    comment.like += 1

    db.session.commit()

    return redirect(url_for('article_detail', id=article_id))


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