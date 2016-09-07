import logging

def initialise_logger(log_file):
    logger = logging.getLogger('mutate')
    handler = logging.FileHandler(log_file, mode='w')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def print_and_log(logger, text):
    '''
    Prevents clutter in the main routine by printing (to stdout) and logging
    '''
    print text
    logger.info(text)