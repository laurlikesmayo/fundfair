from flask import Flask, render_template
from views import views

app = Flask(__name__)

app.register_blueprint(views, url_prefix='/admin')

@app.route('/')
def test():
    return "<h1>Test<h1>"

if __name__ == "__main__":
    app.run(debug =True)

#pull