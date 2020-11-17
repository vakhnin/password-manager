# cli.py
import click
import os

import database_manager.models


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
    session = database_manager.models.create_session()

    if database_manager.models.check_user(session, user):
        print(f'User named "{user}" already exists')
        print('New user not created')
    else:
        database_manager.models.add_user(session, user, password)
        print(f'User named "{user}" created')


@cli.command()
@user_argument
@password_argument
def deluser(user, password):
    """
    delete user command
    """
    session = database_manager.models.create_session()

    if not database_manager.models.check_user_password(session, user, password):
        print('Incorrect login or password')
        return

    if database_manager.models.check_user(session, user):
        database_manager.models.del_user(session, user)
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
    click.echo('Command: show')


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
@click.option('-ps', '--password-for-safe', prompt=True, hide_input=True)
def add(user, password, login, password_for_safe):
    """
    add login and password command
    """
    click.echo('Command: add')


if __name__ == '__main__':
    cli()
