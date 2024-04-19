from chunking import Chunk
from model import Model
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

def extract(chunk:Chunk, model:Model, base_path:str, no_extractions = 2):

    chunk.load_text(base_path + 'chunks/match.txt')
    for i in range(no_extractions):
        response = model.response(model.get_prompt_template(task='extract_overs'), chunk.get_chunk_text())
        chunk.set_chunk_extracts(response)
        chunk_id = str(chunk.get_chunk_id())
    
        with open(base_path+'extracted/'+ chunk_id + str(i) + '.txt', 'w') as file:
            file.write(response)

    chunk.print_chunk_extracts()

def revise(chunk:Chunk, model:Model, base_path:str):
    chunk.load_text(base_path + 'revised/0.txt')
    response = model.response(model.get_prompt_template(task='revise_overs'), chunk.get_chunk_extracts()[0] + chunk.get_chunk_text()[1])
    chunk_id = str(chunk.get_chunk_id())
    with open(base_path+'revised/'+chunk_id+'.txt', 'w') as file:
        file.write(response)
    print(response)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract and Revise')
    parser.add_argument('--config', dest='config_path', default ='config.yaml', type=str, help='Path to the config file')
    args = parser.parse_args()
    config = get_args(args)
    paths = config['paths']
    base = paths['base']
    
    chunk = Chunk('over')
    model = Model('gemma:2b')
    
    extract(chunk, model, base)
    revise(chunk, model, base)