# cli.py
import click
import os

from database_manager.models import User, create_session
from main import get_hash


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
    add user
    """
    session = create_session()

    if len(session.query(User).filter(User.user == user).all()):
        print(f'User named "{user}" already exists')
        print('New user not created')
    else:
        pass_hash = get_hash((user + password).encode("utf-8"))
        user_for_add = User(user, pass_hash)
        session.add(user_for_add)
        print(f'User named "{user}" created')

    session.commit()


@cli.command()
@user_argument
@password_argument
def deluser(user, password):
    """
    delete user
    """
    session = create_session()

    pass_hash = get_hash((user + password).encode("utf-8"))
    if not len(session.query(User).filter(User.user == user)
                       .filter(User.password == pass_hash).all()):
        print('Incorrect login or password')
        session.commit()
        return

    if len(session.query(User).filter(User.user == user).all()):
        session.query(User).filter(User.user == user).delete()
        print(f'User named "{user}" deleted')
    else:
        print(f'User named "{user}" does not exist')
        print('User not deleted')

    session.commit()


@cli.command()
@user_argument
@password_argument
def show(user, password):
    """
    show logins
    """
    click.echo('Command: show')


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
def get(user, password, login):
    """
    get password by login
    """
    click.echo('Command: get')


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
def delete(user, password, login):
    """
    delete login and password
    """
    click.echo('Command: delete')


@cli.command()
@user_argument
@password_argument
@click.option('-l', "--login", prompt="Login", help="Provide login")
@click.option('-ps', '--password-for-safe', prompt=True, hide_input=True)
def add(user, password, login, password_for_safe):
    """
    add login and password
    """
    click.echo('Command: add')


if __name__ == '__main__':
    cli()
