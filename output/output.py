from common.enums import OutputType, OutputTransformationType
from common.utils.exceptions import InvalidTypeException
from common.utils.profiling import lap_time
import pandas as pd


@lap_time(tolerance=2)
def output(transformed_df, output_json, output_id=None, caches=None):

    output_type = output_json['output']['type']

    dataframe_type_transformations(transformed_df, output_json)
    
    if output_type == OutputType.CSV.value:
        from output.type.csv import generate_output
        return generate_output(transformed_df, output_json, output_id, caches)
    else:
        raise InvalidTypeException("Output type: " + output_type + " is not supported")
    

def dataframe_type_transformations(df, output_json):

    try:
        df_to_output = output_json['output']['rules']['dataframe-to-output']
    except KeyError:
        raise InvalidTypeException("Invalid JSON structure: 'output.rules.dataframe-to-output' key not found")
    
    for field in df_to_output:
        if 'transformation' in field:
            transformation = field['transformation']
            if 'type' in transformation:
                transformation_type = transformation['type']
                field_name = field['field-name']
                if transformation_type == OutputTransformationType.CAST.value:
                    to = transformation['rules']['to']
                    if to == 'int':
                        df[field_name] = df[field_name].astype(int)
                    elif to == 'float':
                        df[field_name] = df[field_name].astype(float)
                    elif to == 'string':
                        df[field_name] = df[field_name].astype(str)
                    elif to == 'date':
                        df[field_name] = pd.to_datetime(df[field_name], format=transformation['format'])
                    elif to == 'boolean':
                        df[field_name] = df[field_name].astype(bool)
                    else:
                        raise InvalidTypeException("Transformation type: " + transformation_type + "(" + to + ") is not supported")
                
                elif transformation_type == OutputTransformationType.TRUNCATE.value:
                    size = transformation['rules']['size']
                    side = transformation['rules']['side']
                    if side == 'left':
                        df[field_name] = df[field_name].str[:size]
                    elif side == 'right':
                        df[field_name] = df[field_name].str[-size:]
                    else:
                        raise InvalidTypeException("Transformation type: " + transformation_type + "(" + side + ") is not supported")
            else:
                raise InvalidTypeException("Transformation type is not defined")