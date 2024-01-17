import requests
import jsonpath_ng as jp
from common.enums import PaginationType, StopSequenceType
from common.utils.exceptions import InvalidTypeException

def extract(rules, part=0):
    json_all_records = []

    # 1. Read $.url, $.method, and $.params.* from rules object. 
    # TODO: think it could be a set of rules when need to extract several places - i.e. superservicios)

    source = rules['source'] 
    method = rules['method']
    params = rules['params']
    http_success_code = rules['success-code'] #200

    # 2. Read $.pagination.* from json object if exists
    pagination = rules['pagination'] if 'pagination' in rules else None

    # 3. If pagination is not null, add pagination params to params object
    if pagination:
        pagination_type = pagination['type']
        stop_sequece = pagination['stop-sequence']

        if stop_sequece['type'] == StopSequenceType.PAGE_LIMIT.value:
            page_limit = stop_sequece['limit']
            if part >= int(page_limit):
                return []
        elif stop_sequece['type'] == StopSequenceType.NO_MORE_RECORDS.value:
            pass # it will be evaluated again at the end of the function. After the request
        else:
            raise InvalidTypeException("Stop sequence type: " + stop_sequece['type'] + " is not supported")

        pagination_params = {}
        if pagination_type == PaginationType.PARAMS.value:
            step_size = int(pagination['next']['step-value'])
            offset_start = int(pagination['next']['offset-start-value'])
            pagination_params[pagination['next']['offset-param-name']] = step_size * part + offset_start
            pagination_params[pagination['next']['step-param-name']] = step_size
            # Update params with pagination params
            params.update(pagination_params)
        else:
            raise InvalidTypeException("Pagination type: " + pagination_type + " is not supported")

    # 4. Go to URL and get json object
    if method.lower() == "get":
        response = requests.get(source, params=params)
    elif method.lower() == "post":
        response = requests.post(source, data=params)
    else:
        raise ValueError("Invalid method: " + method)

    # 5. Check if response status code is 200
    if response.status_code != int(http_success_code):
        raise Exception("HTTP error code: " +
                         str(response.status_code) + 
                         ". Message: " + response.text + 
                         ". Source: " + source + 
                         ". Params: " + str(params))
    
    # 5. Append json object to json_all_records
    json_all_records.append(response.json())

    # 6. Check if pagination is not null and stop-sequence is NO_MORE_RECORDS. If so, check if jsonpath is empty. If so, return empty list.
    if pagination:
        pagination_type = pagination['type']
        stop_sequece = pagination['stop-sequence']
        if stop_sequece['type'] == StopSequenceType.NO_MORE_RECORDS.value:
                empty_element_eval = stop_sequece['empty-element-jsonpath']
                empty_element_value = jp.parse(empty_element_eval).find(response.json())
                if len(empty_element_value) == 0:
                    return []   

    # 7. Return json_all_records
    return json_all_records

