-- MySQL witness data for PERF_0078
-- draft_origin: JOB_DRAFT_0017

INSERT INTO cast_info (id, movie_id, person_id) VALUES (1, 1, 1);
INSERT INTO cast_info (id, movie_id, person_id) VALUES (101, 1, 1);

INSERT INTO company_name (id, country_code) VALUES (1, '[us]');
INSERT INTO company_name (id, country_code) VALUES (2, '[gb]');

INSERT INTO keyword (id, keyword) VALUES (1, 'character-name-in-title');

INSERT INTO movie_companies (id, company_id, movie_id) VALUES (1, 1, 1);
INSERT INTO movie_companies (id, company_id, movie_id) VALUES (2, 2, 2);

INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (1, 1, 1);
INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (2, 1, 2);

INSERT INTO name (id, name) VALUES (1, 'Btail');
INSERT INTO name (id, name) VALUES (2, 'Ctail');

INSERT INTO title (id) VALUES (1);
INSERT INTO title (id) VALUES (2);

INSERT INTO cast_info (id, movie_id, person_id) VALUES (2, 2, 2);
INSERT INTO cast_info (id, movie_id, person_id) VALUES (3, 1, 2);
