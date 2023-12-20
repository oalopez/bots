import json
import requests
import jsonpath_ng as jp
import common.utils.exceptions as InvalidTypeException
# Global dictionary to hold all caches
caches = {}

def cache(cache_name, cache_definition, value_to_find, default_value):
    # Check if the cache exists, if not create it
    if cache_definition['source-type'] == 'json': 
        if cache_name not in caches:
            # Initialize the cache
            caches[cache_name] = load_new_json_cache(cache_name, cache_definition)
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

def load_new_json_cache(cache_name, cache_definition):
    cache_keys = cache_definition['keys']
    cache_value = cache_definition['value']
    source = cache_definition['source']

    if source.startswith('http'):
        json_data = load_json_url(source)
    else:
        # TODO: Manage local files
        json_data = load_json_file(source)

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
            cache_key = cache_key + "_" + str(jp.parse(key).find(element)[0].value)
        cache[cache_key] = jp.parse(cache_value).find(element)[0].value
    return cache

def load_json_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data
    
def load_json_url(url):
    response = requests.get(url)
    data = json.loads(response.text)
    return data