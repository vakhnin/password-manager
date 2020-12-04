import os


DIR_DB = 'databases'
DIR_UNITS_DBS = DIR_DB + os.sep + 'units'
FILE_USERS_DB = os.path.join(DIR_DB, 'users.sqlite')

TIME_SESSION_CLOSE = 15 * 60  # дефолтное время в секундах, отведенное на длительность сессии


if not os.path.exists(DIR_UNITS_DBS):
    os.makedirs(DIR_UNITS_DBS)
