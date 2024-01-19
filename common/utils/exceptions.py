import logging

logger = logging.getLogger(__name__)

class RequiredFieldException(Exception):
    pass

class InvalidTypeException(Exception):
    pass

class InvalidFormulaException(Exception):
    pass

class JsonResponseError(Exception):
    def __init__(self, message="", should_continue=False):
        super().__init__(message)
        self.should_continue = should_continue

def handle_transformation_exception(exception, strategy="raise"):
    if strategy == "raise":
        logger.error(exception)
        raise exception
    elif strategy == "ignore":
        logger.error(f"Ignored: {exception}")
    elif strategy == "omit":
        pass
    else:
        raise InvalidTypeException(f"Exception strategy type '{strategy}' not supported")