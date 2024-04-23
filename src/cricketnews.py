from chunking import Match, combine_summaries
from model import Model
from extract import extract
from revise import revise
from generate import generate
from refine import refine
from loguru import logger
from utils import metadata_template, count_tokens
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
            logger.error(exc)
    return config

if __name__ == '__main__':
    total_start = time.time()
    parser = argparse.ArgumentParser(description='Extract and Revise')
    parser.add_argument('--config', dest='config_path', default ='config.yaml', type=str, help='Path to the config file')
    args = parser.parse_args()
    
    config = get_args(args)
    paths = config['paths']
    base = paths['base']
    data = paths['data']
    commentary = paths['commentary']
    chunks = paths['chunks']
    extracted = base+paths['extract']
    revised = base+paths['revise']
    final_dir = base+paths['final_dir']

    models = config['models']
    extractmodel = models['extract']
    revisemodel = models['revise']
    generatemodel = models['generate']

    save_options = config['save_options']
    save_extract = save_options['save_extract']
    save_revise = save_options['save_revise']
    save_generate = save_options['save_generate']
    save_refine = save_options['save_refine']

    match = Match(data_path=base + data + commentary, save_chunk=True, chunk_dir=base + chunks)
    match.load_commentaries()
    metadata_template(66169, base)

    start = time.time()
    model = Model(extractmodel)
    end = time.time()

    logger.info(f'Total time taken to load model {extractmodel} :{end-start}')

    start = time.time()

    for chunk in match.prematch:
        extract(chunk, model, extracted, save_extract)
        revise(chunk, model, revised, save_revise)

    for chunk in match.innings:
        extract(chunk, model, extracted, save_extract)
        revise(chunk, model, revised, save_revise)

    for chunk in match.postmatch:
        extract(chunk, model, extracted, save_extract)
        revise(chunk, model, revised, save_revise)

    end = time.time()
    logger.info(f'Total time taken to extract and revise: {end-start}')

    combined_prematch = combine_summaries(match.prematch)
    combined_innings = combine_summaries(match.innings)
    combined_postmatch = combine_summaries(match.postmatch)
    combined = combined_prematch + combined_innings + combined_postmatch
    count_tokens(combined)

    start = time.time()
    model = Model(generatemodel)
    end = time.time()
    
    logger.info(f'Total time taken to load model {generatemodel} :{end-start}')
    article = generate(combined, model, final_dir, save_generate)
    refine(article, model, final_dir, save_refine)
    total_end = time.time()
    logger.info(f'Total time taken for the entire process: {total_end-total_start}')