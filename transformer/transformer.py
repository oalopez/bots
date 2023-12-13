import jsonpath_ng as jp
from transformer.type.simple import simple
from transformer.type.regex import regex
from transformer.type.json_source import json_source
from common.enums import TransformationType
from common.preprocessor.preprocessor import parse_element
import pandas as pd


def transform(transformer_json, extracted_json_output, context_vars):

    df = pd.DataFrame()
    jsonpath_expression = jp.parse(transformer_json['elements-iterator-jsonpath'])
    # Iterate over all elements from json source
    for index, element in enumerate(jsonpath_expression.find(extracted_json_output)):
        for field_mapping in transformer_json['field-mappings']: 
            field_name = field_mapping['field-name']
            optional = field_mapping['optional']
            transformation_element_parsed = parse_element(field_mapping['transformation'], element, context_vars)
            calculated_value = process_transformation(transformation_element_parsed, element)
            if calculated_value is None and not optional:
                raise Exception('Field ' + field_name + ' is required')

            # Add calculated value to dataframe. The data frame should have an index with the element id
            df.loc[index, field_name] = calculated_value
            context_vars['local_vars'][field_name] = calculated_value

    return df
        
def process_transformation(transformation, element):
    type = transformation['type']
    default_value = transformation['default-value']
    value = transformation['value']
        
    if type == TransformationType.SIMPLE.value:
        return simple(value, default_value)
    elif type == TransformationType.REGEX.value:
        return regex(value['element'], value['pattern'], value['replacement'], default_value)
    elif type == TransformationType.JSON_SOURCE.value:
        return json_source(value['source'], value['element-to-extract'], default_value)