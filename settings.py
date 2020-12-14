import pathlib

DB_ROOT = 'databases'
DIR_DB = pathlib.Path.cwd() / DB_ROOT
DIR_UNITS_DBS = DIR_DB / 'units'
FILE_USERS_DB = DIR_DB / 'users.sqlite'

LOGS_PATH = pathlib.Path.cwd() / 'logs' / 'common.log'

TIME_SESSION_CLOSE = 15 * 60  # дефолтное время в секундах, отведенное на длительность сессии

if not DIR_UNITS_DBS.exists():
    DIR_UNITS_DBS.mkdir(parents=True)

if not LOGS_PATH.parent.exists():
    LOGS_PATH.parent.mkdir(parents=True)
    LOGS_PATH.touch()
