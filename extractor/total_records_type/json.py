import requests
import jsonpath_ng as jp
from extractor.type.json_all_records import parse_element

def total_records(tr_element, context_vars):
    
    total_records = 0
    tr_element = parse_element(tr_element, None, context_vars)
    method = tr_element['value']['method']
    source = tr_element['value']['source']
    params = tr_element['value']['params']

    if method.lower() == "get":
        response = requests.get(source, params=params)
    elif method.lower() == "post":
        response = requests.post(source, data=params)
    else:
        raise ValueError("Invalid method: " + method)

    # Check if response status code is 200
    if response.status_code != 200:
        raise Exception("HTTP error code: " +
                         str(response.status_code) + 
                         ". Message: " + response.text + 
                         ". Source: " + source + 
                         ". Params: " + str(params))
    try:
        jsonpath_expression = jp.parse(tr_element['value']['element-jsonpath'])
        total_records = jsonpath_expression.find(response.json())
        # get the first element
        total_records = total_records[0].value

    except Exception as e:
        raise Exception("Error parsing jsonpath: " + str(e) + 
                        ". Source: " + source + 
                        ". Params: " + str(params) + 
                        ". Response: " + str(response.json()))
    
    if not total_records or total_records == 0:
        raise Exception("No total records found. Source: " + source + 
                        ". Params: " + str(params) + 
                        ". Response: " + str(response.json()))
    
    return total_records