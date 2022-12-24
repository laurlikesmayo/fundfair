from flask import Flask, Blueprint, render_template, request, url_for, redirect, session, flash
from .models import Users
from .models import Posts
from datetime import timedelta, datetime
from flask_login import login_user, logout_user, login_required 
from . import db
from werkzeug.security import generate_password_hash, check_password_hash 
import smtplib
#module that hashes the password out
#//meaning will not store the actual password in database and will store value

views = Blueprint("views", __name__)

# , static_folder = 'static', templates_folder = 'templates'




#app routes

@views.route('login',  methods=['GET', 'POST'] )
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        permanentsesh =request.form.get('permanentsession')
        user = Users.query.filter_by(username=username).first() #Users is database with all the users
       #the line above will create a new child in the class User
       #stores as first because usernames are unique and will always be the first option
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=user.email)
                print('Logged in')
                if permanentsesh:
                    session.permanent = True
                else:
                    session.permanent = False
                session['loggedin'] = True
                session['email'] = user.email
                flash('Log in sucessful', 'info ')
                return redirect(url_for('views.home')) 
            else:
                print('Wrong Password')
        else:
            print('Username does not exist')
                
                
    return render_template("login.html")

@views.route('register',  methods=['GET', 'POST'] )
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        username_exists = Users.query.filter_by(username = username).first()
        email_exists = Users.query.filter_by(email = email).first()
        if password1 != password2:
            print("Passwords don't match!")
        elif username_exists or email_exists:
            print('username or email already exists!')
        elif len(password1) < 6 or len(username) <6:
            print("Username or password must contain more than 6 characters")
        else:
            new_user = Users(username = username, email=email, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            session['loggedin'] = True
            flash('sign up sucessful', 'info')
            return redirect(url_for('views.home'))


    return render_template("register.html")


@login_required
@views.route('/')
def home():
    if 'loggedin' in session:

        return render_template("home.html")
    else:
        return redirect(url_for('views.login'))

@login_required
@views.route('/logout')
def logout():
    logout_user()
    session.pop('loggedin', None)
    return redirect(url_for('views.login'))


@login_required
@views.route('/create', methods = ['GET', "POST"])
def create(): 
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get('content')
        author = request.form.get('author')
        slug = request.form.get('slug')
        dateadded=datetime.utcnow
        post = Posts(title=title, content=content, author=author, slug=slug)

        db.session.add(post)
        db.session.commit()

        flash('Event created sucessfully')
        print('post sucessful')

        return redirect(url_for('views.home'))

    return render_template("create.html")


@login_required
@views.route('/post')
def posts():
    posts = Posts.query.order_by(Posts.date_added)

    return render_template("posts.html", posts=posts)