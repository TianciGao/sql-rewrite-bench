-- Spark witness data for PERF_0081
-- draft_origin: JOB_DRAFT_0004

INSERT INTO info_type (id, info) VALUES (1, 'rating');
INSERT INTO info_type (id, info) VALUES (2, 'votes');

INSERT INTO keyword (id, keyword) VALUES (1, 'presequelpost');
INSERT INTO keyword (id, keyword) VALUES (2, 'great-sequel');
INSERT INTO keyword (id, keyword) VALUES (3, 'standalone');

INSERT INTO movie_info_idx (id, movie_id, info_type_id, info) VALUES (1, 1, 1, '7.2');
INSERT INTO movie_info_idx (id, movie_id, info_type_id, info) VALUES (2, 2, 2, '7.8');
INSERT INTO movie_info_idx (id, movie_id, info_type_id, info) VALUES (3, 3, 1, '4.5');

INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (1, 1, 1);
INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (2, 2, 2);
INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (3, 3, 3);

INSERT INTO title (id, production_year, title) VALUES (1, 2006, 'Alpha Rating Movie');
INSERT INTO title (id, production_year, title) VALUES (2, 2007, 'Beta Votes Movie');
INSERT INTO title (id, production_year, title) VALUES (3, 2008, 'Gamma Guardrail');
