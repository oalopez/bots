import jsonpath_ng as jp
import re
import common.preprocessor.local_preprocessor as local_preprocessor
import common.preprocessor.global_preprocessor as global_preprocessor
import common.preprocessor.python_preprocessor as python_preprocessor
import common.preprocessor.jsonpath_preprocessor as jsonpath_preprocessor

def parse_element(value_obj, element, context_vars):
    # if value is str
    if isinstance(value_obj, str):
        return preprocess_special_functions(value_obj, element, context_vars)
    if isinstance(value_obj, dict):
        return preprocess_dict(value_obj, element, context_vars)
    if isinstance(value_obj, list):
        return preprocess_list(value_obj, element, context_vars)

def preprocess_dict(dict, element, context_vars):
    preprocessed_dict = {}
    for key, value in dict.items():
        preprocessed_dict[key] = parse_element(value, element, context_vars)
    return preprocessed_dict

def preprocess_list(list, element, context_vars):
    preprocessed_list = []
    for value in list:
        preprocessed_list.append(parse_element(value, element, context_vars))
    return preprocessed_list

def preprocess_special_functions(string, element=None, context_vars=None):
    new_string = string

    while ('@jsonpath(' in new_string) or ('@local(' in new_string) or ('@global(' in new_string) or ('@python(' in new_string):
        if '@jsonpath(' in new_string:
            value = get_formula_content(new_string, '@jsonpath(')
            #pattern with variable jsonpath_string
            pattern = r"@jsonpath\([^)]*\)"
            pre_processed_value = jsonpath_preprocessor.pre_process(value, element)
            
        elif '@local(' in new_string:
            value = get_formula_content(new_string, '@local(')
            pattern = r"@local\([^)]*\)"
            pre_processed_value = local_preprocessor.pre_process(value, context_vars)
            
        elif '@global(' in new_string:
            value = get_formula_content(new_string, '@global(')
            pattern = r"@global\([^)]*\)"
            pre_processed_value = global_preprocessor.pre_process(value, context_vars)

        elif '@python(' in new_string:
            value = get_formula_content(new_string, '@python(')
            pattern = r"'@python\([^)]*\)"
            pre_processed_value = python_preprocessor.pre_process(value)
            
        new_string = re.sub(pattern, 
                            pre_processed_value, 
                            new_string, 
                            count=1)
    return new_string

def get_formula_content(string, formula_delimiter):
    return string.split(formula_delimiter)[1].split(')')[0]