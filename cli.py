# cli.py
import os

import click
import pyperclip

from database_manager.models import SQLAlchemyManager
from settings import FILE_DB
from utils.show import ShowUtils


def validate_user(ctx, param, value):
    """
    Check user exists
    """
    manager_obj = SQLAlchemyManager(ctx.obj['DB'], value)

    if not manager_obj.user_obj.check_user():
        print(f'ERROR: User named "{value}" not exists')
        exit(-1)
    elif 'PASSWORD' in ctx.obj.keys() \
            and not manager_obj.user_obj.check_user_password(ctx.obj['PASSWORD']):
        print(f'ERROR: Incorrect password for user named "{value}"')
        exit(-1)
    else:
        ctx.obj['USER'] = value
        return value


def validate_password(ctx, param, value):
    """
    Check password
    """
    if 'USER' not in ctx.obj.keys():
        ctx.obj['PASSWORD'] = value
        return value

    user = ctx.obj['USER']
    manager_obj = SQLAlchemyManager(ctx.obj['DB'], user)

    if not manager_obj.user_obj.check_user_password(value):
        print(f'ERROR: Incorrect password for user named "{user}"')
        exit(-1)
    else:
        return value


user_argument = click.option('--user', '-u', prompt="Username",
                             help="Provide your username",
                             callback=validate_user,
                             default=os.getlogin)
password_argument = click.option('--password', '-p', help="Provide your password",
                                 callback=validate_password,
                                 prompt=True, hide_input=True)


@click.group()
@click.option('-c/-not-category', help='print or not category')
@click.option('-u/-not-url', help='print or not url')
@click.option("--db", default=FILE_DB, required=False, hidden=True)
@click.pass_context
def cli(ctx, c, u, db):
    """
    pwdone is a multi-user, multi-platform command-line utility
    for storing and organizing passwords and another info for logins

    Samples:

    \b
    adding a new user:
    $ pwdone uadd
    or using options:
    $ pwdone uadd -u user-name

    \b
    adding a new record in passwords DB:
    $ pwdone add
    or using options:
    $ pwdone add -u user-name -l login-for-site -n record-name

    \b
    show all user records:
    $ pwdone show

    \b
    get the password of record to the clipboard:
    $ pwdone get

    \b
    full list of command options:
    $ pwdone [command] --help
    """
    ctx.obj = {
        'FLAGS': {
            'login': True,
            'name': True,
            'category': c,
            'url': u
        },
        'DB': db,
    }


@cli.command()
@click.option('--user', '-u', prompt="Username",
              help="Provide your username",
              default=os.getlogin)
@click.option('--password', '-p', help="Provide your password",
              prompt=True, hide_input=True)
@click.pass_context
def uadd(ctx, user, password):
    """
    add user command
    """
    manager_obj = SQLAlchemyManager(ctx.obj['DB'], user)

    if manager_obj.user_obj.check_user():
        print(f'ERROR: User named "{user}" already exists')
        exit(-1)
    else:
        manager_obj.user_obj.add_user(password)
        print(f'User named "{user}" created')


@cli.command()
@user_argument
@password_argument
@click.option('-nu', '--new-username',
              prompt="New username", help="Provide new username")
@click.option('-np', '--new-password',
              prompt="New password (Press 'Enter' for keep old password)",
              default='',
              help="Provide new password for user", hide_input=True)
@click.pass_context
def uupdate(ctx, user, password,
            new_username, new_password):
    """
    update username (and password) command
    """
    manager_obj = SQLAlchemyManager(ctx.obj['DB'], user)

    new_password = None if new_password == '' else new_password
    if manager_obj.user_obj.check_user(new_username) and not new_password:
        print(f'ERROR: User named "{new_username}" already exists '
              f'and no new password is given')
    else:
        manager_obj.user_obj.update_user(ctx.obj['DB'], password, new_username, new_password)


@cli.command()
@user_argument
@password_argument
@click.pass_context
def udelete(ctx, user, password):
    """
    delete user command
    """
    manager_obj = SQLAlchemyManager(ctx.obj['DB'], user)

    manager_obj.user_obj.del_user()
    print(f'User named "{user}" deleted')


