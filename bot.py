# main.py

import json
import os
import tqdm
import argparse
import logging
import requests

from extractor.extractor import extract, total_records
from transformer.transformer import transform
from output.output import output

from common.interpreter.cache_interpreter import load_caches
from common.interpreter.input_interpreter import load_input
from common.utils.logging_config import setup_logger
from common.utils.profiling import lap_time
from common.interpreter.formula_parser import parse_json_structure
from common.global_state import GlobalStateKeys, global_state
from common.utils.exceptions import JsonResponseError

logger = logging.getLogger(__name__)

def process(base_directory):
        
    try:
        global_state.set_value(GlobalStateKeys.CURRENT_BASE_DIR, base_directory)

        setup_logger()
        
        extractor_json = load_json_file(base_directory, 'extractor.json')
        extractor_input, parsed_extractor_json = parse_extractor_file(extractor_json)
        if extractor_input:
            global_state.set_value(GlobalStateKeys.INPUT_RECORDS, extractor_input)
            global_state.set_value(GlobalStateKeys.CURRENT_INPUT_PART, 0)

        transformer_json = load_json_file(base_directory, 'transformer.json')
        transformer_caches, parsed_transformer_json = parse_transformer_file(transformer_json)

        output_json = load_json_file(base_directory, 'output.json')
        parsed_output_json = parse_output_file(output_json)

        part = 0
        total_records_count = total_records(parsed_extractor_json)
        global_state.set_value(GlobalStateKeys.TOTAL_RECORDS, total_records_count)

        extracted_output_page = extract(parsed_extractor_json, part)
        extraction_error = False
        output_id = None

        with tqdm.tqdm(total=int(total_records_count), desc="Processing", unit=' records', colour='green') as pbar:
            while extracted_output_page:
                # If the extraction type is based on input, the update of the progress bar is done at the bot.py level (per input row)
                # else, the update is done at the transformer level (per record extracted from the page)
                update_pbar = None
                if not extractor_input:
                    update_pbar = pbar
                else:
                    pbar.update(1)

                transformed_df = transform(extracted_output_page, parsed_transformer_json, transformer_caches, update_pbar)
                output_id = output(transformed_df, parsed_output_json, output_id)
                
                try:
                    #get next page / part / input-row
                    part += 1
                    global_state.set_value(GlobalStateKeys.CURRENT_INPUT_PART, part)
                    extracted_output_page = extract(parsed_extractor_json, part)
                    extraction_error = False
                except (json.decoder.JSONDecodeError, requests.exceptions.RequestException) as e:
                    logger.error(f"Error processing part/page/row: {part}, file id: {output_id}. Continuing with next part/page/row. Error: {e}")
                    extraction_error = True
                except JsonResponseError as e:
                    if e.should_continue:
                        extraction_error = True
                    else:
                        raise e
                
        pbar.close()
    
    except Exception as e:
        # print the full traceback
        import traceback
        traceback.print_exc() # <-- this prints it to stdout
        logger.error(traceback.format_exc()) 

        print(f"Error processing - finishing execution: {e}")
        logger.error(f"Error processing - finishing execution: {e}")


    print("Done!")

def load_json_file(base_directory, filename):
    json_file = None
    file_path = os.path.join(base_directory, filename)
    if not os.path.isfile(file_path):
        raise Exception(f'File {file_path} does not exist')
    with open(file_path) as file:
        json_file = json.load(file)
    return json_file

def parse_transformer_file(json):
    parsed_json = parse_json_structure(json)
    caches = load_caches(parsed_json)
    return caches, parsed_json

def parse_extractor_file(json):
    parsed_json = parse_json_structure(json)
    input = load_input(parsed_json)
    return input, parsed_json

def parse_output_file(json):
    parsed_json = parse_json_structure(json)
    return parsed_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bot input files.')
    parser.add_argument('base_directory', type=str, help='Base directory containing the JSON files (output.json, extractor.json, transformer.json)')
    
    args = parser.parse_args()
    process(args.base_directory)