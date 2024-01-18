import jsonpath_ng as jp
import pandas as pd
import logging

from transformer.type.simple import simple
from transformer.type.regex import regex
from transformer.type.json_source import json_source
from transformer.type.cache import cache
from transformer.type.geometry import geometry
from shapely.geometry import Polygon

from common.enums import TransformationType
from common.utils.exceptions import RequiredFieldException, InvalidTypeException, handle_transformation_exception
from common.utils.profiling import lap_time

logger = logging.getLogger(__name__)

@lap_time(tolerance=5)
def transform(extracted_json_output, parsed_transformer, transformer_caches, pbar=None):

    df = pd.DataFrame()
    jsonpath_expression = jp.parse(parsed_transformer['elements-iterator-jsonpath'])
    
    for index, element in enumerate(jsonpath_expression.find(extracted_json_output)):
        
        # get the actual json element
        element = element.value

        for field_mapping in parsed_transformer['field-mappings']: # cambiar por iterar un dict de mapeo de funciones precargada

            field_name = field_mapping['field-name']
            optional = field_mapping['optional']
            transformed_value = None
            try:            
                exception_strategy = None if 'exception-strategy' not in field_mapping else field_mapping['exception-strategy']
                transformed_value = transform_by_type(element, field_mapping['transformation'], field_name, optional, transformer_caches)
            except RequiredFieldException as rfe:
                handle_transformation_exception(rfe, exception_strategy)

            # Add calculated value to dataframe. The data frame should have an index with the element id
            df.loc[index, field_name] = transformed_value
            #context_vars['local_vars'][field_name] = transformed_value
        
        pbar.update(1)

    try: 
        save_partial_results(df)
    except Exception as e:
        logger.error(f"Error saving partial results dataframe: {e}")

    return df


@lap_time(tolerance=1)        
def transform_by_type(element, transformation, field_name, optional=False, caches=None):
    type = transformation['type']
    default_value = transformation['default-value']
    value = transformation['value']
    calculated_value = None
        
    if type == TransformationType.SIMPLE.value:
        calculated_value = simple(value=value, default_value=default_value, json_data=element)
    
    elif type == TransformationType.CACHE.value:
        calculated_value =  cache(caches, 
                                  cache_name=value['cache-name'], 
                                  value_to_find=value['value-to-find'], 
                                  element=element,
                                  default_value=default_value)
    
    elif type == TransformationType.GEOMETRY.value:
        arguments = {
            "geometry": value['geometry'],
            "element": element,
            "source_format": value['source-format'],
            "target_format": value['target-format']
        }
        # Avoid key error when value['source-crs'] is not defined
        if 'source-crs' in value:
            arguments['source_crs'] = value['source-crs']

        if 'target-crs' in value:
            arguments['target_crs'] = value['target-crs']

        calculated_value = geometry(**arguments)
        # if calculated_value is instance of Polygon and it is empty, return None
        if isinstance(calculated_value, Polygon) and calculated_value.is_empty:
            calculated_value = None


    else:
        raise InvalidTypeException(f"Transformation type '{type}' not supported")
    
    if calculated_value is None and not optional:
        raise RequiredFieldException(f"Field {field_name} is required. Transformation: {transformation}")

    return calculated_value


def save_partial_results(partial_results_df):
    #TODO: implement for retries strategy (its possible that the code is already prepared for this, 
    #       because the file is saved with partial results)
    pass
    # base_directory = GlobalState.get_value(GlobalStateKeys.BASE_DIRECTORY)
    # #dump transformed_df to csv. Append to csv if it exists. Do not include the index
    # partial_results_df.to_csv(base_directory + 'data/transformed_df_' + 
    #                           str(now) + '.csv', 
    #                           mode='a', 
    #                           header=False if part > 0 else True, index=False)
            