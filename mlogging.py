
from config import CONFIG
from utils import *

import logging


class MLogging:

    def __init__(self):

        self.loggers = []
        self._DEFAULT_FORMAT = '[%(levelname)s] %(asctime)s (%(relativeCreated)d): {}%(message)s'

        self.glogger = self.get_logger()  # 在不需要特別建立一個經設定的logger時可直接調用此glogger

        self.CRITICAL = logging.CRITICAL
        self.ERROR = logging.ERROR
        self.WARNING = logging.WARNING
        self.INFO = logging.INFO
        self.DEBUG = logging.DEBUG
        self.NOTSET = logging.NOTSET


    def get_logger(self, log_name=None, use_console=True, level=CONFIG.LOG_LEVEL, format_str=None, logger_name=None, log_dir_path=CONFIG.LOG_DIR, prefix=None):

        """
        建立一個經設定的logging物件

        回傳的logger用法與一般logging一樣，主要是簡化初始的流程

        Args:
            log_name: log檔的檔名，若不需要輸出log檔可不使用此參數(None)
            use_console: log是否要輸出在console上面(True/False)
            level: 要印出的log等級，與logging的用法相同
            format_str: log內容的字串模板，預設為self._DEFAULT_FORMAT
            logger_name: 為logger取名，等同原本logging.getLogger()的name參數
            log_dir_path: 輸出log檔的存放目錄，預設為CONFIG.LOG_DIR
            prefix: log時可為log的訊息加上prefix

        Returns:
            logger: 經設定的logger，相當於經調整過的logging.getLogger
        """

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


mlogging = MLogging()


if __name__ == '__main__':

    logger = mlogging.logger(log_name='test.log')
