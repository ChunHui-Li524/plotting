import logging

LOGGER = None


def get_logger():
    global LOGGER
    if LOGGER is None:
        LOGGER = setup_logger('my_logger', 'app.log')
    return LOGGER


def setup_logger(name, log_file, level=logging.DEBUG):
    """Function setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)  # Only log Info and above to file

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)  # Log all messages to console

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
