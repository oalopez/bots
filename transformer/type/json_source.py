import json
import requests
import jsonpath_ng as jp

def json_source(source, element_to_extract, default_value):
    #TODO: Manage cache
    # open URL source and read it
    response = requests.get(source)
    json_data = json.loads(response.text)

    # return the element_to_extract wich is a jsonpath expression
    jsonpath_expression = jp.parse(element_to_extract)

    # if the jsonpath expression is not found, return default_value
    if not jsonpath_expression.find(json_data):
        return default_value
    else:
        return jsonpath_expression.find(json_data)[0].value