@cli.command()
@click.pass_context
def ushow(ctx):
    """
    show users command
    """
    manager_obj = SQLAlchemyManager(ctx.obj['DB'])

    users = manager_obj.user_obj.all_users()
    for user in users:
        print(user)


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-n', "--name", prompt="Name", help='name', default='default')
@click.option('-pl', '--password-for-login', prompt=True,
              help="Provide password for login", hide_input=True)
@click.option('-c', "--category", help='"default" or skip for default category, optional',
              default=None, required=False)
@click.option('-ur', "--url", help='url, optional', default=None, required=False)
@click.pass_context
def add(ctx, user, password, login,
        password_for_login, category, url, name):
    """
    add login and password command
    """
    manager_obj = SQLAlchemyManager(ctx.obj['DB'], user)

    if manager_obj.unit_obj.check_login(login, name):
        print(f'login "{login}" with "{name}" name already exists')
    else:
        category = 'default' if category is None else category
        manager_obj.unit_obj\
            .add_unit(user, password, login, password_for_login, name, category, url)
        print(f'Login "{login}" added')


@cli.command()
@user_argument
@password_argument
@click.option('-c', "--category", help='"default" for default category, '
                                       'skip for all logins, optional',
              default=None, required=False)
@click.pass_context
def show(ctx, user, password, category):
    """
    show logins command
    """
    manager_obj = SQLAlchemyManager(ctx.obj['DB'], user)

    units = manager_obj.unit_obj.get_logins(category)
    units = ShowUtils.extend_fields(units)
    res_str = ShowUtils.make_str_units(units, ctx.obj['FLAGS'])
    print(res_str)


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-n', "--name", prompt="Name", help='name', default='default')
@click.pass_context
def get(ctx, user, password, login, name):
    """
    get password by login command
    """
    manager_obj = SQLAlchemyManager(ctx.obj['DB'], user)

    if manager_obj.unit_obj.check_login(login, name):
        pyperclip.copy(manager_obj.unit_obj
                       .get_password(user, password, login, name))
        print(f'Password is placed on the clipboard')
    else:
        print(f'login "{login}" with "{name}" name not exists')


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-n', "--name", prompt="Name", help='name', default='default')
@click.pass_context
def delete(ctx, user, password, login, name):
    """
    delete login and password command
    """
    manager_obj = SQLAlchemyManager(ctx.obj['DB'], user)

    if manager_obj.unit_obj.check_login(login, name):
        manager_obj.unit_obj.delete_unit(login, name)
        print(f'Login "{login}" deleted')
    else:
        print(f'login "{login}" with "{name}" name not exists')


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-n', "--name", prompt="Name", help='name', default='default')
@click.option('-nl', "--new-login", help='new login, optional',
              default=None, required=False)
@click.option('-nn', "--new-name", help='"default" or skip for old name, optional', required=False)
@click.option('-pl', '--password-for-login',
              prompt="New password for login (Press 'Enter' for keep old password)",
              default='',
              help="Provide new password for login", hide_input=True)
@click.option('-nc', "--new-category", help='"default" or skip for old category, optional',
              default=None, required=False)
@click.option('-ur', "--url", help='url, optional', default=None, required=False)
@click.pass_context
def update(ctx, user, password, login, name,
           new_login, new_name, password_for_login, new_category, url):
    """Update unit"""

    manager_obj = SQLAlchemyManager(ctx.obj['DB'], user)

    new_login = login if new_login is None else new_login

    if not manager_obj.unit_obj.check_login(login, name):
        print(f'login "{login}" with "{name}" name not exists')
    elif manager_obj.unit_obj.check_login(new_login, new_name) \
            and (login != new_login or name != new_name):
        print(f'login "{login}" with "{name}" name already exists')
    else:
        password_for_login = None if password_for_login == '' else password_for_login
        manager_obj.unit_obj\
            .update_unit(user, password, login, name,
                         new_login, password_for_login,
                         new_category, url, new_name)
        print(f'Login "{login}" updated')


if __name__ == '__main__':
    cli()
