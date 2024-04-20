from chunking import Chunk
from model import Model
from extract import extract
from revise import revise
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
    parser.add_argument('--task' , dest='task', default = 'extract', type=str, help='Task to perform: extract or revise')
    args = parser.parse_args()
    config = get_args(args)
    paths = config['paths']
    base = paths['base']
    
    # chunk = Chunk('overs')
    # model = Model('gemma:2b')
    
    # extract(chunk, model, base)
    # revise(chunk, model, base)

    chunk = Chunk('prematch')
    model = Model('orca-mini')

    extract(chunk, model, base)
    revise(chunk, model, base)