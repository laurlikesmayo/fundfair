from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()

def createapp():

    #configurations of the app, setting up database and initialising
    app = Flask(__name__)
    app.config['SECRET_KEY']='hello'
    app.config['SQLAlchemy_DATABASE_URI']='aqlite:///database.db'
    app.config['SQLAlchemy_TRACK_MODIFICATIONS']= False
    db.init_app(app)
    loginmanager = LoginManager(app)
    loginmanager.login_view = '/'


    #gets all the website routes from views.py
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    #gets the user information from the database 
    from .models import Users
    createdatabase(app)

    #gets the id of the user and filters it
    @loginmanager.user_loader
    def userloader(id):
        return Users.query.filter_by(int(id)).first()



     
    #returning the app 
    return app

 
 
 
 
#creating a database for the website if its not created
def createdatabase(app):
    if not path.exists("website/database.db"):
        db.create_all(app = app)
        print("created")


