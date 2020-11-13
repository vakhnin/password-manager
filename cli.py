# cli.py
import click
import os
import encryption


def get_passwords(username, password):
    """
    This function extracts passwords table from database
    """
    os.chdir("databases" + os.sep + username)
    # Function decrypts database
    cipher = encryption.AESCipher(password)
    with open(username + ".database", "r") as f:
        encrypted = f.read()
        text = cipher.decrypt(encrypted)
    if not text:
        os.chdir("..")
        return None

    # Then from decrypted text it extracts line with login and password
    text = text.splitlines()
    passwords_table = {}
    for line in text:
        line = line.strip().split(':')
        passwords_table[line[0]] = line[1]
    os.chdir('..')
    os.chdir('..')
    return passwords_table


@click.command()
@click.argument('command')
@click.option('-u', '--username')
@click.option("--username", prompt="Username", help="Provide your username")
@click.option('-p', '--password')
@click.option('--password', prompt=True, hide_input=True)
def main(command, username, password):
    """
    Функция выбора команды
    """
    if command == 'show': # Отображение всех сохраненных логинов
        passwords_table = get_passwords(username, password)
        if not passwords_table:
            print("!!!Something went wrong. Database is corrupted or not exists!!!")
        for login in passwords_table.keys():
            print(login)
    elif command == 'get':
        print('get')
    else:
        print('No such command')
        print('Try \'cli.py --help\' for help.')


if __name__ == "__main__":
    main()
