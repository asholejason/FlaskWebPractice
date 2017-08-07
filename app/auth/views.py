from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ResetPasswordForm
from app import db
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Invalid username or password.")
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email('1009772684@qq.com',
                   'Confirm Your Account',
                   'auth/email/confirm',
                   user=user,
                   token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email('1009772684@qq.com',
               'Confirm Your Account',
               'auth/email/confirm',
               user=current_user,
               token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():
    user = current_user
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if user.verify_password(form.password.data):
            user.password = form.password1.data
            db.session.add(user)
            db.session.commit()
        flash("Your Password have been change successful")
        return redirect(url_for('main.index'))
    return render_template('auth/changepassword.html', form=form)


@auth.route('/resetpassword')
@login_required
def reset_password():
    user = current_user
    token = user.generate_confirmation_token()
    send_email('1009772684@qq.com',
               'Reset Your Password',
               'auth/email/resetpassword',
               user=user,
               token=token)
    flash('A password reset email has been send to your inbox')
    return redirect(url_for('main.index'))


@auth.route('/resetpassword/<token>', methods=['GET', 'POST'])
@login_required
def resetpassword(token):
    user = current_user
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password1.data
        db.session.add(user)
        db.session.commit()
        flash("Reset password successful")
        return redirect(url_for('main.index'))
    return render_template('auth/resetpassword.html', form=form)
