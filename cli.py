# cli.py
import os
import re
from logging import ERROR, INFO, WARNING

import click
import pyperclip

from database_manager.models import FILE_USERS_DB, SQLAlchemyManager
from log_manager.models import log_and_print
from settings import DB_ROOT
from units_manager.models import UnitsComposition


def get_os_username():
    if 'USERNAME' in os.environ and os.environ.get('USERNAME'):
        return os.environ.get('USERNAME')
    if 'USER' in os.environ and os.environ.get('USER'):
        return os.environ.get('USER')
    return None


def validate_new_user(ctx, param, value):
    """
    Check new user name
    """
    if not re.match('^[A-Za-z][A-Za-z0-9_]*$', value):
        log_and_print('The user name must consist of English letters, '
                      'numbers, and underscores. Start with a letter', level=ERROR)
        exit(-1)
    else:
        return value


def validate_user(ctx, param, value):
    """
    Check user exists
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, value)

    if not manager_obj.user_obj.check_user():
        log_and_print(f'User named "{value}" not exists', level=ERROR)
        exit(-1)
    else:
        ctx.obj['USER'] = value
        return value


def validate_password(ctx, param, value):
    """
    Check user exists
    """
    user = ctx.obj['USER']
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, value)

    if not manager_obj.user_obj.check_user_password(value):
        log_and_print(f'Incorrect password for user named "{user}"', level=ERROR)
        exit(-1)
    else:
        return value


def dangerous_warning(ctx, param, value):
    """Предупреждение об опасности команды uupdate"""
    log_and_print(f'The "uupdate" command is potentially dangerous.\n'
                  f'It is strongly recommended to make a backup '
                  f'of the "{DB_ROOT}" folder.', level=WARNING)
    return value


user_argument = click.option('--user', '-u', prompt="Username",
                             help="Provide your username",
                             callback=validate_user,
                             default=get_os_username)
password_argument = click.option('--password', '-p', help="Provide your password",
                                 callback=validate_password,
                                 prompt=True, hide_input=True)


@click.group()
# @click.option('-a/-not-alias', help='print or not alias')
@click.option('-c/-not-category', help='print or not category')
@click.option('-u/-not-url', help='print or not url')
@click.pass_context
def cli(ctx, c, u):
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
    $ pwdone add -u user-name -l login-for-site -a record-name

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
            'alias': True,
            'category': c,
            'url': u
        }
    }


@cli.command()
@click.option('--user', '-u', prompt="Username",
              help="Provide your username",
              callback=validate_new_user,
              default=get_os_username)
@click.option('--password', '-p', help="Provide your password",
              prompt=True, hide_input=True)
def uadd(user, password):
    """
    add user command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if manager_obj.user_obj.check_user():
        log_and_print(f'User named "{user}" already exists', level=ERROR)
        exit(-1)
    else:
        manager_obj.user_obj.add_user(password)
        log_and_print(f'User named "{user}" created', level=INFO)


@cli.command()
@user_argument
@password_argument
@click.option('-nu', '--new-username', prompt="New username",
              callback=validate_new_user, help="Provide new username")
@click.option('-np', '--new-password',
              prompt="New password (Press 'Enter' for keep old password)",
              default='old-password',
              help="New password 'old-password' for keep old password", hide_input=True)
@click.option('--dangerous-warning-option', callback=dangerous_warning, required=False)
@click.confirmation_option(prompt='Are you sure you want to update user data?')
def uupdate(user, password,
            new_username, new_password, dangerous_warning_option):
    """
    update username (and password) command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        log_and_print(f'User named "{user}" not exists', level=ERROR)
        return
    elif not manager_obj.user_obj.check_user_password(password):
        log_and_print(f'Incorrect password for user named "{user}"', level=ERROR)
        return

    if manager_obj.user_obj.check_user(new_username):
        log_and_print(f'User named "{new_username}" already exists', level=ERROR)
    else:
        manager_obj.user_obj.update_user(password, new_username, new_password)


@cli.command()
@user_argument
@password_argument
def udelete(user, password):
    """
    delete user command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        log_and_print(f'User named "{user}" not exists', level=ERROR)
        return
    elif not manager_obj.user_obj.check_user_password(password):
        log_and_print(f'Incorrect password for user named "{user}"', level=ERROR)
        return

    manager_obj.user_obj.del_user()
    log_and_print(f'User named "{user}" deleted', level=INFO)


