import requests
import jsonpath_ng as jp
import logging
import json
from common.enums import JsonErrorActionType
from common.utils.exceptions import InvalidTypeException, JsonResponseError
from common.interpreter.formula_executor import execute_node
from common.global_state import GlobalStateKeys, global_state

logger = logging.getLogger(__name__)

def extract(rules):

    # get the current input row and total records
    current_input_row = global_state.get_value(GlobalStateKeys.CURRENT_INPUT_PART)
    total_records = global_state.get_value(GlobalStateKeys.TOTAL_RECORDS)
    if current_input_row > total_records - 1:
        return []

    json_record = []

    source = rules['source'] 
    method = rules['method']
    params = rules['params']
    error_jsonpath = rules['error-response-jsonpath'] if 'error-response-jsonpath' in rules else None
    error_action = rules['error-action'] if 'error-action' in rules else None

    # for every param, execute the node
    calculated_params = {}
    for param in params:
        calculated_params[param] = execute_node(node_json=params[param])

    source = execute_node(node_json=source)

    # Read $.pagination.* from json object if exists
    pagination = rules['pagination'] if 'pagination' in rules else None

    # No pagination for this type of extraction

    try:
        # Go to URL and get json object
        if method.lower() == "get":
            response = requests.get(source, params=calculated_params)
        elif method.lower() == "post":
            response = requests.post(source, data=calculated_params)
        else:
            raise ValueError("Invalid method: " + method)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error requesting URL: {source}, method: {method}, params: {calculated_params}. Error: {e}")
        raise e

    # Get response json object
    try:
        logger.info(f"Extracting url: {source}, method: {method}, params: {calculated_params}")
        json_record.append(response.json())

        # 5.1 Check if error jsonpath is not empty. If so, raise exception
        if error_jsonpath:
            error_value = jp.parse(error_jsonpath).find(response.json())
            if len(error_value) > 0:
                err_msg = f"Error given by the server : url: {source}, method: {method}, params: {calculated_params}. Error: {error_value}"
                if error_action == JsonErrorActionType.SKIP.value:
                    logger.warning()
                    raise JsonResponseError(err_msg, should_continue=True)
                elif error_action == JsonErrorActionType.STOP.value:
                    logger.error(err_msg)
                    raise JsonResponseError(err_msg, should_continue=False)
                else:
                    raise InvalidTypeException("Json Error action: " + error_action + " is not supported")

    except json.decoder.JSONDecodeError as e:
        logger.error(f"Error decoding json response. url: {source}, method: {method}, params: {calculated_params}. Error: {e}")
        raise e
    
    # 7. Return json_all_records
    return json_record

