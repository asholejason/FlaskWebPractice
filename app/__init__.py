from flask import Flask
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# app
app = Flask(__name__)
app.config.from_object('config')

# manager
manager = Manager(app)

# bootstrap
bootstrap = Bootstrap(app)

# local time
moment = Moment(app)

# db
db = SQLAlchemy(app)

# mail
mail = Mail(app)

from app import views, models
