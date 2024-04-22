from chunking import Chunk
from model import Model
from loguru import logger
import time
import os

def revise(chunk:Chunk, model:Model, base_path:str, write:bool = True):
    """
    Takes all the extracts of the chunk and sends it to the model to generate a final list of summaries for that chunk.

    Model is usually a smaller model like Phi-2 fine tuned, orca-mini or gemma:2b.
    """
    start = time.time()
    response = model.response(model.get_prompt_template(task='revise', type=chunk.chunk_type), chunk.get_chunk_extracts()[0] + chunk.get_chunk_extracts()[1])
    chunk_id = str(chunk.get_chunk_id())
    chunk_type = chunk.chunk_type
    chunk.revised = response
    end = time.time()
    logger.info(f'Total time taken to revise: {chunk.chunk_type} | {chunk_id} | {end-start}')
    
    if not os.path.exists(base_path+'revised/'+chunk_type+'/'):
        os.makedirs(base_path+'revised/'+chunk_type+'/')
    
    if write:
        with open(base_path+'revised/'+chunk_type+'/'+chunk_id+'.txt', 'w') as file:
            file.write(response)
    return response