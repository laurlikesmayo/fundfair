from flask import Flask, render_template, url_for, redirect

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY']='hello'
app.config['SQLALCHEMY_DATABASE_URI']='aqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

loginmanager = LoginManager(app)

loginmanager.login_view = '/'

def createdatabase(app):
    if not path.exists("website/database.db"):
        db.create_all(app=app)
        print("created")

from .models import Users
createdatabase(app)



@app.route('/')
def home(): 
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/explore')
def explore():
    return render_template('explore.html ')



if __name__ == '__main__':
    app.run(debug = True)