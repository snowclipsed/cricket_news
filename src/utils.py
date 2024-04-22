import pandas as pd
from loguru import logger
from transformers import AutoTokenizer

def combine_text_column(df: pd.DataFrame) -> str:
    """
    Combine the text data from a specified column in a pandas DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        text_column (str or int): The name or index of the column containing the text data.

    Returns:
        str: The combined text data from the specified column.
    """
    # Convert the column to a string data type
    df.loc[:, 'commentary_data'] = df['commentary_data'].astype(str)

    # Combine the text data from the column using an empty string as the separator
    combined_text = ''.join(df['commentary_data'])

    return combined_text

def metadata_template(match_id:int, base:str):
    """
    Get the match information from the specified match ID.

    Args:
        df (pd.DataFrame): The input DataFrame.
        match_id (str): The match ID.

    Returns:
        pd.DataFrame: The match information.
    """
    df = pd.read_csv(base + 'data/'+str(match_id)+'_match_info.csv')
    # Filter the DataFrame to get the match information
    match_info = df[df['match_id'] == match_id]
    year = match_info['year'].values[0]
    team1 = match_info['team1'].values[0]
    team2 = match_info['team2'].values[0]
    venue = match_info['venue'].values[0]
    city = match_info['city'].values[0]

    metadata = 'The match happened on ' + str(year) + ' between ' + str(team1) + ' and ' + str(team2) + ' at ' + str(venue) + ' in ' + str(city) + '.'

    with open(base + 'prompt_templates/generate/metadata.txt', 'w') as file:
        file.write(metadata)
    logger.info('Metadata template created successfully.')
    return year, team1, team2, venue, city

def count_tokens(text):
    tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
    tokens = tokenizer.encode(text, return_tensors="np")
    logger.info("Number of tokens: {}".format(len(tokens[0])))

# make a function to feed in write argument into revise and extract function so it can be used to toggle saving or not 
# write a function to load all the chunks into a list after creating chunks (DONE)
# write a function to create chunks (DONE)
# write a function to load the data (DONE)
# write a function to load the innings