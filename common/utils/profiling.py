import time
import logging
import sys

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
                size = get_size(argument)

                # get second argument of the function call if is a string only get the first 10 characters
                if isinstance(argument, str):
                    arg_str = argument[:10] if len(argument) > 10 else argument
                    logger.warning(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with argument (str - truncated) <{arg_str}>")
                    

                # if is a list print the first element
                elif isinstance(argument, list):
                    logger.warning(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with argument (lstsize: {len(argument)}, bytesize: {size})")

                # if is a dict print the first key
                elif isinstance(argument, dict):
                    logger.warning(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with argument (dictsize {list(argument.keys())}, bytesize: {size})")

                else: #print type
                    #calculate bytesize of the argument
                    bytesize = sys.getsizeof(argument)
                    logger.warning(f"Function {func.__module__}.{func.__name__} elapsed time: {end:.3f} seconds. Called with arguments ({type(argument)}, bytesize: {size})")

            return result
        return wrapper
    return decorator

def get_size(obj):
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum([get_size(v) for v in obj.values()])
        size += sum([get_size(k) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i) for i in obj])
    return size