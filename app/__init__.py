from flask import Flask, render_template
from flask_login import current_user, login_required
from flask_migrate import Migrate
from flask_mail import Mail

from app.blog import bp
from app.errors import error
from app.auth import auth, login_manager
from app.models import Post, User, db, bcrypt
from config import Config

mail = Mail()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate = Migrate(app, db)


    @app.route('/')
    @app.route('/home')
    @login_required
    def home():
        posts = current_user.followed_posts().all()
        return render_template('home.html', posts=posts)

    if test_config:
        app.config.from_mapping(test_config)

    #Register extentions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    #Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(bp)
    app.register_blueprint(error)


    @app.shell_context_processor
    def make_context():
        return{'db': db, 'User': User, 'Post': Post}





    return app

