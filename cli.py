# cli.py
import os

import click
import pyperclip

from database_manager.models import FILE_DB, SQLAlchemyManager


@click.group()
@click.pass_context
def cli(ctx):
    pass


user_argument = click.option('--user', '-u', prompt="Username", help="Provide your username",
                             default=lambda: os.environ.get('USERNAME'))
password_argument = click.option('--password', '-p', prompt=True, hide_input=True)


@cli.command()
@user_argument
@password_argument
def useradd(user, password):
    """
    add user command
    """
    manager_obj = SQLAlchemyManager(FILE_DB, user)

    if manager_obj.user_obj.check_user():
        print(f'Error: User named "{user}" already exists')
    else:
        manager_obj.user_obj.add_user(password)
        print(f'User named "{user}" created')


@cli.command()
@user_argument
@password_argument
def deluser(user, password):
    """
    delete user command
    """
    manager_obj = SQLAlchemyManager(FILE_DB, user)

    if not manager_obj.user_obj.check_user_password(password):
        print('Error: incorrect login or password')
        return

    manager_obj.user_obj.del_user()
    print(f'User named "{user}" deleted')


@cli.command()
@user_argument
@password_argument
def show(user, password):
    """
    show logins command
    """
    manager_obj = SQLAlchemyManager(FILE_DB, user)

    if not manager_obj.user_obj.check_user_password(password):
        print('Error: incorrect login or password')
        return

    logins = manager_obj.unit_obj.all_logins()
    for login in logins:
        print(login)


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
def get(user, password, login):
    """
    get password by login command
    """
    manager_obj = SQLAlchemyManager(FILE_DB, user)

    if not manager_obj.user_obj.check_user_password(password):
        print('Error: incorrect login or password')
        return

    if manager_obj.unit_obj.check_login(login):
        pyperclip.copy(manager_obj.unit_obj.get_password(login))
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
    manager_obj = SQLAlchemyManager(FILE_DB, user)

    if not manager_obj.user_obj.check_user_password(password):
        print('Error: incorrect login or password')
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
@click.option('-pl', '--password-for-login', prompt=True, hide_input=True)
def add(user, password, login, password_for_login):
    """
    add login and password command
    """
    manager_obj = SQLAlchemyManager(FILE_DB, user)

    if not manager_obj.user_obj.check_user_password(password):
        print('Error: incorrect login or password')
        return

    if manager_obj.unit_obj.check_login(login):
        print(f'Error: login "{login}" already exists')
    else:
        manager_obj.unit_obj.add_unit(login, password_for_login)
        print(f' login "{login}" added')


@cli.command()
@user_argument
@password_argument
@click.option('-l', '--newusername', prompt="NewUsername", help="Provide new username")
@click.option('-pl', '--password-for-newusername', prompt=False, hide_input=True)
def userupd(user, password, newusername, password_for_newusername):
    """
    update username and password command
    """
    manager_obj = SQLAlchemyManager(FILE_DB, user)

    if not manager_obj.user_obj.check_user_password(password):
        print('Error: incorrect login or password')
        return

    manager_obj_new = SQLAlchemyManager(FILE_DB, newusername)

    if manager_obj_new.user_obj.check_user():
        print(f'Error: User named "{newusername}" already exists')
    else:
        manager_obj.user_obj.update_user(password, newusername, password_for_newusername)


if __name__ == '__main__':
    cli()
