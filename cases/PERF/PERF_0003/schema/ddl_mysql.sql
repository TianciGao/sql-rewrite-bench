CREATE TABLE `complete_cast` (
    id INT NOT NULL PRIMARY KEY,
    movie_id INT,
    subject_id INT NOT NULL,
    status_id INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `comp_cast_type` (
    id INT NOT NULL PRIMARY KEY,
    kind VARCHAR(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `company_name` (
    id INT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    country_code VARCHAR(255),
    imdb_id INT,
    name_pcode_nf VARCHAR(5),
    name_pcode_sf VARCHAR(5),
    md5sum VARCHAR(32)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `company_type` (
    id INT NOT NULL PRIMARY KEY,
    kind VARCHAR(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `keyword` (
    id INT NOT NULL PRIMARY KEY,
    keyword TEXT NOT NULL,
    phonetic_code VARCHAR(5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `link_type` (
    id INT NOT NULL PRIMARY KEY,
    link VARCHAR(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `movie_companies` (
    id INT NOT NULL PRIMARY KEY,
    movie_id INT NOT NULL,
    company_id INT NOT NULL,
    company_type_id INT NOT NULL,
    note TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `movie_info` (
    id INT NOT NULL PRIMARY KEY,
    movie_id INT NOT NULL,
    info_type_id INT NOT NULL,
    info TEXT NOT NULL,
    note TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `movie_keyword` (
    id INT NOT NULL PRIMARY KEY,
    movie_id INT NOT NULL,
    keyword_id INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `movie_link` (
    id INT NOT NULL PRIMARY KEY,
    movie_id INT NOT NULL,
    linked_movie_id INT NOT NULL,
    link_type_id INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `title` (
    id INT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    imdb_index VARCHAR(12),
    kind_id INT NOT NULL,
    production_year INT,
    imdb_id INT,
    phonetic_code VARCHAR(5),
    episode_of_id INT,
    season_nr INT,
    episode_nr INT,
    series_years VARCHAR(49),
    md5sum VARCHAR(32)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
