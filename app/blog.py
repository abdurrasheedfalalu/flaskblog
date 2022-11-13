from datetime import datetime
import os
from pathlib import Path
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models import Post, User, db
from app.forms import EditPostForm, EditProfileForm, EmptyForm, NewPost

from app.utils import save_picture

bp = Blueprint('blog', __name__)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@bp.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('blog/explore.html', title='Explore', posts=posts)

@bp.route("/profile/<int:id>", methods=['POST', 'GET'])
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

            if current_user.image_file != 'vector.jpg':
                #Remove an after upload new one
                os.remove(os.path.join(current_app.root_path, "static/profile_pics", current_user.image_file))
                # image = Path() / current_app.root_path / "static/profile_pics" / current_user.image_file
                # print(image)
                # image.unlink()

            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('blog.profile', id=current_user.id))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
    return render_template("blog/edit_pro.html", title='Edit Profile', legend='Edit', form=form)


@bp.route('/new post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added successfully.', 'success')
        return redirect(url_for('home'))
    return render_template('blog/new_post.html', title='New Post', legend='New Post', form=form)



@bp.route('/follow/<int:id>', methods=['POST'])
@login_required
def follow(id):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=id).first()
        if user:
            current_user.follow(user)
            db.session.commit()
            flash(f'You are following user {user.username} Now.', 'success')
            return redirect(url_for('home'))
    print(form.errors)



@bp.route('/unfollow/<int:id>', methods=['POST'])
@login_required
def unfollow(id):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=id).first()
        if current_user.is_following(user):
            current_user.unfollow(user)
            db.session.commit()
            flash(f'You are unfollowing user {user.username} Now.', 'success')
            return redirect(url_for('home'))
    print(form.errors)


@bp.route('/post/<int:id>/update', methods=['POST', 'GET'])
def edit_post(id):
    post = Post.query.get_or_404(id) 
    form = EditPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('You post has been updated.', 'success')
        return redirect(url_for('blog.profile', id=current_user.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('blog/edit_post.html', form=form, title='Edit Post', legend='Edit Post')


@bp.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post is not None:
        db.session.delete(post)
        db.session.commit()
        flash('Your Post has been deleted.', 'danger')
        return redirect(url_for('blog.profile', id=current_user.id))