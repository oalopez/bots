from common.interpreter.formula_executor import execute_node

def simple(value, default_value, json_data=None):
    """
    Simple mapping function. 
    """
    value = execute_node(node_json=value, json_data=json_data)
    if not value:
        return default_value
    else:
        return value