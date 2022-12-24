from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from os import path
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def createapp():

    #configurations of the app, setting up database and initialising
    app.secret_key = 'hello'
    app.permanent_session_lifetime = timedelta(days = 5)

    app.config['SECRET_KEY']='hello'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
    db.init_app(app)
    loginmanager = LoginManager(app)
    loginmanager.login_view = '/'


    #gets all the website routes from views.py
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    #gets the user information from the database 
    from .models import Users
    from .models import Posts
    createdatabase(app)

    #gets the id of the user and filters it
    @loginmanager.user_loader
    def userloader(id):
        return Users.query.filter_by(id=int(id)).first()



     
    #returning the app 
    return app

 
 
 
 
#creating a database for the website if its not created
def createdatabase(app):
    if not path.exists("website/database.db"):
        db.create_all(app = app)
        print("created")

