import os
import secrets
from datetime import datetime
from PIL import Image
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models import Post, User, db
from app.forms import EditProfileForm

bp = Blueprint('blog', __name__)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    
    return picture_fn


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
    image_file = url_for('static', filename="profile_pics/"+user.image_file)
    return render_template('profile.html', user=user, title='Profile', image_file=image_file)


@bp.route("/profile/<int:id>/update", methods=['POST', 'GET'])
def profile_update(id):
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('blog.profile', id=current_user.id))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
    return render_template("edit_pro.html", title=f'Edit Profile{id}', legend='Edit', form=form)