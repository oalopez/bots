import logging

logger = logging.getLogger(__name__)

class RequiredFieldException(Exception):
    pass

class InvalidTypeException(Exception):
    pass
        
def handle_transformation_exception(exception, strategy="raise"):
    if strategy == "raise":
        logger.error(exception)
        raise exception
    elif strategy == "ignore":
        logger.error(f"Ignored: {exception}")
    elif strategy == "omit":
        pass
    else:
        raise InvalidTypeException(f"Exception strategy '{strategy}' not supported")