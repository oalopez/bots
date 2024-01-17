import sys
import jsonpath_ng as jp
import importlib
from common.interpreter.formula_parser import parse_formula, Node
from common.global_state import GlobalStateKeys, global_state

if '.' not in sys.path:
    sys.path.append('.')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def execute_node(node_json, json_data=None):

    base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)

    # if is instance of Node, convert to json
    if not isinstance(node_json, Node):
        node = Node()
        node.from_json(node_json)
    else:  
        node = node_json

    if base_directory not in sys.path:
        sys.path.append(base_directory)

    if node.value == 'jsonpath':
        jsonpath_expression = jp.parse(node.children[0].value)
        matches = jsonpath_expression.find(json_data)
        if matches:
            return matches[0].value
        else:
            raise ValueError(f"Jsonpath query '{node.children[0].value}' did not match any data")
    else:
        module = importlib.import_module("custom_functions")
        func = getattr(module, node.value, None)
        
        # if the function is not found in the custom_functions module of the specific bot, use the default custom_functions module
        if not (func and callable(func)):
            # look for the function in the custom_functions module
            module = importlib.import_module("common.custom_functions")
            func = getattr(module, node.value, None)
        
        if func and callable(func):
            args = []
            for child in node.children:
                if child.value.startswith("'") and child.value.endswith("'"):
                    # It's a string literal
                    args.append(child.value[1:-1])  # Remove the quotes
                elif is_number(child.value):
                    # It's a numeric literal
                    args.append(float(child.value) if '.' in child.value else int(child.value))
                else:
                    # It's another function call or variable
                    result = execute_node(child, json_data)
                    args.append(result)
            return func(*args)
        else:
            raise ValueError(f"Function '{node.value}' not defined in module 'custom_functions'")
