from common.enums import ExtractionType, TotalRecordsType
from common.utils.exceptions import InvalidTypeException
from common.utils.profiling import lap_time

@lap_time(tolerance=10)
def extract(base_directory, json_config, context_vars, part=0):
    # Read $extraction.type and depending on it, call the corresponding extractor
    rules = json_config['extraction']['rules']
    extraction_type = json_config['extraction']['type']
    
    if extraction_type == ExtractionType.JSON_ALL_RECORDS.value:
        from extractor.type.json_all_records import extract
        return extract(base_directory, rules, context_vars, part)
    else:
        raise InvalidTypeException("Extraction type: " + extraction_type + " is not supported")

@lap_time(tolerance=10)    
def total_records(base_directory, json_config, context_vars):
    # Read $extraction.type and depending on it, call the corresponding extractor
    total_records_element= json_config['extraction']['rules']['total-records'] if 'total-records' in json_config['extraction']['rules'] else None
    
    if not total_records_element:
        return None
    
    tr_type = total_records_element['type']
    if tr_type == TotalRecordsType.JSON.value:
        from extractor.total_records_type.json import total_records
        return total_records(base_directory, total_records_element, context_vars)
    else:
        raise InvalidTypeException("TotalRecords type: " + tr_type + " is not supported")