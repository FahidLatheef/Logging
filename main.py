import logging
import platform
import sys


class LoggingFormatHelper(logging.LogRecord):
    """
    Helps in setting origin (functionname and line no) and hostname in logging format. Inherited using LogRecordFactory.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.origin = f"{self.funcName}: {self.lineno}"
        self.hostname = f"{platform.node()}"


def start_logger(name=None, output_file="log.log", level="INFO", show_console_output=True):
    """
    Start or Continue logger with the inputted configuration
    :param name: Start or Append logger with the specified name
    :type name: str or None
    :param output_file: Log file name
    :type output_file: str
    :param level: Logger Level
    :type level: str
    :param show_console_output: Decides if logs should be printed to console or not
    :type show_console_output: bool
    :return: Logger with the given configuration
    :rtype: logging.Logger
    """
    logging.setLogRecordFactory(LoggingFormatHelper)

    # Create Logger
    if not name:
        logger_instance = logging.getLogger(name)
    else:
        logger_instance = logging.getLogger()  # Root logger
    logger_instance.setLevel(level)

    # Console Handler
    if show_console_output:
        ch = logging.StreamHandler(sys.stdout)  # create console handler which print in console
        ch.setFormatter(logging.Formatter(
            "%(levelname)-9s | %(asctime)s | %(hostname)-40s | %(filename)-20s | %(origin)-20s | %(message)-s"))
        logger_instance.addHandler(ch)

    # File handler
    fh = logging.FileHandler(output_file)
    fh.setFormatter(logging.Formatter(
        "%(levelname)-9s | %(asctime)s | %(hostname)-40s | %(filename)-20s | %(origin)-20s | %(message)-s"))
    logger_instance.addHandler(fh)

    return logger_instance


if __name__ == '__main__':
    logger = start_logger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
