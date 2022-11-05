from datetime import datetime
from hashlib import md5
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String, default='vector.jpg')
    about = db.Column(db.String, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def generate_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password_hash(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_online(self):
        pass


    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Post {self.title}, {self.date_posted}>"