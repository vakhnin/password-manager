# pwdone

## Password manager with command line interface

pwdone is a multi-user, multi-platform command-line utility for storing and organizing passwords and another info for
logins.

1. Common commands
   <br>
   <br>

   help on using the utility:
    ```
    $ pwdone --help
    ```
   <br>   

   more detailed help on using utility commands:
    ```
    $ pwdone [command] --help
    ```
   <br>   

   adding a new user:
    ```
    $ pwdone uadd
    ```
   or using options:
    ```
    $ pwdone uadd -u user-name
    ``` 
   <br>      

   adding a new record in passwods DB:
    ```
    $ pwdone add
    ```
   or using options:
   ```
   $ pwdone add -u user-name -l login-for-site -a record-name
   ```
   <br>   

   show all user records:
    ```
    $ pwdone show
    ```
   <br>   

   get password of record to the clipboard:
    ```
    $ pwdone get
    ```
   or using options:
    ```
    $ pwdone get -a record-name
    ```
   <br>   

   full list of command options:
    ```
    $ python3 --version [command] --help
    ```

2. Installing the utility

   <br>

    1. Installing on Ubuntu
       <br>   
       the utility requires python 3.8 or higher

       check version python:
       ```
       $ python3 --version
       ```
       <br>
       install pip3:
       
       ```
       sudo apt update
       $ sudo apt upgrade
       $ sudo apt install python3-pip
       $ pip3 --version
       ```
       <br>
       install pipenv:
       
       ```
       pip3 install --user pipenv
       ```
       if you see a warning like this
       ```
       WARNING: The script virtualenv is installed 
       in '/home/sv/.local/bin' which is not on PATH.
       ```
       follow this:
         - Open ~/.profile file.
         - Check if ~/.local/bin path exist in that file.
         - If not add these following lines:
            ```
            # set PATH so it includes user's private bin if it exists
            if [ -d "$HOME/.local/bin" ] ; then
               PATH="$HOME/.local/bin:$PATH"
            ```
         - Run bash --login for login mode because ~/.profile 
           is executed for login shells.
   

    2. Installing on Windows
