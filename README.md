# FlaskWebPractice

## init db
$ python manage db init
$ python manage db migrate
$ python manage db upgrade

# insert role
python manage shell
from app.models import Role
Role.insert_roles()

## start server
python manage runserver --host 0.0.0.0
