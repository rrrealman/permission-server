
import functools
from flask import current_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy.exc import IntegrityError
from app import app, RoleModel
from errors import NoUserFound, NoRoleFound
from utils import app_context, grant_role, withdraw_role


manager = Manager(app)
migrate = Migrate(
    app=app,
    db=app.db)


manager.add_command('db', MigrateCommand)
manager.help_args = ('-?', '--help')


def check_user_and_role_exist(command_func):

    @functools.wraps(command_func)
    def wrapper(*args, **kwargs):
        try:
            return command_func(*args, **kwargs)
        except NoUserFound as e:
            print(f'No user found: {e.user_name}')
        except NoRoleFound as e:
            print(f'No role found: {e.role_name}')
    return wrapper


def process_integrity_error(message):

    def outer(command_func):

        @functools.wraps(command_func)
        def inner(*args, **kwargs):
            try:
                return command_func(*args, **kwargs)
            except IntegrityError:
                print(message)

        return inner
    return outer


@manager.command
@app_context
@process_integrity_error('One or more roles has already been installed')
def install_roles():

    'Install predefined roles list'

    roles = (
        'Notifications',
        'Money',
        'SDuser',
        'requestCard')

    role_models = [RoleModel(role_name=role_name) for role_name in roles]
    current_app.db.session.bulk_save_objects(role_models)
    current_app.db.session.commit()
    for role_name in roles:
        print(f'Role {role_name} installed')


@manager.option(
    '-u', dest='user_name', help='Name of user whom role is adding to',
    required=True)
@manager.option('-r', dest='role_name', help='Role name', required=True)
@check_user_and_role_exist
@process_integrity_error('Role has already been granted')
@app_context
def grant_role_command(user_name, role_name):

    'Grant role to user'

    grant_role(user_name, role_name)
    print(f'Role {role_name} added successfully to user {user_name}')


@manager.option(
    '-u', dest='user_name', help='Name of user whom role is withdrawing from',
    required=True)
@manager.option('-r', dest='role_name', help='Role name', required=True)
@check_user_and_role_exist
@app_context
def withdraw_role_command(user_name, role_name):

    'Withdraw role from user'

    withdraw_role(user_name, role_name)
    print(f'Role {role_name} withdrawn successfully from user {user_name}')


if __name__ == '__main__':
    manager.run()
