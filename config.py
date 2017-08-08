import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 'ao%$%^xghy5uabzpyo1fo=5jlb6btw8i%nmf1&+fpe-zfnr+_+'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # page
    FLASKY_POSTS_PER_PAGE = 5
    FLASKY_USERS_PER_PAGE = 10
    # follow
    FLASKY_FOLLOWERS_PER_PAGE = 5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASEDIR, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASEDIR, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASEDIR, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
