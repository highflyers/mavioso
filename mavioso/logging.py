"""
Minimal logging module that prints messages to stdout
"""

CRITICAL = 50
ERROR = 40
WARNING	= 30
INFO = 20
DEBUG = 10
NOTSET = 0

LEVEL_NAMES = {CRITICAL: "CRITICAL", ERROR: "ERROR", \
WARNING: "WARNING", INFO: "INFO", DEBUG: "DEBUG", NOTSET: "NOTSET"}

def debug(msg, *args, **kwargs):
    log(DEBUG, msg, args, kwargs)

def info(msg, *args, **kwargs):
    log(INFO, msg, args, kwargs)
    
def warning(msg, *args, **kwargs):
    log(WARNING, msg, args, kwargs)

def error(msg, *args, **kwargs):
    log(INFO, msg, args, kwargs)

def critical(msg, *args, **kwargs):
    log(CRITICAL, msg, args, kwargs)

def exception(msg, *args, **kwargs):
    log(ERROR, msg, args, kwargs)

def log(lvl, msg, *args, **kwargs):
    print(LEVEL_NAMES[lvl] + "  " + msg)
