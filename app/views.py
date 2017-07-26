from app import app, db, mail
from flask import render_template, session, redirect, url_for, flash
from datetime import datetime
from app.forms import NameForm
from app.models import User, Role
from flask_mail import Message


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.body = template
    mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            send_mail(app.config['FLASKY_ADMIN'], 'test', 'hello', user=user)
        else:
            session['known'] = True

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           current_time=datetime.utcnow(),
                           known=session.get('known'))


@app.route('/user/', methods=['GET', 'POST'])
def user():
    form = NameForm()
    return render_template('user.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
