# main.py

import json
import os
import time
import tqdm
import argparse

from extractor.extractor import extract, total_records
from transformer.transformer import transform
from output.output import generate_output

from common.utils.logging_config import setup_logger
from common.utils.profiling import lap_time

# TODO: Handle context_vars correctly
global_vars={"_year":"2022"}
local_vars = {}

context_vars = {"global_vars": global_vars, 
                "local_vars": local_vars}

def process(base_directory):
    setup_logger(base_directory)

    extractor_path = os.path.join(base_directory, 'extractor.json')
    transformer_path = os.path.join(base_directory, 'transformer.json')
    output_path = os.path.join(base_directory, 'output.json')

    if not os.path.isfile(extractor_path):
        raise Exception('Extractor file does not exist')

    if not os.path.isfile(transformer_path):
        raise Exception('Transformer file does not exist')
    
    if not os.path.isfile(output_path):
        raise Exception('Loader file does not exist')
    
    with open(extractor_path) as extractor_file:
        extractor_json = json.load(extractor_file)
    
    with open(transformer_path) as transformer_file:
        transformer_json = json.load(transformer_file)

    with open(output_path) as output_file:
        output_json = json.load(output_file)
    
    #parsed_extractor_json = parse_json_file(extractor_json)
    #parsed_transformer_json = parse_json_file(transformer_json)
    #parsed_output_json = parse_json_file(output_json)

    total_records_count = total_records(base_directory, extractor_json, context_vars)
    extracted_output_page = extract(base_directory, extractor_json, context_vars)
    now = time.time()
    part = 0

    output_id = None
    with tqdm.tqdm(total=int(total_records_count), desc="Processing", unit=' records', colour='green') as pbar:
        while extracted_output_page:
            transformed_df = transform(base_directory, transformer_json, extracted_output_page, context_vars)
            #dump transformed_df to csv. Append to csv if it exists. Do not include the index
            transformed_df.to_csv('data/transformed_df_' + str(now) + '.csv', mode='a', header=False if part > 0 else True, index=False)
            #TODO: improve return type of generate_output. Handle errors better
            output_id = generate_output(base_directory, output_json, transformed_df, context_vars, output_id)
            # Update the progress bar
            pbar.update(transformed_df.shape[0])
            #get next page
            part += 1
            extracted_output_page = extract(base_directory, extractor_json, context_vars, part)
            
    pbar.close()

    print("Done!")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bot input files.')
    parser.add_argument('base_directory', type=str, help='Base directory containing the JSON files (output.json, extractor.json, transformer.json)')
    
    args = parser.parse_args()
    process(args.base_directory)