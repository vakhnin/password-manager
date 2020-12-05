import logging
import os
from logging.handlers import TimedRotatingFileHandler

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
LOG.addHandler(ROTATION_LOGGING_HANDLER)

LOG.setLevel(logging.DEBUG)
