import requests
import jsonpath_ng as jp
from common.interpreter.formula_executor import execute_node

def total_records(tr_element):
    
    total_records = 0
    method = tr_element['value']['method']
    source = tr_element['value']['source']
    params = tr_element['value']['params']

    calculated_params = {}
    for param in params:
        calculated_params[param] = execute_node(node_json=params[param])

    

    if method.lower() == "get":
        response = requests.get(source, params=calculated_params)
    elif method.lower() == "post":
        response = requests.post(source, data=calculated_params)
    else:
        raise ValueError("Invalid method: " + method)

    # Check if response status code is 200
    if response.status_code != 200:
        raise Exception("HTTP error code: " +
                         str(response.status_code) + 
                         ". Message: " + response.text + 
                         ". Source: " + source + 
                         ". Params: " + str(calculated_params))
    try:
        jsonpath_expression = jp.parse(tr_element['value']['element-jsonpath'])
        total_records = jsonpath_expression.find(response.json())
        # get the first element
        total_records = total_records[0].value

    except Exception as e:
        raise Exception("Error parsing jsonpath: " + str(e) + 
                        ". Source: " + source + 
                        ". Params: " + str(calculated_params) + 
                        ". Response: " + str(response.json()))
    
    if not total_records or total_records == 0:
        raise Exception("No total records found. Source: " + source + 
                        ". Params: " + str(calculated_params) + 
                        ". Response: " + str(response.json()))
    
    return total_records