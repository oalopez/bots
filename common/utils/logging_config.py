# logging_config.py

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from colorlog import ColoredFormatter
from common.global_state import GlobalStateKeys, global_state


def setup_logger():

    base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)
    if not base_directory:
        raise ValueError("Base directory is not set")

    # Create the logs directory if it doesn't exist
    if not os.path.exists(os.path.join(base_directory, 'logs')):
        os.makedirs(os.path.join(base_directory, 'logs'))
    
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
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(color_formatter)

    # Create a TimedRotatingFileHandler for app.log
    app_file_handler = TimedRotatingFileHandler(
        os.path.join(base_directory, 'logs/app.log'), 
        when='midnight', 
        backupCount=15  # Keep last 15 days of logs
    )
    app_file_handler.setLevel(logging.INFO)
    app_file_handler.setFormatter(basic_formatter)

    # Create a TimedRotatingFileHandler for error.log with level ERROR
    error_file_handler = TimedRotatingFileHandler(
        os.path.join(base_directory, 'logs/error.log'), 
        when='midnight', 
        backupCount=15  # Keep last 15 days of logs
    )
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
