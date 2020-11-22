from setuptools import setup

setup(
    name='SOS',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        SOS=cli:cli
    ''',
)