from settings import settings
import logging
from logging.handlers import RotatingFileHandler
import sys
import os  # Add this import

class stdredirector():
    def __init__(self):
        self.data = []

    def write(self, s):
        if len(s) > 1:
            logger.info(s)

    def flush(self):
        pass

# Ensure log directory exists
log_dir = os.path.dirname(settings['logfilepath'])
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(settings['logappname'])
logger.setLevel(logging.INFO)
LogFile = RotatingFileHandler(settings['logfilepath'], maxBytes=1048576, backupCount=10)
formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s : %(message)s')
LogFile.setFormatter(formatter)
logger.addHandler(LogFile)
sys.stdout = x = stdredirector()
print('Logging started')
