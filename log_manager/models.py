import logging
import os
from logging.handlers import TimedRotatingFileHandler


def change_filename(filename):
    filename_parts = filename.rsplit('.', maxsplit=2)
    if filename_parts[-1] == 'log':
        return filename
    elif filename_parts[-2] == 'log':
        return filename_parts[0] + '.' + filename_parts[2] + '.log'
    else:
        print('Внутренняя ошибка: базовый файл логирования не заканчивается на ".log"')
        exit(-1)


LOG = logging.getLogger('cli')

FORMATTER = \
    logging.Formatter('%(asctime)s - %(levelname)s -  %(name)s - %(message)s ')

LOGS_PATH = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH)
LOGS_PATH = os.path.join(LOGS_PATH, 'common.log')


ROTATION_LOGGING_HANDLER = \
    TimedRotatingFileHandler(
        LOGS_PATH, when='D', interval=1, backupCount=5, encoding='utf-8')
ROTATION_LOGGING_HANDLER.setFormatter(FORMATTER)
ROTATION_LOGGING_HANDLER.setLevel(logging.DEBUG)
ROTATION_LOGGING_HANDLER.namer = change_filename

LOG.addHandler(ROTATION_LOGGING_HANDLER)

LOG.setLevel(logging.DEBUG)
