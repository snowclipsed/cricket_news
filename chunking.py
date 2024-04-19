import os
import pandas as pd

class Chunk():
    def __init__(self, chunk_type = 'over', chunk_id:int = 0, chunk_size = 1000, chunk_text = None):
        self.chunk_type = chunk_type
        self.chunk_size = chunk_size
        self.chunk_text = chunk_text
        self.chunk_id = chunk_id
        self.chunk_extracts = []

    def load_text(self, path):
        if os.path.exists(path):
            if path.endswith('.txt'):
                with open(path, 'r') as file:
                    self.chunk_text = file.read()
            # if path.endswith('.csv'):
            #     commentary = pd.read_csv(path)
        else:
            print("File does not exist.")


    def set_chunk_extracts(self, chunk_extract):
        self.chunk_extracts.append(chunk_extract)

    def get_chunk_extracts(self):
        return self.chunk_extracts
    
    def print_chunk_extracts(self):
        for extract in self.chunk_extracts:
            print(extract)
            print('\n')

    def get_chunk_id(self):
        return self.chunk_id
    
    def get_chunk_size(self):
        return self.chunk_size
    
    def get_chunk_text(self):
        return self.chunk_text
    

