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
    output_field_mapping = rules['field-mapping']

    # Delete the columns that are not in the field mapping (fiel+mapping is an array of strings)
    df = df[output_field_mapping]
    df.reset_index(drop=True, inplace=True)

    # save to csv
    to_custom_csv_append(df, output_folder, output_id, output_separator, output_encoding)
        
    return output_id


import os

def to_custom_csv_append(df, foldername, filename, sep, encoding):

    base_directory = global_state.get_value(GlobalStateKeys.CURRENT_BASE_DIR)
    
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
