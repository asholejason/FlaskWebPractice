from datetime import datetime
from flask import render_template, session, abort, redirect, flash, url_for, request, current_app
from . import main
from ..models import User, Role, Permission, Post
from flask_login import login_required, current_user
from .forms import EditProfileForm, EditProfileAdminForm, DeleteUserForm, PostForm
from app import db
from app.decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           name=session.get('name'),
                           current_time=datetime.utcnow(),
                           known=session.get('known'))


@main.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    users = User.query.all()
    return render_template('userinfo.html', users=users)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/secret')
@login_required
def secret():
    return "Only authenticated users are allowed!"


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    form = DeleteUserForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.delete(user)
        db.session.commit()
        flash('The User has been deleted.')
        return redirect(url_for('main.userinfo'))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('delete_user.html', form=form, user=user)


@main.route('/', methods=['GET', 'POST'])
@login_required
def post(id):
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all
    return render_template('index.html', form=form, posts=posts)