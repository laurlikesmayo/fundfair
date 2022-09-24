from . import db
from flask_login import UserMixin

#puts all the users information into the database
class Users(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    # def __init__(self, username, email, password, id):
    #     self.username = username
    #     self.email = email
    #     self.password = password
    #     self.id = id