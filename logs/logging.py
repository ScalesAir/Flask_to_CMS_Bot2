import logging
import logging.handlers


def init_logger(name):
    loggers = logging.getLogger(name)
    sh_formats = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'
    fh_formats = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'
    loggers.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(sh_formats))
    sh.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(filename='logs/logs.csv', encoding='utf-8',
                                              maxBytes=1000000, backupCount=10)
    fh.setFormatter(logging.Formatter(fh_formats))
    fh.setLevel(logging.INFO)
    loggers.addHandler(sh)
    loggers.addHandler(fh)
    # logger.debug("logger was initialized")


init_logger("app")

logger = logging.getLogger("app.main")
