from common.enums import ExtractionType

def extract(json_config, context_vars):
    # Read $extraction.type and depending on it, call the corresponding extractor
    rules = json_config['extraction']['rules']
    extraction_type = json_config['extraction']['type']
    
    if extraction_type == ExtractionType.JSON_ALL_RECORDS.value:
        from extractor.type.json_all_records import extract
        return extract(rules, context_vars)
    else:
        raise ValueError("Invalid extraction.type: " + extraction_type)