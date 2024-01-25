import csv
import os

from common.utils.exceptions import InvalidTypeException
from common.enums import InputType
from common.global_state import GlobalStateKeys, global_state


def total_records(input_definition):
    
    total_records = 0
    
    if input_definition is None:
        raise ValueError("Input definition not found in extractor.json")

    input_type = input_definition['type']
    if input_type == InputType.CSV.value:
        total_records = total_records_csv(input_definition)
    else:
        raise InvalidTypeException("Input type: " + input_type + " is not supported")

    if total_records == 0:
        raise Exception("No total records for input definition")
    
    return total_records


def total_records_csv(input_definition):
    total_records = 0
    file_name_path = input_definition['rules']['source']

    # if source starts with /, it is an absolute path, else it is a relative path to the base directory
    if not file_name_path.startswith('/'):
        base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)
        file_name_path = os.path.join(base_directory, file_name_path)
        
    if not os.path.isfile(file_name_path):
        raise ValueError("File path: " + file_name_path + " not found")
    with open(file_name_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            total_records += 1

    # remove header
    return total_records - 1