@cli.command()
@click.pass_context
def ushow(ctx):
    """
    show users command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB)

    users = manager_obj.user_obj.all_users()
    for user in users:
        print(user)
    log_and_print(f'Show users command is done', print_need=False, level=INFO)


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
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        log_and_print(f'User named "{user}" not exists', level=ERROR)
        return
    elif not manager_obj.user_obj.check_user_password(password):
        log_and_print(f'Incorrect password for user named "{user}"', level=ERROR)
        return

    logins = manager_obj.unit_obj.get_logins(category)
    units_composition_obj = UnitsComposition(logins)
    units_composition_obj.prepare_data()
    res_str = units_composition_obj.make_str_logins(ctx.obj['FLAGS'])
    print(res_str)
    log_and_print(f'Show logins command is done', print_need=False, level=INFO)


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-a', "--alias", prompt="Alias", help='alias', default='default')
def get(user, password, login, alias):
    """
    get password by login command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        log_and_print(f'User named "{user}" not exists', level=ERROR)
        return
    elif not manager_obj.user_obj.check_user_password(password):
        log_and_print(f'Incorrect password for user named "{user}"', level=ERROR)
        return

    if manager_obj.unit_obj.check_login(login, alias):
        pyperclip.copy(manager_obj.unit_obj
                       .get_password(user, password, login, alias))
        log_and_print(f'Password is placed on the clipboard', level=INFO)
    else:
        log_and_print(f'login "{login}" with "{alias}"'
                      f' alias not exists', level=ERROR)


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-a', "--alias", prompt="Alias", help='alias', default='default')
def delete(user, password, login, alias):
    """
    delete login and password command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        log_and_print(f'User named "{user}" not exists', level=ERROR)
        return
    elif not manager_obj.user_obj.check_user_password(password):
        log_and_print(f'Incorrect password for user named "{user}"', level=ERROR)
        return

    if manager_obj.unit_obj.check_login(login, alias):
        manager_obj.unit_obj.delete_unit(login, alias)
        log_and_print(f'Login "{login}" deleted', level=INFO)
    else:
        log_and_print(f'login "{login}" with "{alias}"'
                      f' alias not exists', level=ERROR)


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-a', "--alias", prompt="Alias", help='alias', default='default')
@click.option('-pl', '--password-for-login', prompt=True,
              help="Provide password for login", hide_input=True)
@click.option('-c', "--category", help='"default" or skip for default category, optional',
              default=None, required=False)
@click.option('-ur', "--url", help='url, optional', default=None, required=False)
def add(user, password, login, password_for_login, category, url, alias):
    """
    add login and password command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        log_and_print(f'User named "{user}" not exists', level=ERROR)
        return
    elif not manager_obj.user_obj.check_user_password(password):
        log_and_print(f'Incorrect password for user named "{user}"', level=ERROR)
        return

    if manager_obj.unit_obj.check_login(login, alias):
        log_and_print(f'login "{login}" with "{alias}"'
                      f' alias already exists', level=ERROR)
    else:
        category = None if category == 'default' else category
        manager_obj.unit_obj\
            .add_unit(user, password, login, password_for_login, category, url, alias)
        log_and_print(f'Login "{login}" added', level=INFO)


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-a', "--alias", prompt="Alias", help='alias', default='default')
@click.option('-nl', "--new-login", help='new login, optional',
              default=None, required=False)
@click.option('-na', "--new-alias", prompt="New alias", help='alias', default='default')
@click.option('-pl', '--password-for-login',
              prompt="New password for login (Press 'Enter' for keep old password)",
              default='old-password',
              help="New password for login, "
                   "'old-password' for keep old password", hide_input=True)
@click.option('-nc', "--new-category", help='"default" or skip for default category, optional',
              default=None, required=False)
@click.option('-ur', "--url", help='url, optional', default=None, required=False)
def update(user, password, login, alias,
           new_login, new_alias, password_for_login, new_category, url):
    """Update unit"""

    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        log_and_print(f'User named "{user}" not exists', level=ERROR)
        return
    elif not manager_obj.user_obj.check_user_password(password):
        log_and_print(f'Incorrect password for user named "{user}"', level=ERROR)
        return

    new_login = login if new_login is None else new_login

    if not manager_obj.unit_obj.check_login(login, alias):
        log_and_print(f'login "{login}" with "{alias}"'
                      f' alias not exists', level=ERROR)
    elif manager_obj.unit_obj.check_login(new_login, new_alias) \
            and (login != new_login or alias != new_alias):
        log_and_print(f'login "{login}" with "{alias}"'
                      f' alias already exists', level=ERROR)
    else:
        new_category = None if new_category == 'default' else new_category
        manager_obj.unit_obj\
            .update_unit(user, password,
                         login, new_login, password_for_login,
                         new_category, url, alias, new_alias)
        log_and_print(f'Login "{login}" updated', level=INFO)


if __name__ == '__main__':
    cli()
