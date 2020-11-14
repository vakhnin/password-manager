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
def get(user, password):
    """
    get logins
    """
    click.echo('Command: get')


if __name__ == "__main__":
    cli()
