from common.enums import OutputType
from common.utils.exceptions import InvalidTypeException
from common.utils.profiling import lap_time


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
                if transformation['type'] == 'int':
                    df[field['field-name']] = df[field['field-name']].astype(int)
                elif transformation['type'] == 'float':
                    df[field['field-name']] = df[field['field-name']].astype(float)
                elif transformation['type'] == 'string':
                    df[field['field-name']] = df[field['field-name']].astype(str)
                elif transformation['type'] == 'date':
                    df[field['field-name']] = pd.to_datetime(df[field['field-name']], format=transformation['format'])
                elif transformation['type'] == 'boolean':
                    df[field['field-name']] = df[field['field-name']].astype(bool)
                else:
                    raise InvalidTypeException("Transformation type: " + transformation['type'] + " is not supported")
            else:
                raise InvalidTypeException("Transformation type is not defined")