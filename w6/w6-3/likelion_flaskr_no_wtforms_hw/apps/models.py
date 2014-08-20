"""
models.py

"""
from apps import db

class Aarticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    author = db.Column(db.String(255))
    category = db.Column(db.String(255))
    like = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime())

class Ccomment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship('Aarticle', backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    like = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime())