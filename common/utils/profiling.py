import time
import logging

logger = logging.getLogger(__name__)

def lap_time(tolerance=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time() - start

            # if the function has two argument assign else assign the first argument
            if len(args) == 2:
                argument = args[1]
            else:
                argument = args[0]

            # execue the following only if the end time is greater than 2 seconds
            if end > 2:
                # get second argument of the function call if is a string only get the first 10 characters
                if isinstance(argument, str):
                    print(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with 2 argument (str) {argument}")
                    logger.warning(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with 2 argument (str) {argument[:10]}")
                    

                # if is a list print the first element
                elif isinstance(argument, list):
                    print(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with 2 argument (list) {argument[0]}")
                    logger.warning(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with 2 argument (str) {argument[:10]}")

                # if is a dict print the first key
                elif isinstance(argument, dict):
                    print(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with 2 argument (dict) {list(argument.keys())[0]}")
                    logger.warning(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with 2 argument (str) {argument[:10]}")

                else: #print type
                    print(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with 2 argument ({type(argument)}) {argument}")
                    logger.warning(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with 2 argument (str) {argument[:10]}")

            return result
        return wrapper
    return decorator