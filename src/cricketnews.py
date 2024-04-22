from chunking import Match, combine_summaries
from model import Model
from extract import extract
from revise import revise
from generate import generate
from loguru import logger
from utils import metadata_template
import time
import yaml
import argparse

def get_args(args):
    # Read the config file #
    with open(args.config_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
    return config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract and Revise')
    parser.add_argument('--config', dest='config_path', default ='config.yaml', type=str, help='Path to the config file')
    args = parser.parse_args()
    config = get_args(args)
    paths = config['paths']
    base = paths['base']
    data = paths['data']
    commentary = paths['commentary']
    models = config['models']
    extractmodel = models['extract']
    revisemodel = models['revise']
    generatemodel = models['generate']

    
    match = Match(base + data + commentary)
    match.load_commentaries()
    metadata_template(66169, base)

    start = time.time()
    model = Model(extractmodel)
    end = time.time()
    logger.info(f'Total time taken to load model {extractmodel} :{end-start}')
    
    start = time.time()
    for chunk in match.innings:
        extract(chunk, model, base)
        revise(chunk, model, base)
    end = time.time()
    logger.info(f'Total time taken to extract and revise: {end-start}')

    combined = combine_summaries(match.innings)
    
    start = time.time()
    model = Model(generatemodel)
    end = time.time()
    logger.info(f'Total time taken to load model {generatemodel} :{end-start}')

    start = time.time()
    generate(combined, model, base)
    end = time.time()
    logger.info(f'Total time taken to generate: {end-start}')