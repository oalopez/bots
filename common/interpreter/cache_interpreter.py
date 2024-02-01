import csv
import os
import json
import jsonpath_ng as jp

from common.utils.exceptions import InvalidTypeException
from common.enums import CacheSourceType
from common.global_state import GlobalStateKeys, global_state

def load_caches(json_data):
    # Find all the cache definitions in the JSON and iterate over them. ("type": "cache"). Example:
    # {
    # [{
    #         "field-name": "Código_parametro",
    #         "description": "Mapeo segun Catalogo de Parámetros definido con Experian",
    #         "optional": false,
    #         "transformation": {
    #             "type": "cache",
    #             "value": {
    #                 "value-to-find": ["exclusiones"],
    #                 "cache-definition": {
    #                     "source": "cache/parametros.csv",
    #                     "source-type": "csv",
    #                     "strategy": "full",
    #                     "keys": ["nombre_parametro"],
    #                     "value": "codigo_parametro"
    #                 }
    #             },
    #             "default-value": null,
    #             "exception-strategy": "ignore"
    #         }
    #     }
    # ]
    # }
    caches = {}

    # Iterate over the json and find all the cache definitions
    if 'cache-definition' in json_data:
        for cache_definition in json_data['cache-definition']:
            cache_name = cache_definition['name']
            if cache_name not in caches:
                caches[cache_name] = load_cache(cache_name, cache_definition)
    
    return caches

def load_cache(cache_name, cache_definition):
    cache_type = cache_definition['type']
    cache = None
    # Check if the cache exists, if not create it
    if cache_type == CacheSourceType.JSON.value: 
        cache = load_json_cache(cache_definition['rules'])
    elif cache_type == CacheSourceType.CSV.value:
        # Initialize the cache
        cache = load_csv_cache(cache_definition['rules'])
    else:
        raise InvalidTypeException('Cache type ' + cache_definition['source-type'] + ' not supported')
    
    return cache
    
def load_csv_cache(cache_rules):
    cache_keys = cache_rules['keys']
    cache_value = cache_rules['value']
    source = cache_rules['source']
    
    if source.startswith('http'):
        #csv_data = load_csv_url(source)
        pass #TODO: Implement csv cache loading from url
    else:

        # if source starts with /, it is an absolute path, else it is a relative path to the base directory
        if source.startswith('/'):
            directory = source
        else:
            base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)
            directory = os.path.join(base_directory, source)
            
        with open(os.path.join(directory, source)) as csv_file:
            data = csv.DictReader(csv_file)
            cache = {}
            for row in data:
                cache_key = 'PK'
                for key in cache_keys:
                    key_value = row[key]
                    cache_key = cache_key + "_" + key_value
                # get the value of row[cache_value]
                value = row[cache_value]
                if cache_key not in cache:
                    cache[cache_key] = value

    return cache

def load_json_cache(cache_rules):
    jsonpath_keys = cache_rules['jsonpath-keys']
    jsonpath_value = cache_rules['jsonpath-value']
    source = cache_rules['source']

    if source.startswith('http'):
        #json_data = load_json_url(source)
        pass #TODO: Implement json cache loading from url
    else:
        if source.startswith('/'):
            filepath = source
        else:
            base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)
            filepath = os.path.join(base_directory, source)
        
        with open(filepath) as json_file:
            data = json.load(json_file)
            cache = {}
            for row in data:
                cache_key = 'PK'
                for jp_key in jsonpath_keys:
                    jsonpath_expression = jp.parse(jp_key)
                    matches = jsonpath_expression.find(row)
                    if matches:
                        key_value = matches[0].value
                        cache_key = cache_key + "_" + key_value
                    else:
                        raise ValueError(f"Jsonpath query for cache '{jp_key}' did not match any data")
                jsonpath_expression = jp.parse(jsonpath_value)
                matches = jsonpath_expression.find(row)
                if matches:
                    value = matches[0].value
                else:
                    raise ValueError(f"Jsonpath query for cache '{jsonpath_value}' did not match any data")

                if cache_key not in cache:
                    cache[cache_key] = value
    return cache