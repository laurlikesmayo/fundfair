from . import db
from flask_login import UserMixin

#puts all the users information into the database
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))

