from flask import Flask, render_template

from app.auth import auth
from app.models import db, bcrypt
from config import Config

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(auth)


    posts = [
        {
            'author': 'Abdurrasheed',
            'title': 'First Post',
            'content': 'First Post Content',
            'date_posted': '31-02-2004'
        },
        {
            'author': 'Abba',
            'title': 'First Post',
            'content': 'First Post Content',
            'date_posted': '31-02-2004'
        }
    ]

    @app.route('/')
    @app.route('/home')
    def home():
        user = {'name': 'Abba'}
        return render_template('home.html', title='Home', user=user, posts=posts)





    return app

