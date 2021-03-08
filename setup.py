# Установка приложения:
# $ pipenv install -e .
#
# Создание установщика для Windows
# $ python setup.py bdist --format=msi
# Установщик в папке dist
from setuptools import setup

setup(
    name='pwdone',
    version='1.2',
    py_modules=['cli'],
    test_suite='tests',
    install_requires=[
        'click',
        'sqlalchemy',
        'tk',
        'pycryptodomex',
        'pycryptodome',
    ],
    entry_points='''
        [console_scripts]
        pwdone=cli:cli
    ''',
)
