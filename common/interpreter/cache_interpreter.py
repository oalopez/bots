import csv
import os

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
    # Check if the cache exists, if not create it
    if cache_type == CacheSourceType.JSON.value: 
        #TODO: Implement json cache loading from url
        pass
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
        base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)
        with open(os.path.join(base_directory, source)) as csv_file:
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