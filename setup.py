# Установка приложения:
# $ pipenv install -e .
from setuptools import setup

setup(
    name='pwdone',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pwdone=cli:cli
    ''',
)
