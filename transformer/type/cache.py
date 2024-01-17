import logging

import common.utils.exceptions as InvalidTypeException
from common.utils.profiling import lap_time
from common.interpreter.formula_executor import execute_node

logger = logging.getLogger(__name__)

# Global dictionary to hold all caches
caches = {}

@lap_time(tolerance=1)
def cache(caches, cache_name, value_to_find, element, default_value):


    # Check if the cache exists, if not raise an exception
    if cache_name not in caches:
        raise Exception('Cache ' + cache_name + ' not found')
    
    cache = caches[cache_name]

    # use execute_node to evaluate the value_to_find which is a list. Iterate over the list and evaluate each element
    value_to_find = [execute_node(value, element) for value in value_to_find]
    
    # Find the value in the cache
    cache_key = 'PK_' + '_'.join(key_str for key_str in value_to_find)
    if cache_key in cache:
        return cache[cache_key]
    else:
        logger.warn('Value not found in cache "{0}" for key "{1}"'.format(cache_name, cache_key))
        return default_value