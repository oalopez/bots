import os
import re
import datetime
import random
import jsonpath_ng as jp
import configparser

from common.interpreter.input_interpreter import input as input_func
from common.global_state import GlobalStateKeys, global_state

config = configparser.ConfigParser()
config.read('path/to/yourfile.properties')

def cons(value):
    return value

def concat(*args):
    '''Concatenate all arguments into a single string'''
    ret_value = ""
    for arg in args:
        ret_value += str(arg)
    return ret_value

def slice_string(s, start=None, end=None):
    # if start is a string convert to int
    if isinstance(start, str):
        start = int(start)
    # if is instance of int do nothing
    elif isinstance(start, int):
        pass
    else:
        raise Exception("start param must be a string: [" + str(start) + "] is not a string" )
    # if end is a string convert to int
    if isinstance(end, str):
        end = int(end)
    elif isinstance(end, int):
        pass
    else:
        raise Exception("end param must be a string: [" + str(end) + "] is not a string" )
    
    try:
        ret_value = s[start:end]
    except Exception as e:
        raise Exception("Error slicing string: " + str(e))
        
    return ret_value

def now(format_str):
    try:
        date_str = datetime.datetime.now().strftime(format_str)
    except Exception as e:
        raise Exception("Error getting current date: " + str(e) + ". Format: " + format_str)
    return date_str
    
def randint(start, end):
    try:
        ret_value = random.randint(int(start), int(end))
    except Exception as e:
        raise Exception("Error generating random int: " + str(e) + ". Start: " + str(start) + ". End: " + str(end))
    return str(ret_value)

def remove_decimals(value):
    return int(value)

def input(value):
    return input_func(value)

def jsonpath(value, json_data):
    jsonpath_expression = jp.parse(value)
    matches = jsonpath_expression.find(json_data)
    if matches:
        return matches[0].value
    else:
        raise ValueError(f"Jsonpath query '{value}' did not match any data")
    

base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)
properties_file_name = 'bot.properties'
properties_file_path = os.path.join(base_directory, properties_file_name)

def prop(section, prop_name):
    if not hasattr(prop, "config"):
        prop.config = configparser.ConfigParser()
        try:
            prop.config.read(properties_file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Properties file '{properties_file_path}' not found")
    
    return prop.config[section].get(prop_name, None)


def regex_sub(pattern, replacement, element):
    result = re.sub(pattern, replacement, element)
    return result