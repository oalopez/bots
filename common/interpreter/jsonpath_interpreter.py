from jsonpath_ng import parse, jsonpath
from common.utils.exceptions import InvalidFormulaException

def interpret(jsonpath_string, json):
    """
    Pre-process function. 
    """
    try:
        jsonpath_expr = parse(jsonpath_string)
        matches = jsonpath_expr.find(json)
        return matches[0].value if matches else None
    except Exception as e:
        raise InvalidFormulaException(f"Error interpreting jsonpath {jsonpath_string}: {e}")
