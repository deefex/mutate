import logging


def initialise_logger(log_file):
    """ Initialises and returns the logger instance """
    logger = logging.getLogger('mutate')
    handler = logging.FileHandler(log_file, mode='w')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def print_and_log(logger, text):
    """ Prevents clutter by sending data to stdout and the log file """
    print text
    logger.info(text)
