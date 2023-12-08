from jsonpath_ng import parse, jsonpath

def pre_process(json, jsonpath_string):
    """
    Pre-process function. 
    """
    jsonpath_expr = parse(jsonpath_string)
    matches = jsonpath_expr.find(json)
    return matches.value