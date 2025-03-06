# Film Data Engineering Project 

A data pipeline for processing, analysing and visualisation data all about film.

## Overview

This project builds a complete data engineering pipeline for film analytics, transforming raw movie data into insights.

## Features:

- **Orchestration**: Apache Airflow in a containerised environment
- **Processing**: Apache Spark for scalable data transformations
- **Storage**:
    - Minio (S3-compatible) for object storage
    - PostgreSQL for relational data
    - DuckDB for analytical queries
- **Quality Assurance**: Automated testing, linting, and CI integration
- **Visualisation**: Interactive dashboards with Quarto and Plotly

## Data Source

The project uses [The Movies Dataset from Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset), which includes:

- **movies_metadata.csv**: Information on 45,000 movies (posters, budget, revenue, release dates, languages, production details)
- **keywords.csv**: Movie plot keywords (JSON format)
- **credits.csv**: Cast and crew information (JSON format)
- **links.csv**: TMDB and IMDB IDs for all movies

## Architecture

### Docker Services

| Service               | Purpose                                    |
| --------------------- | ------------------------------------------ |
| **PostgreSQL**        | Source database and Airflow metadata store |
| **Airflow Webserver** | Web interface for DAG management           |
| **Airflow Scheduler** | Triggers DAGs based on defined schedules   |
| **Minio**             | S3-compatible object storage               |
| **PGAdmin**           | Database administration interface          |

## Development Workflow

0. **Exploratory Data Analysis**: Python scripts give an overview of the data, including any inconsistencies
1. **Data Ingestion**: Raw data is loaded from CSVs into PostgreSQL
2. **Transformation**: Spark jobs clean and transform the data
3. **Storage**: Processed data is stored in optimised formats
4. **Analysis**: DuckDB performs analytical queries
5. **Visualisation**: Quarto generates reports with Plotly visualisations

## Setup

TBC
