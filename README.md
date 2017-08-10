# FlaskWebPractice

## 1.init db
*$ python manage db init<br />*
*$ python manage db migrate<br />*
*$ python manage db upgrade<br />*

## 2.insert role
*$ python manage shell<br />*
>\> from app.models import Role<br />
>\> Role.insert_roles()<br />

## 3.start server
*$ python manage runserver --host 0.0.0.0*
