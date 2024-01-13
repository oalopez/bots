import json
import os
import csv
import requests
import jsonpath_ng as jp
import common.utils.exceptions as InvalidTypeException
import common.interpreter.interpreter as interpreter

from common.enums import CacheSourceType
from common.utils.profiling import lap_time

# Global dictionary to hold all caches
caches = {}

@lap_time(tolerance=1)
def cache(base_directory, cache_name, cache_definition, value_to_find, default_value):
    # Check if the cache exists, if not create it
    if cache_definition['source-type'] == CacheSourceType.JSON.value: 
        if cache_name not in caches:
            # Initialize the cache
            caches[cache_name] = load_new_json_cache(base_directory, cache_definition)
    elif cache_definition['source-type'] == CacheSourceType.CSV.value:
        if cache_name not in caches:
            # Initialize the cache
            caches[cache_name] = load_new_csv_cache(base_directory, cache_definition)
    else:
        raise InvalidTypeException('Cache type ' + cache_definition['source-type'] + ' not supported')

    # Get the cache
    cache = caches[cache_name]

    # Find the value in the cache
    # concatenate the strings of value_to_find with a _
    cache_key = 'PK_' + '_'.join(key_str for key_str in value_to_find)

    if cache_key in cache:
        return cache[cache_key]
    else:
        return default_value

def load_new_json_cache(base_directory, cache_definition):
    cache_keys = cache_definition['keys']
    cache_value = cache_definition['value']
    source = cache_definition['source']
    namespace = cache_definition['namespace'] if 'namespace' in cache_definition else ''

    if source.startswith('http'):
        json_data = load_json_url(source)
    else:
        json_data = load_json_file(base_directory, source)

    # Given cache_keys as a list of jsonpaths (e.g. ["$.[0].cod_entidad", "$.[0].tipo_entidad"])
    # and cache_value as a jsonpath string (e.g. "$.[0].numeroidentificacion")
    # create a dictionary with the following structure:
    # {
    #   "cod_entidad_tipo_entidad": "numeroidentificacion"
    # }
    # where cod_entidad_tipo_entidad is the concatenation of the values of the jsonpaths in cache_keys
    # and numeroidentificacion is the value of the jsonpath in cache_value
    cache = {}
    for element in json_data:
        cache_key = 'PK'
        for key in cache_keys:
            cache_key = cache_key + "_" + interpreter.parse_element(base_directory, key, element, None, namespace)
        cache[cache_key] = interpreter.parse_element(base_directory, cache_value, element, None, namespace)
    return cache

def load_json_file(base_directory, filename):
    with open(os.path.join(base_directory, filename)) as json_file:
        data = json.load(json_file)
        return data
    
def load_json_url(url):
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def load_new_csv_cache(base_directory, cache_definition):
    cache_keys = cache_definition['keys']
    cache_value = cache_definition['value']
    source = cache_definition['source']
    namespace = cache_definition['namespace'] if 'namespace' in cache_definition else ''

    if source.startswith('http'):
        #csv_data = load_csv_url(source)
        pass #TODO: Implement csv cache loading from url
    else:
        with open(os.path.join(base_directory, source)) as csv_file:
            data = csv.DictReader(csv_file)
            cache = {}
            for row in data:
                cache_key = 'PK'
                for key in cache_keys:
                    key_value = row[key]
                    cache_key = cache_key + "_" + interpreter.parse_element(base_directory, key_value, element=None, context_vars=None, namespace=namespace)
                # get the value of row[cache_value]
                value = row[cache_value]
                if cache_key not in cache:
                    cache[cache_key] = interpreter.parse_element(base_directory, value, element=None, context_vars=None, namespace=namespace)

    return cache
