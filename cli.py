# cli.py
import click
import os


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
