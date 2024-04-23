from chunking import Chunk
from model import Model
from loguru import logger
import time
import os


def extract(chunk:Chunk, model:Model, dir_path:str, save:bool = True, no_extractions = 2):

    start = time.time()
    for i in range(no_extractions):
        response = model.response(model.get_prompt_template(task='extract', type = chunk.chunk_type), chunk.get_chunk_text())
        chunk.set_chunk_extracts(response)
        chunk_id = str(chunk.get_chunk_id())
        chunk_type = chunk.chunk_type
        
        if save:
            if not os.path.exists(dir_path + chunk_type + '/'):
                os.makedirs(dir_path + chunk_type + '/')

            with open(dir_path + chunk_type + '/' + chunk_id + str(i) + '.txt', 'w') as file:
                file.write(response)
            logger.info(f'Saved Extract: {chunk.chunk_type} | {chunk_id} | {i}')

    end = time.time()
    logger.info(f'Total time taken to extract: {chunk.chunk_type} | {chunk_id} | {end-start}')
    # chunk.print_chunk_extracts()
