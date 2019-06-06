

from config import CONFIG
from utils import *

import logging


class MLogging:

    def __init__(self):

        self.loggers = []
        self._DEFAULT_FORMAT = '[%(levelname)s] %(asctime)s (%(relativeCreated)d): {}%(message)s'

        self.glogger = self.logger()

        self.CRITICAL = logging.CRITICAL
        self.ERROR = logging.ERROR
        self.WARNING = logging.WARNING
        self.INFO = logging.INFO
        self.DEBUG = logging.DEBUG
        self.NOTSET = logging.NOTSET


    def logger(self, log_name=None, use_console=True, level=CONFIG.LOG_LEVEL, format_str=None, logger_name=None, log_dir_path=CONFIG.LOG_DIR, prefix=None):

        # get logger
        new_logger = logging.getLogger(str(len(self.loggers)) if logger_name==None else logger_name)
        new_logger.setLevel(level)

        # set logger format
        format_str = format_str if format_str!=None else self._DEFAULT_FORMAT.format('' if prefix==None else '%s | '%prefix)
        log_formatter = logging.Formatter(format_str)

        # set file handler
        if log_name!=None:
            logPath = relpath(log_name, log_dir_path)
            file_handler = logging.FileHandler(logPath, encoding='utf8')
            file_handler.setFormatter(log_formatter)
            new_logger.addHandler(file_handler)

        if use_console:
            console_andler = logging.StreamHandler()
            console_andler.setFormatter(log_formatter)
            new_logger.addHandler(console_andler)

        self.loggers.append(new_logger)

        return new_logger


def progress_log(seq, total_num, name=None, format_str='processing: %s%%', log_freq=None, logger=None):
    if log_freq==None or seq%log_freq==0:
        if logger==None:
            logger = mlogging.glogger
        if name is not None:
            format_str = '%s %s'%(name, format_str)
        logger.info(format_str%(round((seq/total_num)*100, 2)))



mlogging = MLogging()


if __name__ == '__main__':

    logger = mlogging.logger(log_name='test.log')
