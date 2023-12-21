# main.py

import json
import os
import pandas as pd
import time

from extractor.extractor import extract
from transformer.transformer import transform
from loader.loader import load

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
    
    with open(os.path.join(os.path.dirname(__file__), 'extractor.json')) as extractor_file:
        extractor_json = json.load(extractor_file)
    
    with open(os.path.join(os.path.dirname(__file__), 'transformer.json')) as transformer_file:
        transformer_json = json.load(transformer_file)
    
    extracted_output_page = extract(extractor_json, context_vars)
    now = time.time()
    part = 0

    while extracted_output_page:
        transformed_df = transform(transformer_json, extracted_output_page, context_vars)
        #print head of transformed_df
        print(transformed_df.head(3))
        #dump transformed_df to csv. Append to csv if it exists. Do not include the index
        transformed_df.to_csv('data/transformed_df_' + str(now) + '.csv', mode='a', header=False if part > 0 else True, index=False)
        #get next page
        part += 1
        extracted_output_page = extract(extractor_json, context_vars, part)

    
    # 3. Load process
    # if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'loader.json')):
    #     raise Exception('Loader file does not exist')
    # with open(os.path.join(os.path.dirname(__file__), 'loader.json')) as loader_file:
    #     loader_json = json.load(loader_file)
    # result = load(loader_json, transformed_df)

    # # TODO: Handle output correctly
    # if result == "SUCCESS":
    #     print("SUCCESS")
    # else:
    #     print("ERROR")

if __name__ == "__main__":
    process()