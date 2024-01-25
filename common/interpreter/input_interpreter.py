import csv
import os

from common.utils.exceptions import InvalidTypeException
from common.enums import InputType
from common.global_state import GlobalStateKeys, global_state
from common.interpreter.formula_executor import execute_node

def load_input(parsed_extractor_json):
    input_definition = parsed_extractor_json['input-definition'] if 'input-definition' in parsed_extractor_json else None

    if input_definition:
        input_type = input_definition['type']
        rules = input_definition['rules']
        
        if input_type == InputType.CSV.value:
            input = load_csv_input(rules)
        else:
            raise InvalidTypeException('Input type ' + input_type + ' not supported')
        
        return input

    return None
    
def load_csv_input(input_rules):
    input_keys = input_rules['keys']
    input_source = input_rules['source']
    
    # if source starts with /, it is an absolute path, else it is a relative path to the base directory
    if input_source.startswith('/'):
        file_name_path = input_source
    else:
        base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)
        file_name_path = os.path.join(base_directory, input_source)
        
    with open(file_name_path) as csv_file:
        data = csv.DictReader(csv_file)
        input_dict = {}

        # create dict structure: {row_number: {key1: value1, key2: value2, ...}}
        for row_number, row in enumerate(data):
            input_dict[row_number] = {}
            for key in input_keys:
                input_dict[row_number][key] = row[key]

    return input_dict

def input(value):
    """
    Input mapping function. 
    """
    # get the current input row
    current_input_row = global_state.get_value(GlobalStateKeys.CURRENT_INPUT_PART)
    # get the input records
    input_records = global_state.get_value(GlobalStateKeys.INPUT_RECORDS)

    value_to_find = execute_node(node_json=value)
    # get the value from the input records (dict structure: {row_number: {key1: value1, key2: value2, ...}})
    value = input_records[current_input_row][value_to_find]

    return value