''' learn great expectations to do this properly '''

import os 
import pandas as pd
import logging
import json

# logging
logging.basicConfig(
    filename='logs/data_validation.log',
    level=logging.INFO,
    format='%(levelname)s @ %(asctime)s: %(message)s'
) 

data_dir = '../data'
output = 'outputs/data_validation.md'

def load_data(filename):
    try:
        df = pd.read_csv(filename, low_memory=False) # automatic d types might be wrong hence False
        logging.info(f'File: {filename} loaded successfully')
        return df
    except Exception as e:
        logging.info(f'ERROR: {filename} failed to load due to {e}')
        return None
    
def main():

    validation_summary = "# Data Validation \n\n"

    movies_metadata = load_data("../data/movies_metadata.csv")
    ratings = load_data("../data/ratings.csv")
    credits = load_data("../data/credits.csv")

    # check theres no duplicates
    try:
        if movies_metadata['id'].is_unique:
            validation_summary += "No duplicates in movies_metadata \n"
        else:
            validation_summary += "Duplicate entries in movies_metadata \n"
    except Exception as e:
        logging.info(f'ERROR: checking for movie duplicates failed due to {e}')

    # check budget is non negative
    try:
        movies_metadata['budget'] = pd.to_numeric(movies_metadata['budget'], errors='coerce')
        if (movies_metadata['budget'] >= 0).all():
            validation_summary += "No negative values in movies_metadata 'budget' column \n"
        else:
            validation_summary += "Negative values in movies_metadata 'budget' column \n"
    except Exception as e:
        logging.info(f'ERROR: checking for non negative budgets failed due to {e}')

    # check revenue is non negative
    try:
        movies_metadata['revenue'] = pd.to_numeric(movies_metadata['revenue'], errors='coerce')
        if (movies_metadata['revenue'] >= 0).all():
            validation_summary += "No negative values in movies_metadata 'revenue' column \n"
        else:
            validation_summary += "Negative values in movies_metadata 'revenue' column \n"
    except Exception as e:
        logging.info(f'ERROR: checking for non negative revenue failed due to {e}')

    # check date formate for release date
    try:
        pd.to_datetime(movies_metadata['release_date'], format='%Y-%m-%d', errors='coerce')
        validation_summary += ("The 'release_date' column in movies_metadata matches format 'YYYY-MM-DD' \n")
    except Exception as e:
        validation_summary += (f"ERROR: 'release_date' column in movies_metadata could not be processed due to {e} \n")

    # check if the rating is a 5 star scale
    try:
        if ratings['rating'].between(1, 5).all():
            validation_summary += ("The 'rating' column in ratings is between 1 and 5 inclusive \n")
        else:
            validation_summary += ("The 'rating' column in ratings is NOT between 1 and 5 inclusive \n")
    except Exception as e:
        validation_summary += (f"Error processing 'release_date' column in movies_metadata: {e} \n")

    # check if cast and crew columns in credits are json
    try:
        credits['cast'] = credits['cast'].apply(json.loads)
        credits['crew'] = credits['crew'].apply(json.loads)
        validation_summary += ("'cast' and 'crew' columns in credits are JSON fields and parse correctly \n")
    except Exception as e:
        validation_summary += (f"'cast' and/or 'crew' columns in credits are NOT JSON fields or do not parse correctly due to {e} \n")

    with open(output, 'w') as file:
        file.write(validation_summary)

    logging.info(f'Finished data validation, view {output}')


if __name__ == "__main__":
    main()

