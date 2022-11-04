from flask import Flask
from flask_migrate import Migrate

from app.blog import bp
from app.auth import auth, login_manager
from app.models import Post, User, db, bcrypt
from config import Config

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate = Migrate(app, db)

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(bp)


    @app.shell_context_processor
    def make_context():
        return{'db': db, 'User': User, 'Post': Post}





    return app

