# cli.py
import click
import os


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option('-u', '--user')
@click.option("--user", prompt="Username", help="Provide your username",
              default=lambda: os.environ.get('USERNAME'))
@click.option('-p', '--password')
@click.option('--password', prompt=True, hide_input=True)
def useradd(user, password):
    """
    add user
    """
    click.echo('Command: useradd')


@cli.command()
@click.option('-u', '--user')
@click.option("--user", prompt="Username", help="Provide your username",
              default=lambda: os.environ.get('USERNAME'))
@click.option('-p', '--password')
@click.option('--password', prompt=True, hide_input=True)
def deluser(user, password):
    """
    delete user
    """
    click.echo('Command: deluser ')


@cli.command()
@click.option('-u', '--user')
@click.option("--user", prompt="Username", help="Provide your username",
              default=lambda: os.environ.get('USERNAME'))
@click.option('-p', '--password')
@click.option('--password', prompt=True, hide_input=True)
def show(user, password):
    """
    show logins
    """
    click.echo('Command: show')


@cli.command()
@click.option('-u', '--user')
@click.option("--user", prompt="Username", help="Provide your username",
              default=lambda: os.environ.get('USERNAME'))
@click.option('-p', '--password')
@click.option('--password', prompt=True, hide_input=True)
@click.option('-l', '--login')
@click.option("--login", prompt="Login", help="Provide login")
def get(user, password, login):
    """
    get logins
    """
    click.echo('Command: get')


@cli.command()
@click.option('-u', '--user')
@click.option("--user", prompt="Username", help="Provide your username",
              default=lambda: os.environ.get('USERNAME'))
@click.option('-p', '--password')
@click.option('--password', prompt=True, hide_input=True)
@click.option('-l', '--login')
@click.option("--login", prompt="Login", help="Provide login")
def delete(user, password, login):
    """
    delete logins
    """
    click.echo('Command: delete')


@cli.command()
@click.option('-u', '--user')
@click.option("--user", prompt="Username", help="Provide your username",
              default=lambda: os.environ.get('USERNAME'))
@click.option('-p', '--password')
@click.option('--password', prompt=True, hide_input=True)
@click.option('-l', '--login')
@click.option("--login", prompt="Login", help="Provide login")
@click.option('-ps', '--password-for-safe')
@click.option('--password-for-safe', prompt=True, hide_input=True)
def add(user, password, login, password_for_safe):
    """
    add login and password
    """
    click.echo('Command: add')


if __name__ == '__main__':
    cli()
