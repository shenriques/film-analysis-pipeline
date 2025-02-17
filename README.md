# Film Data Engineering Project 

## Project Background

### Aims:

- build a data pipeline for a film analytics company to process, analyse, and visualise movie-related datasets
- the data includes information about movies, their metadata, keywords, cast and crew, and ratings
- ingest, transform, store, and visualise the data for analytics and reporting purposes

### Project features:

- pipeline orchestration using Apache Airflow in a Dockerized environment
- Scalable data processing using Apache Spark
- Object storage with Minio (S3-compatible)
- Relational and warehouse-style databases with PostgreSQL and DuckDB
- Testing, linting, and CI integration for quality assurance
- Visualisation and reporting with Quarto and Plotly

## Project Data

### Data Source

https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

movies_metadata.csv: The main Movies Metadata file. Contains information on 45,000 movies featured in the Full MovieLens dataset. Features include posters, backdrops, budget, revenue, release dates, languages, production countries and companies.

keywords.csv: Contains the movie plot keywords for our MovieLens movies. Available in the form of a stringified JSON Object.

credits.csv: Consists of Cast and Crew Information for all our movies. Available in the form of a stringified JSON Object.

links.csv: The file that contains the TMDB and IMDB IDs of all the movies featured in the Full MovieLens dataset.

### Exploratory Data Analysis

- develop scripts to understand the data and output results to markdown

## Order of Development

### 1. Create the skeleton

- create containers/airflow which contains:
    - Dockerfile to set up Airflow image with Quarto and Spark
    - bash script to set up Quarto
    - requirements.txt
    - python script to set up airflow connections

- create data/ which contains
    - CSV of the input data 

- create containers/upstream which contains:
    - SQL script to create the source database and load the local data into it 

- create docker compose file which:
    - sets up data pipeline environment with containers for airflow, postgres and minio
    - includes mounted directories so they can share data / configurations

    - has an x-airflow-common

    - has service for postgres
        - postgres database used for airflow for metadata
        - does a health check to check service is ready before dependencies (airflow) start
        - ./data:/input_data: shares data between host and container
        - ./containers/upstream:/docker-entrypoint-initdb.d: folder has initialisation scripts to be executed when the database is first started

    - has service for airflow web server
        - runs the web interface so you can see the DAGS

    - has service for airflow scheduler 
        - what triggers DAGs based on schedules
        - gets config from x-airflow-common

    - has service for airflow init  
        - initialises airflow by performing database migrations and creating web server user 

    - has service for minio