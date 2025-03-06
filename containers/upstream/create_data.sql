CREATE SCHEMA films;

-- FILMS
CREATE TABLE films.films_raw (
    adult TEXT, -- should be boolean but some bad values e.g. - Written by Ørnås
    belongs_to_collection TEXT, -- invalid json
    budget TEXT, -- should be int but bad values e.g. a jpg link
    genres TEXT,
    homepage TEXT, -- treat urls as long strings & store as text
    id TEXT, -- should be int but bad values / removed primary key constraint becuase EDA tells us theres duplicates
    imdb_id VARCHAR(15),
    original_language VARCHAR(5),
    original_title TEXT,
    overview TEXT,
    popularity TEXT, -- should be NUMERIC(10,6) but "Beware Of Frost Bites" is in here for some reason
    poster_path TEXT,
    production_companies TEXT,
    production_countries TEXT,
    release_date TEXT, -- should be DATE but bad data
    revenue NUMERIC(15,2), -- some float values present
    runtime NUMERIC(5,1), -- runtimes have small decimals
    spoken_languages TEXT,
    status VARCHAR(20),
    tagline TEXT,
    title TEXT,
    video BOOLEAN,
    vote_average NUMERIC(3,1), -- averages between 0-10 with 1 decimal
    vote_count NUMERIC(10,2) -- incase
);

-- ALTER TABLE films.films_raw ALTER COLUMN popularity DROP NOT NULL;

COPY films.films_raw(
    adult,
    belongs_to_collection,
    budget,
    genres,
    homepage,
    id,
    imdb_id,
    original_language,
    original_title,
    overview,
    popularity,
    poster_path,
    production_companies,
    production_countries,
    release_date,
    revenue,
    runtime,
    spoken_languages,
    status,
    tagline,
    title,
    video,
    vote_average,
    vote_count
)
FROM '/input_data/movies_metadata_jsonclean.csv' DELIMITER ',' CSV HEADER NULL AS '';

-- CREDITS
CREATE TABLE films.credits_raw (
    id INT PRIMARY KEY,
    film_cast JSONB, -- 'cast' is reserved keyword
    crew JSONB
);

COPY films.credits_raw(id, film_cast, crew)
FROM '/input_data/credits_raw.csv' DELIMITER ',' CSV HEADER;

-- KEYWORDS
CREATE TABLE films.keywords_raw (
    id INT PRIMARY KEY,
    keywords JSONB
);

COPY films.keywords_raw(id, keywords)
FROM '/input_data/keywords_raw.csv' DELIMITER ',' CSV HEADER;

-- RATINGS
CREATE TABLE films.ratings_raw (
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating NUMERIC(2,1) NOT NULL,  -- need floats, vals like 4.5 
    timestamp INT NOT NULL,

    PRIMARY KEY (user_id, movie_id)  -- composite key to avoid duplicate ratings
);

COPY films.ratings_raw(user_id, movie_id, rating, timestamp)
FROM '/input_data/ratings_raw.csv' DELIMITER ',' CSV HEADER;

-- LINKS
CREATE TABLE films.links_raw (
    movie_id INT PRIMARY KEY,  
    imdb_id VARCHAR(10) NOT NULL,  -- account for occasional leading zeros
    tmdb_id INT NOT NULL  
);

COPY films.links_raw(movie_id, imdb_id, tmdb_id)
FROM '/input_data/links_raw.csv' DELIMITER ',' CSV HEADER;
