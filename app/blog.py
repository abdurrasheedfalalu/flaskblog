from datetime import datetime
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models import Post, User, db
from app.forms import EditProfileForm, EmptyForm, NewPost

from app.utils import save_picture

bp = Blueprint('blog', __name__)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@bp.route('/')
@bp.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    return render_template('blog/posts.html', title='Home', posts=posts)

@bp.route("/profile/<int:id>")
@login_required
def profile(id):
    form = EmptyForm()
    user = User.query.get_or_404(id)
    image_file = url_for('static', filename="profile_pics/"+user.image_file)
    return render_template('blog/profile.html', user=user, title='Profile', image_file=image_file, form=form)


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
    return render_template("blog/edit_pro.html", title=f'Edit Profile{id}', legend='Edit', form=form)


@bp.route('/new post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added successfully.', 'success')
        return redirect(url_for('blog.posts'))
    return render_template('blog/new_post.html', title='New Post', legend='New Post', form=form)










# @bp.route('/follow/<username>', methods=['POST'])
# @login_required
# def follow(username):
#     form = EmptyForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=username).first()
#         if user is None:
#             flash(f'User {username} Not Found!')
#             return redirect(url_for('blog.home'))
#         if user == current_user:
#             flash('You can`t follow yourself!')
#             return redirect(url_for('blog.profile', id=user.id))
#         current_user.follow(user)
#         db.session.commit()
#         flash(f'You are following user {username}')
#         return redirect(url_for('blog.profile', id=user.id))
