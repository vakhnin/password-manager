# cli.py
import os

import click
from sqlalchemy.orm.exc import FlushError

from database_manager.models import SQLAlchemyManager, FILE_DB


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

    if manager_obj.check_user():
        print(f'User named "{user}" already exists')
        print('New user not created')
    else:
        manager_obj.add_user(password)
        print(f'User named "{user}" created')


@cli.command()
@user_argument
@password_argument
def deluser(user, password):
    """
    delete user command
    """
    manager_obj = SQLAlchemyManager(FILE_DB, user)

    if not manager_obj.check_user_password(password):
        print('Incorrect login or password')
        return

    if manager_obj.check_user():
        manager_obj.del_user()
        print(f'User named "{user}" deleted')
    else:
        print(f'User named "{user}" does not exist')
        print('User not deleted')


@cli.command()
@user_argument
@password_argument
def show(user, password):
    """
    show logins command
    """
    manager_obj = SQLAlchemyManager(FILE_DB, user)

    if not manager_obj.check_user_password(password):
        print('Incorrect login or password')
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
    click.echo('Command: get')


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
def delete(user, password, login):
    """
    delete login and password command
    """
    click.echo('Command: delete')


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

    if not manager_obj.check_user_password(password):
        print('Incorrect login or password')
        return

    if manager_obj.unit_obj.check_login(login):
        print(f'Error: login "{login}" already exists')
    else:
        manager_obj.unit_obj.add_item(login, password_for_login)
        print(f' login "{login}" added')


if __name__ == '__main__':
    cli()
