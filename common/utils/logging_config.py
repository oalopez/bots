# logging_config.py

import logging
import os
from colorlog import ColoredFormatter

def setup_logger(base_directory):

    # Create a formatter that will color our log records
    color_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    # Basic formatter for file output
    basic_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Create a console handler using the formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)
    console_handler.setFormatter(color_formatter)

    # Create a FileHandler for app.log
    app_file_handler = logging.FileHandler(os.path.join(base_directory, 'logs/app.log'))
    app_file_handler.setFormatter(basic_formatter)

    # Create a FileHandler for error.log with level ERROR
    error_file_handler = logging.FileHandler(os.path.join(base_directory, 'logs/error.log'))
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(basic_formatter)

    # Get the root logger
    logger = logging.getLogger()
    # TODO: Set the minimum logging level depending on the environment
    logger.setLevel(logging.INFO) 

    # Remove existing handlers if any and add our custom handlers
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    logger.addHandler(console_handler)
    logger.addHandler(app_file_handler)
    logger.addHandler(error_file_handler)
