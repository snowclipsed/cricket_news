from chunking import Chunk
from model import Model

def revise(chunk:Chunk, model:Model, base_path:str, write:bool = True):
    """
    Takes all the extracts of the chunk and sends it to the model to generate a final list of summaries for that chunk.

    Model is usually a smaller model like Phi-2 fine tuned, orca-mini or gemma:2b.
    """
    response = model.response(model.get_prompt_template(task='revise', type=chunk.chunk_type), chunk.get_chunk_extracts()[0] + chunk.get_chunk_extracts()[1])
    chunk_id = str(chunk.get_chunk_id())
    chunk.revised = response
    if write:
        with open(base_path+'revised/'+chunk_id+'.txt', 'w') as file:
            file.write(response)
    print(response)
    return response