import os
from common.global_state import GlobalStateKeys, global_state
from common.interpreter.formula_executor import execute_node

def generate_output(df, config_json, output_id=None, cache=None):
    rules = config_json['output']['rules']
    
    if not output_id:
        output_id = execute_node(rules['file-name-value'])

    output_folder = rules['folder']
    output_separator = rules['separator']
    output_encoding = rules['encoding']
    dataframe_to_output_mapping = rules['dataframe-to-output']

    # "dataframe-to-output": [
    #             {"field-name": "Marca"},
    #             {"field-name": "Departamento"},
    #             {"field-name": "Codigo_departamento"},
    #             {"field-name": "Municipio"},
    #             {"field-name": "Codigo_municipio"},
    #             {"field-name": "Código_parametro"},
    #             {"field-name": "Parametro"},
    #             {"field-name": "Ano_parametro"},
    #             {"field-name": "Mes_parametro"},
    #             {"field-name": "Codigo_valor"},
    #             {"field-name": "Valor"},
    #             {"field-name": "Poligono"},
    #             {"field-name": "NumId", "transformation": {"type": "int"}},
    #             {"field-name": "Area"},
    #             {"field-name": "Fecha_extraccion"}
    #         ]
    #     }

    # iterate dataframe_to_output_mapping and create a list of output_field_mapping
    output_field_mapping = []
    for mapping in dataframe_to_output_mapping:
        output_field_mapping.append(mapping['field-name'])

    df = df[output_field_mapping]
    df.reset_index(drop=True, inplace=True)

    # save to csv
    to_custom_csv_append(df, output_folder, output_id, output_separator, output_encoding)
        
    return output_id


import os

def to_custom_csv_append(df, foldername, filename, sep, encoding):

    base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)
    
    # if folder name starts with /, it is considered an absolute path
    # otherwise, it is considered a relative path and is appended to the base directory
    if not foldername.startswith('/'):
        foldername = os.path.join(base_directory, foldername)

    # Create folder if it does not exist
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    # Check if file exists to decide on writing header
    file_exists = os.path.isfile(os.path.join(base_directory, foldername, filename))
        
    # Convert DataFrame to CSV string with custom separator
    csv_string = '\n'.join([sep.join(map(str, row)) for row in df.values])
    
    # Add column headers if file does not exist
    if not file_exists:
        header = sep.join(df.columns)
        csv_string = header + '\n' + csv_string

    # Create directory if it does not exist
    if not os.path.exists(os.path.join(base_directory, foldername)):
        os.makedirs(os.path.join(base_directory, foldername))
        
    # Append to file
    with open(os.path.join(base_directory, foldername, filename), 'a', encoding=encoding) as file:
        file.write(csv_string + '\n')
