# main.py

import json
import os
import tqdm
import argparse
import logging

from extractor.extractor import extract, total_records
from transformer.transformer import transform
from output.output import output

from common.interpreter.cache_interpreter import load_caches
from common.utils.logging_config import setup_logger
from common.utils.profiling import lap_time
from common.interpreter.formula_parser import parse_json_structure
from common.global_state import GlobalStateKeys, global_state

logger = logging.getLogger(__name__)

def process(base_directory):
        
    try:
        global_state.set_value(GlobalStateKeys.CURRENT_BASE_DIR, base_directory)

        setup_logger()
        extractor_json = load_json_file(base_directory, 'extractor.json')
        transformer_json = load_json_file(base_directory, 'transformer.json')
        output_json = load_json_file(base_directory, 'output.json')

        extractor_caches, parsed_extractor_json = parse_json_file(extractor_json)
        transformer_caches, parsed_transformer_json = parse_json_file(transformer_json)
        output_caches, parsed_output_json = parse_json_file(output_json)

        part = 0
        total_records_count = total_records(parsed_extractor_json, extractor_caches)
        extracted_output_page = extract(parsed_extractor_json, part, extractor_caches)
        output_id = None

        with tqdm.tqdm(total=int(total_records_count), desc="Processing", unit=' records', colour='green') as pbar:
            while extracted_output_page:
                transformed_df = transform(extracted_output_page, parsed_transformer_json, transformer_caches, pbar)
                
                #TODO: improve return type of generate_output. Handle errors better
                output_id = output(transformed_df, parsed_output_json, output_id, output_caches)
                
                #get next page
                part += 1
                extracted_output_page = extract(parsed_extractor_json, part, extractor_caches)
                
        pbar.close()
    except Exception as e:
        # print the full traceback
        import traceback
        traceback.print_exc() # <-- this prints it to stdout
        logger.error(traceback.format_exc()) 

        print(f"Error processing: {e}")
        logger.error(f"Error processing: {e}")


    print("Done!")

def load_json_file(base_directory, filename):
    json_file = None
    file_path = os.path.join(base_directory, filename)
    if not os.path.isfile(file_path):
        raise Exception(f'File {file_path} does not exist')
    with open(file_path) as file:
        json_file = json.load(file)
    return json_file

def parse_json_file(json):
    
    parsed_json = parse_json_structure(json)
    caches = load_caches(parsed_json)

    return caches, parsed_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bot input files.')
    parser.add_argument('base_directory', type=str, help='Base directory containing the JSON files (output.json, extractor.json, transformer.json)')
    
    args = parser.parse_args()
    process(args.base_directory)