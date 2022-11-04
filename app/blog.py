from flask import Blueprint, render_template, url_for
from flask_login import current_user, login_required
from app.models import Post, User

bp = Blueprint('blog', __name__)



@bp.route('/')
@bp.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', title='Home', posts=posts)

@bp.route("/profile/<int:id>")
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    image_file = url_for('static', filename="profile_pics/"+current_user.image_file)
    return render_template('profile.html', user=user, title='Profile', image_file=image_file)


