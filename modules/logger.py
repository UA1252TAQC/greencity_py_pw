"""
Module for holding logs
"""

import logging
import sys
from datetime import datetime


class TcLogger:
    """
    Class that intended for keeping logs
    """
    __logger = None

    def __init__(self, level: int = 100, logger_name: str = 'TITLE'):
        self._level = level
        self._logger_name = logger_name
        logging.addLevelName(self._level, self._logger_name)

    @classmethod
    def get_log(cls):
        """
        Class method for getting single log object

        :return: <class 'CustomLogger'> (single object of class
        CustomLogger)

        Example:

        The following example will show how to use only one logger
        object to logging something

        .. code-block:: python

                from utils_sdk.logger import CustomLogger

                custom_logger = CustomLogger.get_log()

                'returns single object no matter if exist or not'
        """
        if not cls.__logger:
            cls.__logger = TcLogger()
        return cls.__logger

    def log_test_name(self, test_name: str):
        """
        Method for holding test name logs

        :param test_name: str
        :return: None

        Example:

        The following example will show how to log test name

        .. code-block:: python

                from utils_sdk.logger import CustomLogger

                custom_logger = CustomLogger.get_log()

                def my_test():

                    custom_logger.log_test_name("this test checking
                    something")
        """
        logging.log(self._level, test_name)

    @staticmethod
    def generate_logs(
            level: str = 'INFO',
            detailed_logs: bool = False,
            write_to_file: bool = True) -> None:
        """
        Fixture to generate log file after test run.

        :param level: Log level ('INFO' by default)
        :param detailed_logs: display detailed logs from stdout
        (False by default)
        :param write_to_file: write to file (True by default)

        :return: None

        The following example will show how to generate logs
        in fixtures

        .. code-block:: python
                from utils_sdk.logger import CustomLogger

                def generate_logs():

                    CustomLogger.generate_logs(level=DEBUG,
                     detailed_logs=True)
        """

        logger = logging.getLogger()
        logger.setLevel(level)

        if detailed_logs:
            stdout_handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(stdout_handler)

        if write_to_file:
            formatter = logging.Formatter(
                fmt='[%(asctime)s] %(levelname)-4s %(filename)-4s '
                    '[LINE:%(lineno)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
            file_handler = logging.FileHandler(
                '{:%Y-%m-%d}.log'.format(datetime.now()), mode='a')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            screen_handler = logging.StreamHandler(stream=sys.stdout)
            screen_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(screen_handler)
