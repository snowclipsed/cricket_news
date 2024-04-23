import os
import pandas as pd
from typing import List
from utils import combine_text_column
from loguru import logger
from transformers import AutoTokenizer

class Chunk():
    """
        It is a dataclass which stores a chunk of text data.
    """
    def __init__(self, chunk_type = 'innings', chunk_id:int = 0, chunk_text = None):
        self.chunk_type = chunk_type
        self.chunk_text = chunk_text
        self.chunk_id = chunk_id
        self.chunk_extracts = []
        self.chunk_revised = ''

    # def load_text(self, path):
    #     """
    #     temporary function to load text from a file

    #     modify this to take data from the match class instead
        
    #     """
    #     if os.path.exists(path):
    #         if path.endswith('.txt'):
    #             with open(path, 'r') as file:
    #                 self.chunk_text = file.read()
    #         # if path.endswith('.csv'):
    #         #     commentary = pd.read_csv(path)
    #     else:
    #         logger.error("File does not exist.")


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
    

class Match():
    def __init__(self, data_path:str = None, chunk_dir:str = None, save_chunk:bool = True, highlights:bool = True):
        self.data_path = data_path
        self.prematch = List[Chunk]
        self.innings = List[Chunk]
        self.postmatch = List[Chunk]
        self.chunk_dir = chunk_dir
        self.save_chunk = save_chunk
        self.highlights = highlights

    def load_commentaries(self):
        """
        Takes in commentary data from a file and loads all of it into a data class object.
        """
        path = self.data_path
        if os.path.exists(path):
            if path.endswith('.csv'):
                commentary = pd.read_csv(path)
                highlights = pd.read_csv(path.replace('commentary', 'highlights'))
                prematch = commentary[commentary['over_number'] == 'preview']
                postmatch = commentary[commentary['over_number'] == 'post']
                if self.highlights:
                    innings = highlights
                else:
                    innings = commentary[commentary['over_number'] != 'preview']
                    innings = innings[innings['over_number'] != 'post']
        else:
            logger.error("File does not exist.")
            return None
        
        # create chunks
        prematch_text = combine_text_column(prematch)
        self.prematch = create_chunks(prematch_text, chunk_type='prematch', save_dir=self.chunk_dir, save=self.save_chunk)
        logger.info(f"Number of prematch chunks: {len(self.prematch)}")


        innings_text = combine_text_column(innings)
        # print(innings_text)
        self.innings = create_chunks(innings_text, chunk_type='innings', save_dir=self.chunk_dir, save=self.save_chunk)
        logger.info(f"Number of innings chunks: {len(self.innings)}")

        postmatch_text = combine_text_column(postmatch)
        self.postmatch = create_chunks(postmatch_text, chunk_type='postmatch', save_dir=self.chunk_dir, save=self.save_chunk)
        logger.info(f"Number of postmatch chunks: {len(self.postmatch)}")

def combine_summaries(chunks: List[Chunk]):
    """
    This function will combine all the summaries into one single summary.

    Needs to be done in temporal order.

    NOTE: Add metadata into it later.
    """
    combined_summary = ''
    for chunk in chunks:
        combined_summary += chunk.revised + '\n'
    return combined_summary



def create_chunks(data: str, chunk_type:str, save_dir:str, save:bool=True, chunk_size: int = 1500, overlap: int = 20, tokenizer_name: str = "microsoft/phi-2") -> List[Chunk]:
    """
    This function takes in data and creates chunks of the specified number of tokens with an optional overlap.

    Args:
        data (str): The input text data to be chunked.
        chunk_size (int, optional): The desired number of tokens in each chunk. Defaults to 100.
        overlap (int, optional): The number of tokens to overlap between consecutive chunks. Defaults to 0.
        tokenizer_name (str, optional): The name of the tokenizer to use (from the Hugging Face Transformers library). Defaults to "phi-2".

    Returns:
        List[Chunk]: A list of Chunk objects containing the chunked text.
    """
    # add metadata

    chunks = []
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    tokens = tokenizer.tokenize(data)
    start = 0
    end = chunk_size
    chunk_id = 0

    while start < len(tokens):
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.convert_tokens_to_string(chunk_tokens)
        chunks.append(Chunk(chunk_id=chunk_id, chunk_type=chunk_type, chunk_text=chunk_text))
        if save:
            if not os.path.exists(save_dir+'/'+chunk_type):
                os.makedirs(save_dir+'/'+chunk_type)
            with open(save_dir+'/'+chunk_type+'/'+str(chunk_id)+'.txt', 'w') as file:
                try:
                    file.write(chunk_text)
                except UnicodeEncodeError:
                    logger.error('UnicodeEncodeError: Could not write to file. Saving as bytes.')
                    file.write(chunk_text.encode('utf-8'))
        start = end - overlap
        end = start + chunk_size
        chunk_id += 1

    return chunks

# Match('/home/snow/NEU/cricket_news/data/66169_commentary.csv').load_commentaries()
