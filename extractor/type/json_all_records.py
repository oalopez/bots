import requests
import jsonpath_ng as jp
import logging
import json
from common.enums import PaginationType, StopSequenceType, JsonErrorActionType
from common.utils.exceptions import InvalidTypeException, JsonResponseError

logger = logging.getLogger(__name__)

def extract(rules, part=0):
    json_all_records = []

    # 1. Read $.url, $.method, and $.params.* from rules object. 
    # TODO: think it could be a set of rules when need to extract several places - i.e. superservicios)

    source = rules['source'] 
    method = rules['method']
    params = rules['params']
    error_jsonpath = rules['error-response-jsonpath'] if 'error-response-jsonpath' in rules else None
    error_action = rules['error-action'] if 'error-action' in rules else None

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

    try:
        # 4. Go to URL and get json object
        if method.lower() == "get":
            response = requests.get(source, params=params)
        elif method.lower() == "post":
            response = requests.post(source, data=params)
        else:
            raise ValueError("Invalid method: " + method)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error requesting URL: {source}, method: {method}, params: {params}. Error: {e}")
        raise e

    # 5. Check if response status code is 200
    try:
        logger.info(f"Extracting part: {part}, url: {source}, method: {method}, params: {params}")
        json_all_records.append(response.json())

        # 5.1 Check if error jsonpath is not empty. If so, raise exception
        error_value = jp.parse(error_jsonpath).find(response.json())
        if len(error_value) > 0:
            if error_action == JsonErrorActionType.SKIP.value:
                logger.warning(f"Error given by the server : {part}, url: {source}, method: {method}, params: {params}. Error: {error_value}")
                raise JsonResponseError(f"Error given by the server : {part}, url: {source}, method: {method}, params: {params}. Error: {error_value}", 
                                        should_continue=True)
            elif error_action == JsonErrorActionType.STOP.value:
                logger.error(f"Error given by the server : {part}, url: {source}, method: {method}, params: {params}. Error: {error_value}")
                raise JsonResponseError(f"Error given by the server : {part}, url: {source}, method: {method}, params: {params}. Error: {error_value}", 
                                        should_continue=False)
            else:
                raise InvalidTypeException("Json Error action: " + error_action + " is not supported")

    except json.decoder.JSONDecodeError as e:
        logger.error(f"Error decoding json response. Part: {part}, url: {source}, method: {method}, params: {params}. Error: {e}")
        raise e
    
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

