from model import Model
from loguru import logger
import time
import os

"""
This function should take in the combined summary points all at once and then should call llama3 to 
generate a final summary.

:param type: Here the type can be either 'article' or 'points'. 
If the type is 'article' then llama3 will generate an article from the combined summary.
If the type is 'points' then llama3 will generate a summary of the combined summary points.
"""

def generate(combined_summary:str, model:Model, save_dir:str, save:bool = True):
    
    start = time.time()    
    article = model.response(model.get_prompt_template(task='generate', type = 'metadata') + model.get_prompt_template(task='generate', type = 'article') , combined_summary)
    end = time.time()
    logger.info(f'Total time taken to generate article: {end-start}')
    
    # write combined summary to file
    if save:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        with open(save_dir+'article.txt', 'w') as file:
            try:
                file.write(article)
            except UnicodeEncodeError:
                logger.error('UnicodeEncodeError: Could not write to file. Saving as bytes.')
                file.write(article.encode('utf-8'))
        logger.info(f'Article generation saved at {save_dir}article.txt.')
    return article