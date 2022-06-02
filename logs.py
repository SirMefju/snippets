import logging
from datetime import datetime


def info(message, logs):
    return logs_config(logs).info(regular_message(message))

def debug(message, logs):
    return logs_config(logs).debug(regular_message(message))

def warning(message, logs):
    return logs_config(logs).warning(regular_message(message))

def error(message, logs):
    return logs_config(logs).error(regular_message(message))

def regular_message(message):
    splitted_message = message.split('|')
    red = '\033[31m'
    reset = '\033[0m'
    return str(datetime.today().strftime('%d-%m-%Y')) + ' ' + str(datetime.now().strftime('%H:%M:%S')) + ' | ' + red + splitted_message[0] + reset + ' | ' + splitted_message[1]

loggers = {}
def logs_config(logs):
    if logs not in loggers:
        loggers[logs] = setup_logger(logs, logs + '.log')
    return loggers[logs]

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)        
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
