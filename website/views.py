from flask import Flask, Blueprint, render_template, request, url_for, redirect, session, flash
from .models import Users
from .models import Posts
from datetime import timedelta, datetime
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

#module that hashes the password out
#//meaning will not store the actual password in database and will store value

views = Blueprint("views", __name__)

# , static_folder = 'static', templates_folder = 'templates'

class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = StringField('Content', validators=[DataRequired()])
	
	author = StringField("Author")
	slug = StringField("Slug", validators=[DataRequired()])
	submit = SubmitField("Submit")

#app routes

@views.route('/login',  methods=['GET', 'POST'] )
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

@views.route('/register',  methods=['GET', 'POST'] )
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
        post = Posts(title=title, content=content, author=author, slug=slug)

        db.session.add(post)
        db.session.commit()

        flash('Event created sucessfully')
        print('post sucessful')

        return redirect(url_for('views.posts'))

    return render_template("create.html")

@views.route('/post/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@login_required
@views.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_added)
    return render_template("posts.html", posts=posts)

@views.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
                
        post.title = form.title.data
        post.content = form.content.data
        post.author =form.author.data
        post.slug = form.slug.data

        db.session.add(post)
        db.session.commit()
        flash("Post has been updated.")
        return redirect(url_for("views.post", id=post.id))
    
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data=post.content
    return render_template('edit_post.html', form=form)

@views.route('post/delete/<int:id>')
def delete_post(id):
    post_to_del = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_del)
        db.session.commit()
        flash('Blog post was deleted')
        posts = Posts.query.order_by(Posts.date_added)
        return render_template("posts.html", posts=posts)
    except:
        flash('There was an error. Please try again.')
        return redirect(url_for('views.posts'))

@views.route('/account')
def account():
    id = current_user.id
    user=Users.query.get_or_404(id)
    return render_template('account.html', user=user)
@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404