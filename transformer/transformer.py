import jsonpath_ng as jp
from transformer.type.simple import simple
from transformer.type.regex import regex
from transformer.type.json_source import json_source
from transformer.type.cache import cache
from common.enums import TransformationType
from common.preprocessor.preprocessor import parse_element
from common.utils.exceptions import RequiredFieldException, InvalidTypeException, handle_transformation_exception
import pandas as pd


def transform(transformer_json, extracted_json_output, context_vars):

    df = pd.DataFrame()
    jsonpath_expression = jp.parse(transformer_json['elements-iterator-jsonpath'])
    # Timestamp for performance
    timestamp = pd.Timestamp.now()

    # Iterate over all elements from json source

    # for this expression jsonpath_expression.find(extracted_json_output) return only the 1st element
    # for element in jsonpath_expression.find(extracted_json_output):
    #     print(element.value)
    

    for index, element in enumerate(jsonpath_expression.find(extracted_json_output)):
        if(index % 100 == 0):
            print('Processing element ' + str(index) + ". Time elapsed: " + str(pd.Timestamp.now() - timestamp))

        for field_mapping in transformer_json['field-mappings']: 
            field_name = field_mapping['field-name']
            optional = field_mapping['optional']
            transformation_element_parsed = parse_element(field_mapping['transformation'], element.value, context_vars)
            calculated_value = None
            try:            
                strategy = None if 'exception-strategy' not in transformation_element_parsed else transformation_element_parsed['exception-strategy']
                calculated_value = calculate_transformation(field_name, transformation_element_parsed, optional)
            except RequiredFieldException as rfe:
                handle_transformation_exception(rfe, strategy)

            # Add calculated value to dataframe. The data frame should have an index with the element id
            df.loc[index, field_name] = calculated_value
            context_vars['local_vars'][field_name] = calculated_value

    return df
        
def calculate_transformation(field_name, transformation, optional=False):
    type = transformation['type']
    default_value = transformation['default-value']
    value = transformation['value']
    calculated_value = None
        
    if type == TransformationType.SIMPLE.value:
        calculated_value = simple(value=value, 
                      default_value=default_value)
    
    elif type == TransformationType.REGEX.value:
        calculated_value =  regex(element=value['element'], 
                     pattern=value['pattern'], 
                     replacement=value['replacement'], 
                     default_value=default_value)
    
    elif type == TransformationType.JSON_SOURCE.value:
        calculated_value =  json_source(source=value['source'], 
                           element_to_extract=value['element-to-extract'], 
                           default_value=default_value)
    
    elif type == TransformationType.CACHE.value:
        calculated_value =  cache(cache_name=field_name, 
                     cache_definition=value['cache-definition'], 
                     value_to_find=value['value-to-find'], 
                     default_value=default_value)
    
    else:
        raise InvalidTypeException(f"Transformation type '{type}' not supported")
    
    if calculated_value is None and not optional:
        raise RequiredFieldException(f"Field {field_name} is required. Transformation: {transformation}")

    return calculated_value