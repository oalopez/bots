import datetime
import random
from common.utils.exceptions import CustomFunctionException

def slice_string(s, start=None, end=None):
    # if start is a string convert to int
    if isinstance(start, str):
        start = int(start)
    else:
        raise CustomFunctionException("start param must be a string: [" + str(start) + "] is not a string" )
    # if end is a string convert to int
    if isinstance(end, str):
        end = int(end)
    else:
        raise CustomFunctionException("end param must be a string: [" + str(end) + "] is not a string" )
    
    try:
        ret_value = s[start:end]
    except Exception as e:
        raise CustomFunctionException("Error slicing string: " + str(e))
        
    return ret_value

def now(format_str):
    try:
        date_str = datetime.datetime.now().strftime(format_str)
    except Exception as e:
        raise CustomFunctionException("Error getting current date: " + str(e) + ". Format: " + format_str)
    return date_str
    
def randint(start, end):
    try:
        ret_value = random.randint(int(start), int(end))
    except Exception as e:
        raise CustomFunctionException("Error generating random int: " + str(e) + ". Start: " + str(start) + ". End: " + str(end))
    return str(ret_value)