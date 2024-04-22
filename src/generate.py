from model import Model
from loguru import logger
import time

"""
This function should take in the combined summary points all at once and then should call llama3 to 
generate a final summary.

:param type: Here the type can be either 'article' or 'points'. 
If the type is 'article' then llama3 will generate an article from the combined summary.
If the type is 'points' then llama3 will generate a summary of the combined summary points.
"""

def generate(combined_summary:str, model:Model, base):
    
    start = time.time()    
    article = model.response(model.get_prompt_template(task='generate', type = 'starter') + model.get_prompt_template(task='generate', type = 'metadata') , combined_summary + model.get_prompt_template(task='generate', type = 'format'))
    end = time.time()
    logger.info(f'Total time taken to generate: {end-start}')
    
    # write combined summary to file
    with open(base+'final_summary/final_summary.txt', 'w') as file:
        file.write(article)

