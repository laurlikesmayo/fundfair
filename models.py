from . import db
from flask_login import UserMixin

#puts all the users information into the database
class Users(db.Model, UserMixin):
    _id = db.Column("id", db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, name, email):
        self.name = name
        self.email = email