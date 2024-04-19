from chunking import Chunk
from model import Model

def revise(chunk:Chunk, model:Model, base_path:str):
    chunk.load_text(base_path + 'revised/0.txt')
    response = model.response(model.get_prompt_template(task='revise_overs'), chunk.get_chunk_extracts()[0] + chunk.get_chunk_text()[1])
    chunk_id = str(chunk.get_chunk_id())
    with open(base_path+'revised/'+chunk_id+'.txt', 'w') as file:
        file.write(response)
    print(response)