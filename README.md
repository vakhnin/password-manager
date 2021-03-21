# pwdone

### Password manager with a command-line interface

pwdone is a multi-user, multi-platform command-line utility for storing and organizing passwords and another info for
logins

### Contents
1\. Common commands

2\. Installing and unistall the utility

3\. Backup and restore data
<br>
<br>

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

   adding a new record in passwords DB:
   ```
   $ pwdone add
   ```
   or using options:
   ```
   $ pwdone add -u user-name -l login-for-site -n record-name
   ```
   <br>   

   show all user records:
   ```
   $ pwdone show
   ```
   <br>   

   get the password of record to the clipboard:
   ```
   $ pwdone get
   ```
   or using options:
   ```
   $ pwdone get -n record-name
   ```
   <br>   

   full list of command options:
   ```
   $ pwdone [command] --help
   ```
   <br>  

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
       $ sudo apt update
       $ sudo apt upgrade
       $ sudo apt install python3-pip
       $ pip3 --version
       ```       
       <br>
       install pwdone:
       
       ```
       $ sudo apt install -y xclip
       $ git clone https://github.com/vakhnin/pwdone.git
       $ cd pwdone
       $ pip3 install --user .
       $ echo -e "export PATH=\"$HOME/.local/bin:$PATH\"" >> ~/.bashrc
       $ source ~/.bashrc
       ```     
       <br>
       uninstall pwdone:
       
       ```
       $ pip3 uninstall -y pwdone
       ```
    <br>                 

    2. Installing on Windows
   
   <br>
   
   the utility requires python 3.8 or higher<br> 
   check version python:
   ```
   $ python --version
   ```
   
   check pip3:
   ```
   $ pip3 --version
   ```       
   <br>
   clone pwdone
   
   ```
   $ git clone https://github.com/vakhnin/pwdone.git
   $ cd pwdone
   ```
   install pipenv:
   
   ```
   pip3 install pipenv
   ```    

   install pwdone:
   ```
   $ pipenv install
   $ pipenv shell
   ```   

   making .msi installer for Windows:
   ```
   $ python setup.py bdist --format=msi
   ```   

   run the .msi installer in the 'dist' folder by double click
   <br>
   <br>
   To uninstall pwdone, look in Apps & features Windows 
   for an application like 'Python pwdone-1.0'
   

3. Backup and restore data
   <br>
   <br>
   All data is stored in the database.sqlite file. 
   You can simply copy the database.sqlite file for 
   backup and replace the database.sqlite file with 
   the one you previously saved to restore all data.
   
   Show where is BD file:
   ```
   $ pwdone where
   ```   