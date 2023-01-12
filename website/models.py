from . import db
from flask_login import UserMixin
from flask_migrate import Migrate
from datetime import datetime

#puts all the users information into the database
class Users(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key = True)
    name= db.Column("name", db.String(255), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(50), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    posts = db.relationship('Posts', backref='poster')
    sign_ups = db.relationship('SignUps', backref='signupper')

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True) #gives the post a unique id
    title = db.Column(db.String(255))
    content = db.Column(db.Text(1000))#not a string but text cuz it a lot bigger
    #author = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id')) #lowercase u bc in database its lowercase cuz its dumb
    sign_ups = db.relationship('SignUps', backref = 'post')


class SignUps(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    post_id= db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)