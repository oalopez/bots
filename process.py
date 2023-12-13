import json
import os

from extractor.extractor import extract
from transformer.transformer import transform
from loader.loader import load
import pandas as pd

global_vars={"_year":"2022"}
local_vars = {}

context_vars = {"global_vars": global_vars, 
                "local_vars": local_vars}


def main():
    # 1. Extraction process
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'extractor.json')):
        raise Exception('Extractor file does not exist')

    with open(os.path.join(os.path.dirname(__file__), 'extractor.json')) as extractor_file:
        extractor_json = json.load(extractor_file)
    extracted_output = extract(extractor_json, context_vars)

    # 2. Transformation process
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'transformer.json')):
        raise Exception('Transformer file does not exist')
    with open(os.path.join(os.path.dirname(__file__), 'transformer.json')) as transformer_file:
        transformer_json = json.load(transformer_file)
    transformed_df = transform(transformer_json, extracted_output, context_vars)

    #print head of transformed_df
    print(transformed_df.head())

    
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
    main()