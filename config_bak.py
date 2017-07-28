import os

# form deepend
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# sqlalchemy
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

# mail
MAIL_SERVER = 'smtp.126.com'
MAIL_PORT = 25
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER')
FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
