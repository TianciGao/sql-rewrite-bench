-- MySQL witness data for PERF_0083
-- draft_origin: JOB_DRAFT_0006

INSERT INTO keyword (id, keyword) VALUES (1, 'marvel-cinematic-universe');

INSERT INTO name (id, name) VALUES (1, 'ADowneyQRobert');
INSERT INTO name (id, name) VALUES (2, 'DowneyZRobert');
INSERT INTO name (id, name) VALUES (3, 'Chris Example');

INSERT INTO title (id, production_year, title) VALUES (1, 2012, 'Alpha Marvel');
INSERT INTO title (id, production_year, title) VALUES (2, 2013, 'Beta Marvel');
INSERT INTO title (id, production_year, title) VALUES (3, 2014, 'Gamma Guardrail');

INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (1, 1, 1);
INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (2, 1, 2);
INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (3, 1, 3);

INSERT INTO cast_info (id, movie_id, person_id) VALUES (1, 1, 1);
INSERT INTO cast_info (id, movie_id, person_id) VALUES (2, 2, 2);
INSERT INTO cast_info (id, movie_id, person_id) VALUES (3, 3, 3);
