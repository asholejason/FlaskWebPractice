from datetime import datetime
from flask import render_template, session
from . import main
from ..models import User
from flask_login import login_required


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           name=session.get('name'),
                           current_time=datetime.utcnow(),
                           known=session.get('known'))


@main.route('/user', methods=['GET', 'POST'])
def user():
    users = User.query.all()
    return render_template('user.html', users=users)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/secret')
@login_required
def secret():
    return "Only authenticated users are allowed!"
