from common.enums import ExtractionType
from common.utils.exceptions import InvalidTypeException

def extract(json_config, context_vars, part=0):
    # Read $extraction.type and depending on it, call the corresponding extractor
    rules = json_config['extraction']['rules']
    extraction_type = json_config['extraction']['type']
    
    if extraction_type == ExtractionType.JSON_ALL_RECORDS.value:
        from extractor.type.json_all_records import extract
        return extract(rules, context_vars, part)
    else:
        raise InvalidTypeException("Extraction type: " + extraction_type + " is not supported")