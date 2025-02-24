CREATE SCHEMA films;

-- FILMS
CREATE TABLE films.films_raw (
    adult BOOLEAN,
    belongs_to_collection JSONB, -- json
    budget INT,
    genres JSONB,
    homepage TEXT, -- treat urls as long strings & store as text
    id INT PRIMARY KEY,
    imdb_id VARCHAR(15),
    original_language VARCHAR(5),
    original_title TEXT,
    overview TEXT,
    popularity NUMERIC(10,6),
    poster_path TEXT,
    production_companies JSONB,
    production_countries JSONB,
    release_date DATE,
    revenue BIGINT, -- for if revenue exceeds 2.2 billion which is the max for int
    runtime NUMERIC(5,2), -- runtimes have small decimals
    spoken_languages JSONB,
    status VARCHAR(20),
    tagline TEXT,
    title TEXT,
    video BOOLEAN,
    vote_average NUMERIC(3,1), -- averages between 0-10 with 1 decimal
    vote_count BIGINT -- incase
);

-- CREDITS
CREATE TABLE films.credits_raw (
    id INT PRIMARY KEY,
    cast JSONB,
    crew JSONB
);

-- KEYWORDS
CREATE TABLE films.keywords_raw (
    id INT PRIMARY KEY,
    keywords JSONB
);

-- RATINGS
CREATE TABLE films.ratings_raw (
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating NUMERIC(2,1) NOT NULL,  -- need floats, vals like 4.5 
    timestamp INT NOT NULL,

    PRIMARY KEY (user_id, movie_id)  -- composite key to avoid duplicate ratings
);

-- LINKS
CREATE TABLE films.links_raw (
    movie_id INT PRIMARY KEY,  
    imdb_id VARCHAR(10) NOT NULL,  -- account for occasional leading zeros
    tmdb_id INT NOT NULL  
);
