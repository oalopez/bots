from jsonpath_ng import parse, jsonpath

def interpret(jsonpath_string, json):
    """
    Pre-process function. 
    """
    jsonpath_expr = parse(jsonpath_string)
    matches = jsonpath_expr.find(json)
    return matches[0].value if matches else None