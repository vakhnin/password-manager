# pwdone
## Password manager with command line interface

pwdone is a multi-user, multi-platform command-line utility 
for storing and organizing passwords and another info for logins.

1. Common commands

    help on using the utility:
    ```
    pwdone --help
    ```
    
    more detailed help on using utility commands:
    ```
    pwdone [command] --help
    ```
    
    adding a new user:
    ```
    pwdone uadd
    ```
    or using options
    ```
    pwdone uadd -u user-name
    ```    
    
    adding a new record in passwods DB:
    ```
    pwdone add
    ```
    or using options 
    ```
    pwdone add -u user-name -l login-for-site -a record-name
    ```
   
    show all user records:
    ```
    pwdone show
    ```
    
    get password of record to the clipboard:    
    ```
    pwdone get
    ```
    or using options    
    ```
    pwdone get -a record-name
    ```
    
    full list of command options:
    ```
    pwdone [command] --help
    ```

2. Installing the utility
    1. Installing on Ubuntu 
    2. Installing on Windows
