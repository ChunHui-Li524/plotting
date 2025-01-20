import datetime
import logging
import os

LOGGER = None


def get_logger():
    global LOGGER
    if LOGGER is None:
        LOGGER = setup_logger('my_logger')
    return LOGGER


def new_logger():
    global LOGGER
    LOGGER = None


def setup_logger(name, level=logging.DEBUG):
    """Function setup as many loggers as you want"""
    log_file = create_log()
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


def create_log():
    dir_path = os.path.join(os.getcwd(), "log")
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    log_path = os.path.join(dir_path, f"log_{now}.log")
    return log_path


if __name__ == '__main__':
    get_logger().info("123")
