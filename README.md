# FlaskWebPractice

## init db
*$ python manage db init<br />*
*$ python manage db migrate<br />*
*$ python manage db upgrade<br />*

## insert role
*$ python manage shell<br />*
*> from app.models import Role<br />*
*> Role.insert_roles()<br />*

## start server
*$ python manage runserver --host 0.0.0.0*
