from chunking import Chunk
from model import Model

def extract(chunk:Chunk, model:Model, base_path:str, no_extractions = 2):

    chunk.load_text(base_path + 'chunks/match.txt')
    for i in range(no_extractions):
        response = model.response(model.get_prompt_template(task='extract_overs'), chunk.get_chunk_text())
        chunk.set_chunk_extracts(response)
        chunk_id = str(chunk.get_chunk_id())
    
        with open(base_path+'extracted/'+ chunk_id + str(i) + '.txt', 'w') as file:
            file.write(response)

    chunk.print_chunk_extracts()
