# main.py

import json
import os
import time
import tqdm

from extractor.extractor import extract, total_records
from transformer.transformer import transform
from output.output import generate_output

from common.utils.logging_config import setup_logger

setup_logger()

# TODO: Handle context_vars correctly
global_vars={"_year":"2022"}
local_vars = {}

context_vars = {"global_vars": global_vars, 
                "local_vars": local_vars}

def process():
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'extractor.json')):
        raise Exception('Extractor file does not exist')

    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'transformer.json')):
        raise Exception('Transformer file does not exist')
    
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'output.json')):
        raise Exception('Loader file does not exist')
    
    with open(os.path.join(os.path.dirname(__file__), 'extractor.json')) as extractor_file:
        extractor_json = json.load(extractor_file)
    
    with open(os.path.join(os.path.dirname(__file__), 'transformer.json')) as transformer_file:
        transformer_json = json.load(transformer_file)

    with open(os.path.join(os.path.dirname(__file__), 'output.json')) as output_file:
        output_json = json.load(output_file)
    

    total_records_count = total_records(extractor_json, context_vars)
    extracted_output_page = extract(extractor_json, context_vars)
    now = time.time()
    part = 0

    output_id = None
    with tqdm.tqdm(total=int(total_records_count), desc="Processing", unit=' records', colour='green') as pbar:
        while extracted_output_page:
            transformed_df = transform(transformer_json, extracted_output_page, context_vars)
            #dump transformed_df to csv. Append to csv if it exists. Do not include the index
            transformed_df.to_csv('data/transformed_df_' + str(now) + '.csv', mode='a', header=False if part > 0 else True, index=False)
            #get next page
            part += 1
            extracted_output_page = extract(extractor_json, context_vars, part)
            #TODO: improve return type of generate_output. Handle errors better
            output_id = generate_output(output_json, transformed_df, context_vars, output_id)
            # Update the progress bar
            pbar.update(transformed_df.shape[0])
    pbar.close()

    print("Done!")
    
if __name__ == "__main__":
    process()