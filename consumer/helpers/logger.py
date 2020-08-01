
import logging
from logging.handlers import RotatingFileHandler


class BaseLogger():

    """Class to log the  information to STDOUT."""

    def logger_instance(self):
        try:
            logging.basicConfig(level=logging.INFO)
            # deletes after 1000 entries, infinite loop
            handler = RotatingFileHandler(
                'app.log', maxBytes=5e+9, backupCount=1000)
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            return logger
        except Exception:
            print('error creating logger  instance')
             