import logging

LOGGER = None


def get_error_logger():
    global LOGGER
    if LOGGER is None:
        LOGGER = setup_logger('my_logger', 'error.log')
    return LOGGER


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
