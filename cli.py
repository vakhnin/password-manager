# cli.py
import click
import os

from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

from database_setup import users_table, User, create_session


@click.group()
@click.pass_context
def cli(ctx):
    pass


user_argument = click.option('--user', '-u', prompt="Username", help="Provide your username",
                             default=lambda: os.environ.get('USERNAME'))
password_argument = click.option('--password', '-p', prompt=True, hide_input=True)

# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///db.sqlite', echo=False)
# Session = sessionmaker(bind=engine)
# session = Session()

session, _ = create_session()

mapper(User, users_table)
# user = User("user1", "qweasdzxc")

print(session.query(User).filter(User.user == 'user1').all())

# session.add(user)
session.commit()


@cli.command()
@user_argument
@password_argument
def useradd(user, password):
    """
    add user
    """
    click.echo('Command: useradd')


@cli.command()
@user_argument
@password_argument
def deluser(user, password):
    """
    delete user
    """
    click.echo('Command: deluser ')


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
