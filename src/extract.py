from chunking import Chunk
from model import Model
from loguru import logger
import time


def extract(chunk:Chunk, model:Model, base_path:str, no_extractions = 2):

    start = time.time()
    for i in range(no_extractions):
        response = model.response(model.get_prompt_template(task='extract', type = chunk.chunk_type), chunk.get_chunk_text())
        chunk.set_chunk_extracts(response)
        chunk_id = str(chunk.get_chunk_id())
    
        with open(base_path+'extracted/'+ chunk_id + str(i) + '.txt', 'w') as file:
            file.write(response)
    end = time.time()
    logger.info(f'Total time taken to extract: {chunk.chunk_type} | {chunk_id} | {end-start}')
    # chunk.print_chunk_extracts()
