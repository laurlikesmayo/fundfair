from flask import Blueprint, render_template, request
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash #this imports the module that hashes out the password

views = Blueprint("views", __name__)




#app routes
@views.route('/')
def home(): 
    return render_template('home.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/explore')
def explore():
    return render_template('explore.html')

@views.route('login',  methods=['GET', 'POST'] )
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first() #Users is database with all the users
        if user:
            pass
    return render_template("login.html")

@views.route('register',  methods=['GET', 'POST'] )
def register():
    if request.method == "POST":
        pass

    return render_template("register.html")
