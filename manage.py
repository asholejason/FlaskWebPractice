from app import manager, db, app
from app.models import User, Role
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

#  manage shell
manager.add_command("shell", Shell(make_context=make_shell_context))

# manage db
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0')
    manager.run()
