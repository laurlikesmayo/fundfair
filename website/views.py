from flask import Flask, Blueprint, render_template, request, url_for, redirect, session, flash
from .models import Users
from .models import Posts
from datetime import timedelta, datetime
<<<<<<< Updated upstream
from flask_login import login_user, logout_user, login_required 
from . import db
from werkzeug.security import generate_password_hash, check_password_hash 
import smtplib
=======
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from . import db, app
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
import smtplib, ssl
from email.message import EmailMessage
from werkzeug.utils import secure_filename
import uuid as uuid
import os

>>>>>>> Stashed changes
#module that hashes the password out
#//meaning will not store the actual password in database and will store value

views = Blueprint("views", __name__)

# , static_folder = 'static', templates_folder = 'templates'

<<<<<<< Updated upstream
=======
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    image = FileField("Image")
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    searched=StringField("Searched", validators=[DataRequired()])
>>>>>>> Stashed changes



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
    if current_user.is_authenticated:
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
<<<<<<< Updated upstream
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

        return redirect(url_for('views.home'))

    return render_template("create.html")
=======
    if not 'loggedin' in session:
        flash('You have not been logged in!')
        return redirect(url_for('views.login'))
    form = PostForm()
    poster=current_user.id
 
    if form.validate_on_submit():
                    
            title = form.title.data
            content = form.content.data
            image = form.image.data
             

            pic = secure_filename(image.filename)
            # pic_name = str(uuid.uuid1()) + "_" + pic
            # #save the image
            # saver = form.image.data
            # saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name)) 
            # image = pic_name
            post = Posts(title=title, content=content, poster_id=poster, image=pic)
            db.session.add(post)
            db.session.commit()
            flash("Post has been updated.")
            return redirect(url_for("views.post", id=post.id))
        
        
    else:
        return render_template("create.html", form=form)
>>>>>>> Stashed changes


@login_required
@views.route('/post')
def posts():
    posts = Posts.query.order_by(Posts.date_added)

<<<<<<< Updated upstream
    return render_template("posts.html", posts=posts)
=======
@login_required
@views.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    if not 'loggedin' in session:
        flash('You have not been logged in!')
        return redirect(url_for('views.login'))
    post = Posts.query.get_or_404(id)
    form = PostForm()
    id=current_user.id
    if id==post.poster.id:
        if form.validate_on_submit():
                    
            post.title = form.title.data
            post.content = form.content.data
            post.image = form.image.data

            db.session.add(post)
            db.session.commit()
            flash("Post has been updated.")
            return redirect(url_for("views.post", id=post.id))
        
        form.title.data = post.title
        form.image.data = post.image
        form.content.data=post.content
        return render_template('edit_post.html', form=form)
    else:
        flash('You are not allowed to edit this post!')
        return redirect(url_for('views.posts'))

@login_required
@views.route('post/delete/<int:id>')
def delete_post(id):\
    
    posts = Posts.query.order_by(Posts.date_added)
    if not 'loggedin' in session:
        flash('You have not been logged in!')
        return redirect(url_for('views.login'))
    post_to_del = Posts.query.get_or_404(id)
    id = current_user.id 
    postid=post_to_del.id
    
    if id == post_to_del.poster.id:

        try:
            
            
            
            signups = SignUps.query.filter_by(post_id=postid).all()
            for i in signups:

                db.session.delete(i)
            db.session.delete(post_to_del)
            db.session.commit()
            flash('Post successfully deleted')
            return render_template("posts.html", posts=posts)
            
        except:
            flash('There was an error. Please try again.')
            return redirect(url_for('views.posts'))
    else:
        flash('You are not allowed to delete this post!')
        return redirect(url_for('views.posts'))
@login_required
@views.route('/account')
def account():
    if not 'loggedin' in session:
        flash('You have not been logged in!')
        return redirect(url_for('views.login'))
    id = current_user.id
    user=Users.query.get_or_404(id)
    return render_template('account.html', user=user)

@views.route('/search', methods=["POST"])
def search():
    print('search')
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts= posts.order_by(Posts.title).all()
        return render_template("search.html", form=form, searched=post.searched, posts=posts)

@login_required
@views.route('/post/signupform/<id>', methods = ['GET', 'POST'])
def signupform(id):
    if not 'loggedin' in session:
        flash('You have not been logged in!')
        return redirect(url_for('views.login'))
    form = SignUpForm()
    post= Posts.query.filter_by(id=id).first()
    currentid = current_user.id
    signup = SignUps.query.filter_by(author=currentid, post_id=id).first()
    if signup:
        db.session.delete(signup)
        db.session.commit()
        return render_template("post.html", post=post, signedup=True)
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            user = Users.query.filter_by(email=email).first()
            
            if user:
                port=465
                smtp_server = 'smtp.gmail.com'
                sender_email="myfundfair@gmail.com"
                password="imqvedmyhobaafgn"
                reciever_email= post.poster.email
                subject = "Someone signed up for your event!"
                subject2 = "You have signed up for this event!"
                message=f"""
                You have a sign up for your event!
                name: {name}
                email: {email}

                Goodluck for running your chairty!

                Fundfair.co
                """
                message2=f"""
                Hi {name},
                You have signed up for this event!:
                {post.title}

                have a nice life
                
                """
                em = EmailMessage()
                em['From'] = sender_email
                em['To'] = reciever_email
                em['subject'] = subject
                em.set_content(message)

                em2 = EmailMessage()
                em2['From'] = sender_email
                em2['To'] = email
                em2['subject'] = subject2
                em2.set_content(message2) 
                
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, reciever_email, em.as_string())
                    server.sendmail(sender_email, email, em2.as_string())
                flash("Sign up successful!")
                return redirect(url_for('views.signup', post_id=post.id))
            else:
                flash('User does not exist')
    return render_template('signupform.html', form=form)




@login_required
@views.route('/post/signup/<post_id>', methods=["GET", "POST"])
def signup(post_id):
    id=current_user.id
    signup=SignUps(author = id, post_id=post_id)
    db.session.add(signup)
    db.session.commit()
    if not 'loggedin' in session:
        flash('You have not been logged in!')
        return redirect(url_for('views.login'))

    return redirect(url_for('views.post', id=post_id))


@login_required
@views.route('/signedupposts')
def signeddupposts():
    if not 'loggedin' in session:
        flash('You have not been logged in!')
        return redirect(url_for('views.login'))
    id = current_user.id
    signups = SignUps.query.filter_by(author=id).all()
    posts=[]
    for sign_up in signups:
        postid=sign_up.post_id
        post = Posts.query.filter_by(id=postid).first()
        if not post:
            pass
        else:
            posts.append(post)
    
    
    return render_template('signedupposts.html', posts=posts)

@views.route('/dangerous')
def dangerous():
    signups = SignUps.query
    posts= Posts.query
    users = Users.query
    for i in signups:
        db.session.delete(i)
    
    for i in posts:
        db.session.delete(i)

    for i in users:
        db.session.delete(i)
    
    db.session.commit()
    return render_template('dangerous.html')


@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
>>>>>>> Stashed changes
