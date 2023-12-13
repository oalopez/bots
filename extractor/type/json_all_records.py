import jsonpath_ng as jp
import requests
from common.preprocessor.preprocessor import parse_element


def extract(rules, context_vars):
    json_all_records = []

    # 1. Read $.url, $.method, and $.params.* from rules object. 
    # TODO: think it could be a set of rules when need to extract several places - i.e. superservicios)
    rules_parsed = parse_element(rules, None, context_vars)
    url = rules_parsed['url'] 
    method = rules_parsed['method']
    params = rules_parsed['params']

    # 2. Read $.pagination.* from json object if exists
    pagination = rules['pagination'] if 'pagination' in rules else None

    # 3. Go to URL and get json object
    if method.lower() == "get":
        response = requests.get(url, params=params)
    elif method.lower() == "post":
        response = requests.post(url, data=params)
    else:
        raise ValueError("Invalid method: " + method)

    # 4. If $.pagination.* exists, go to next page
    if pagination:
        # TODO: implement pagination
        pass
    
    # 5. Append json object to json_all_records
    json_all_records.append(response.json())

    # 6. Return json_all_records
    return json_all_records

