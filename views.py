from flask import Blueprint, render_template

views = Blueprint('views', __name__, static_folder = "static", template_folder = "template")

@views.route('/home')
@views.route('/')
def home():
    return render_template('home.html')