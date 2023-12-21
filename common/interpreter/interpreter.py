import jsonpath_ng as jp
import re
import common.interpreter.local_interpreter as local_interpreter
import common.interpreter.global_interpreter as global_interpreter
import common.interpreter.python_interpreter as python_interpreter
import common.interpreter.jsonpath_interpreter as jsonpath_interpreter
import common.utils.exceptions as ex

def parse_element(value_obj, element, context_vars, namespace=''):
    # if value is str
    if isinstance(value_obj, str):
        return special_functions_interpreter(value_obj, element, context_vars, namespace)
    if isinstance(value_obj, dict):
        return dict_interpreter(value_obj, element, context_vars, namespace)
    if isinstance(value_obj, list):
        return list_interpreter(value_obj, element, context_vars, namespace)

def dict_interpreter(dict, element, context_vars, namespace):
    interpreted_dict = {}
    for key, value in dict.items():
        interpreted_dict[key] = parse_element(value, element, context_vars, namespace)
    return interpreted_dict

def list_interpreter(list, element, context_vars, namespace):
    interpreteded_list = []
    for value in list:
        interpreteded_list.append(parse_element(value, element, context_vars, namespace))
    return interpreteded_list

def special_functions_interpreter(string, element=None, context_vars=None, namespace=''):
    new_string = string

    namespace_prefix = namespace + '.'  if namespace != '' else ''
    jsonpath_string = '@'+ namespace_prefix + 'jsonpath('
    local_string = '@'+ namespace_prefix + 'local('
    global_string = '@'+ namespace_prefix + 'global('
    python_string = '@'+ namespace_prefix + 'python('

    while (jsonpath_string in new_string)       \
            or (local_string in new_string)     \
            or (global_string in new_string)    \
            or (python_string in new_string):
        
        if jsonpath_string in new_string:
            value = get_formula_content(new_string, jsonpath_string)
            #pattern with variable jsonpath_string
            pattern = r"@{}jsonpath\([^)]*\)".format(namespace_prefix)
            interpreted_value = jsonpath_interpreter.interpret(value, element)
            
        elif local_string in new_string:
            value = get_formula_content(new_string, local_string)
            pattern = r"@{}local\([^)]*\)".format(namespace_prefix)
            interpreted_value = local_interpreter.interpret(value, context_vars)
            
        elif global_string in new_string:
            value = get_formula_content(new_string, global_string)
            pattern = r"@{}global\([^)]*\)".format(namespace_prefix)
            # pattern = r"@global\([^)]*\)"
            interpreted_value = global_interpreter.interpret(value, context_vars)

        elif python_string in new_string:
            value = get_formula_content(new_string, python_string)
            pattern = r"@{}python\((?:[^)(]+|\([^)]*\))*\)".format(re.escape(namespace_prefix))
            interpreted_value = python_interpreter.interpret(value)

        old_string = new_string    
        new_string = re.sub(pattern, 
                            interpreted_value, 
                            old_string, 
                            count=1)
        
        if old_string == new_string:
            # inifinite loop break
            raise ex.InvalidFormulaException("Incorrect formula parsing (it didn't reduce): " + old_string)
        
    return new_string

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
