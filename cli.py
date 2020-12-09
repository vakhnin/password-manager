# cli.py
import os
from logging import INFO, WARNING, ERROR

import click
import pyperclip

from database_manager.models import FILE_USERS_DB, SQLAlchemyManager
from log_manager.models import log_and_print


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


user_argument = click.option('--user', '-u', prompt="Username",
                             help="Provide your username",
                             callback=validate_user,
                             default=lambda: os.environ.get('USERNAME'))
password_argument = click.option('--password', '-p', help="Provide your password",
                                 callback=validate_password,
                                 prompt=True, hide_input=True)


@click.group()
@click.option('-a/-not-alias', help='print or not alias')
@click.option('-c/-not-category', help='print or not category')
@click.option('-u/-not-url', help='print or not url')
@click.pass_context
def cli(ctx, a, c, u):
    """
    Use "pwdone [COMMAND] --help" for more information
    """
    ctx.obj = {
        'FLAGS': {
            'alias': a,
            'category': c,
            'url': u
        }
    }


@cli.command()
@click.option('--user', '-u', prompt="Username",
              help="Provide your username",
              default=lambda: os.environ.get('USERNAME'))
@click.option('--password', '-p', help="Provide your password",
              prompt=True, hide_input=True)
def uadd(user, password):
    """
    add user command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if manager_obj.user_obj.check_user():
        log_and_print(f'User named "{user}" already exists', level=ERROR)
    else:
        manager_obj.user_obj.add_user(password)
        log_and_print(f'User named "{user}" created', level=INFO)


@cli.command()
@user_argument
@password_argument
@click.option('-l', '--newusername', prompt="NewUsername", help="Provide new username")
@click.option('-pl', '--password-for-newusername', prompt=False, hide_input=True)
def uupdate(user, password, newusername, password_for_newusername):
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

    if manager_obj.user_obj.check_user(newusername):
        log_and_print(f'User named "{newusername}" already exists', level=ERROR)
    else:
        manager_obj.user_obj.update_user(password, newusername, password_for_newusername)


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
    log_and_print("Это сообщение попадает и в лог и выводится на экран")
    log_and_print("Это сообщение попадает в лог, на экран не выводится",
                  print_need=False)
    log_and_print("Это сообщение попадает и в лог с "
                  "пометкой WARNING и выводится на экран", level=WARNING)

    users = manager_obj.user_obj.all_users()
    for user in users:
        print(user)


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

    def prepare_logins(logins_):
        """Подготовка списка логинов"""
        for key, lst in logins_.items():
            # Ищем максимальную длину строки в столбце
            max_len = len(key)
            for item in lst:
                if len(item) > max_len:
                    max_len = len(item)

            # Добавляем пробелы в столбцы, для одинаковой длины столбцов
            for i in range(len(lst)):
                logins_[key][i] = logins_[key][i].ljust(max_len+1)
            logins_[key].insert(0, key.ljust(max_len+1))

        return logins_

    def print_logins(logins_, flags):
        """Печатем логины с флагами"""
        is_first_line = True
        for i in range(len(logins_['logins'])):
            str_for_print = logins_['logins'][i]
            delimiter_str = "-" * len(logins_['logins'][i])
            for key in logins_.keys():
                if key in flags.keys() and flags[key]:
                    str_for_print += '| ' + logins_[key][i]
                    delimiter_str += '+-' + '-' * len(logins_[key][i])
            print(str_for_print)
            if is_first_line:
                print(delimiter_str)
                is_first_line = False

    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        print(f'Error: User named "{user}" not exists')
        return
    elif not manager_obj.user_obj.check_user_password(password):
        print(f'Error: incorrect password for user named "{user}"')
        return

    logins = manager_obj.unit_obj.get_logins(category)
    logins = prepare_logins(logins)
    print_logins(logins, ctx.obj['FLAGS'])


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
def get(user, password, login):
    """
    get password by login command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        print(f'Error: User named "{user}" not exists')
        return
    elif not manager_obj.user_obj.check_user_password(password):
        print(f'Error: incorrect password for user named "{user}"')
        return

    if manager_obj.unit_obj.check_login(login):
        pyperclip.copy(manager_obj.unit_obj.get_password(user, password, login))
        print(f'Password is placed on the clipboard')
    else:
        print(f'Error: login "{login}" not exists')


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
def delete(user, password, login):
    """
    delete login and password command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        print(f'Error: User named "{user}" not exists')
        return
    elif not manager_obj.user_obj.check_user_password(password):
        print(f'Error: incorrect password for user named "{user}"')
        return

    if manager_obj.unit_obj.check_login(login):
        manager_obj.unit_obj.delete_unit(login)
        print(f' login "{login}" deleted')
    else:
        print(f'Error: login "{login}" not exists')


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-pl', '--password-for-login', prompt=True,
              help="Provide password for login", hide_input=True)
@click.option('-c', "--category", help='"default" or skip for default category, optional',
              default=None, required=False)
@click.option('-ur', "--url", help='url, optional', default=None, required=False)
@click.option('-a', "--alias", help='alias, optional', default=None, required=False)
def add(user, password, login, password_for_login, category, url, alias):
    """
    add login and password command
    """
    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        print(f'Error: User named "{user}" not exists')
        return
    elif not manager_obj.user_obj.check_user_password(password):
        print(f'Error: incorrect password for user named "{user}"')
        return

    if manager_obj.unit_obj.check_login(login):
        print(f'Error: login "{login}" already exists')
    else:
        category = None if category == 'default' else category
        manager_obj.unit_obj\
            .add_unit(user, password, login, password_for_login, category, url, alias)
        print(f' login "{login}" added')


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-nl', "--new-login", help='new login, optional',
              default=None, required=False)
@click.option('-pl', '--password-for-login',
              prompt="New password for login (Press 'Enter' for keep old password)",
              default='old-password',
              help="New password for login, "
                   "'old-password' for keep old password", hide_input=True)
@click.option('-nc', "--new-category", help='"default" or skip for default category, optional',
              default=None, required=False)
@click.option('-ur', "--url", help='url, optional', default=None, required=False)
@click.option('-a', "--alias", help='alias, optional', default=None, required=False)
def update(user, password, login, new_login, password_for_login, new_category, url, alias):
    """Update unit"""

    manager_obj = SQLAlchemyManager(FILE_USERS_DB, user, password)

    if not manager_obj.user_obj.check_user():
        print(f'Error: User named "{user}" not exists')
        return
    elif not manager_obj.user_obj.check_user_password(password):
        print(f'Error: incorrect password for user named "{user}"')
        return

    if not manager_obj.unit_obj.check_login(login):
        print(f'Error: login "{login}" not exists')
    elif manager_obj.unit_obj.check_login(new_login) \
            and login != new_login:
        print(f'Error: new login "{login}" already exists')
    else:
        new_category = None if new_category == 'default' else new_category
        manager_obj.unit_obj\
            .update_unit(user, password, login, new_login,
                         password_for_login, new_category, url, alias)
        print(f' login "{login}" updated')


if __name__ == '__main__':
    cli()
