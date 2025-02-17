'''
inconsistent relationships between datasets = broken joins, invalid analytics results
this file is to check the id, movieId and tmdbId all match up across files 

things to find out:
    - check all ID values in movies_metadata present in credits, keywords, ratings and links?
    - are there any IDs in one file but not another
'''

import pandas as pd
import logging

# logging
logging.basicConfig(
    filename='logs/id_relationships.log',
    level=logging.INFO,
    format='%(levelname)s @ %(asctime)s: %(message)s'
) 

data_dir = '../data'
output = 'outputs/data_relationship_summary.md'

def load_ID_data():

    # links >> movieId
    # credits >> id
    # movies_metadata >> id 
    # ratings >> movieId
    # keywords >> id

    # all datasets to check, only using id columns 
    credits = pd.read_csv(f"{data_dir}/credits.csv", usecols=["id"])
    movies_metadata = pd.read_csv(f"{data_dir}/movies_metadata.csv", usecols=["id"])
    links = pd.read_csv(f"{data_dir}/links.csv", usecols=["movieId"])
    ratings = pd.read_csv(f"{data_dir}/ratings.csv", usecols=["movieId"])
    keywords = pd.read_csv(f"{data_dir}/keywords.csv", usecols=["id"])

    for df in [credits, movies_metadata, links, ratings, keywords]:
        # print(f'LENGTH OF DF BEFORE: {len(df)}')
        first_col = df.columns[0]  # could be id or movieid so not hardcoded
        df[first_col] = pd.to_numeric(df[first_col], errors='coerce').astype('Int64')  # convert values
        df.dropna(subset=[first_col], inplace=True)  # drop nans
        # print(f'LENGTH OF DF AFTER: {len(df)}\n\n') # verify

    return credits, movies_metadata, links, ratings, keywords


def generate_summary(credits, movies_metadata, links, ratings, keywords):

    summary = {}

    # section 1: total ids
    summary['Total IDs in credits'] = len(credits['id'].unique())
    summary['Total IDs in movies_metadata'] = len(movies_metadata['id'].unique())
    summary['Total IDs in links'] = len(links['movieId'].unique())
    summary['Total IDs in ratings'] = len(ratings['movieId'].unique())
    summary['Total IDs in keywords'] = len(keywords['id'].unique())

    # section 2: ids in movies that aren't in anything else
    movie_ids = set(movies_metadata['id'])
    summary['Movie IDs not in credits'] = movie_ids - set(credits['id'])
    summary['Movie IDs not in links'] = movie_ids - set(links['movieId'])
    summary['Movie IDs not in ratings'] = movie_ids - set(ratings['movieId'])
    summary['Movie IDs not in keywords'] = movie_ids - set(keywords['id'])

    # section 3: ids in everything else that arent in movies
    summary['Credit IDs not in movies_metadata'] = set(credits['id']) - movie_ids
    summary['Link IDs not in movies_metadata'] = set(links['movieId']) - movie_ids
    summary['Ratings IDs not in movies_metadata'] = set(ratings['movieId']) - movie_ids
    summary['Keywords IDs not in movies_metadata'] = set(keywords['id']) - movie_ids

    return summary 


def main():
    credits, movies_metadata, links, ratings, keywords = load_ID_data()
    summary = generate_summary(credits, movies_metadata, links, ratings, keywords)
    
    with open(output, 'w') as file:
        file.write('# Relationship between IDs\n\n')

        for title, data in summary.items():
            if isinstance(data, set): # dont print out whole dataframes
                file.write(f'## {title}\n')
                file.write(f'- Count: {len(data)}\n')
                file.write(f'- Sample: {list(data)[:5]}\n') # gets a sample, workaround for .sample(5)

            else: 
                file.write(f'- {title}: {data}\n\n')

    logging.info(f'Finished checking id relationships, view {output}')

if __name__ == "__main__":
    main()