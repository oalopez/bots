import jsonpath_ng as jp
import re
import common.interpreter.local_interpreter as local_interpreter
import common.interpreter.global_interpreter as global_interpreter
import common.interpreter.python_interpreter as python_interpreter
import common.interpreter.jsonpath_interpreter as jsonpath_interpreter
import common.utils.exceptions as ex
import json
from  common.utils.profiling import lap_time

special_functions_array = ["jsonpath(", "local(", "global(", "python("]

@lap_time(tolerance=1)
def parse_element(base_directory, value_obj, element, context_vars, namespace=''):
    
    # if value is str
    if isinstance(value_obj, str):
        return special_functions_interpreter(base_directory, value_obj, element, context_vars, namespace)
    if isinstance(value_obj, dict):
        return dict_interpreter(base_directory, value_obj, element, context_vars, namespace)
    if isinstance(value_obj, list):
        return list_interpreter(base_directory, value_obj, element, context_vars, namespace)

@lap_time(tolerance=1)    
def dict_interpreter(base_directory, dict, element, context_vars, namespace):
    interpreted_dict = {}
    for key, value in dict.items():
        interpreted_dict[key] = parse_element(base_directory, value, element, context_vars, namespace)
    return interpreted_dict

@lap_time(tolerance=1)
def list_interpreter(base_directory, list, element, context_vars, namespace):
    interpreteded_list = []
    for value in list:
        interpreteded_list.append(parse_element(base_directory, value, element, context_vars, namespace))
    return interpreteded_list

@lap_time(tolerance=1)
def special_functions_interpreter(base_directory, string, element=None, context_vars=None, namespace=''):
    new_string = string
    needs_parsing, special_function_found, pattern = find_special_function(new_string, namespace)
    while needs_parsing:
        value = get_formula_content(new_string, special_function_found)
        
        if "jsonpath(" == special_function_found:
            interpreted_value = jsonpath_interpreter.interpret(value, element)
            
        elif "local(" == special_function_found:
            interpreted_value = local_interpreter.interpret(value, context_vars)
            
        elif "global(" == special_function_found:
            interpreted_value = global_interpreter.interpret(value, context_vars)

        elif "python(" == special_function_found:
            interpreted_value = python_interpreter.interpret(base_directory, value)

        if not interpreted_value:
            raise ex.InvalidFormulaException("Incorrect formula parsing: " + value)

        old_string = new_string 

        if isinstance(interpreted_value, str):
            new_string = re.sub(pattern, 
                                interpreted_value, 
                                old_string, 
                                count=1)
        
            if old_string == new_string:
                # inifinite loop break
                raise ex.InvalidFormulaException("Incorrect formula parsing (it didn't reduce): " + old_string)
        else:
            new_string = re.sub(pattern, 
                                json.dumps(interpreted_value), 
                                old_string, 
                                count=1)
            
        
        needs_parsing, special_function_found, pattern = find_special_function(new_string, namespace)
        
    return new_string

@lap_time(tolerance=1)
def get_formula_content(string, formula_delimiter):
    start_index = string.find(formula_delimiter)
    if start_index == -1:
        return ""  # or handle error

    start_index += len(formula_delimiter)
    paren_count = 1
    end_index = start_index

    while end_index < len(string) and paren_count > 0:
        if string[end_index] == '(':
            paren_count += 1
        elif string[end_index] == ')':
            paren_count -= 1
        end_index += 1

    return string[start_index:end_index-1] if paren_count == 0 else ""

@lap_time(tolerance=1)
def find_special_function(string, namespace):
    '''
    Returns True, the first special-function-string found and the pattern to replace
    Otherwise, returns False, None and None
    '''

    namespace_prefix = namespace + '.'  if namespace != '' else ''

    for special_function in special_functions_array:
        #create a pattern with the special function and the namespace prefix
        pattern = r"@{}{}".format(re.escape(namespace_prefix), re.escape(special_function))
        #check if the pattern is in the string
        if re.search(pattern, string):
            pattern_to_replace = r"@{}{}\([^)]*\)".format(namespace_prefix, special_function[:-1])
            return True, special_function, pattern_to_replace
    
    return False, None, None
