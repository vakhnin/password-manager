# cli.py
import click


@click.command()
@click.argument('command')
def main(command):
    if command == 'show':
        print('show')
    elif command == 'show':
        print('show')
    else:
        print('No such command')
        print('Try \'cli.py --help\' for help.')


if __name__ == "__main__":
    main()
