-- MySQL witness data for PERF_0084
-- draft_origin: JOB_DRAFT_0012

INSERT INTO company_name (id, country_code, name) VALUES (1, '[us]', 'Alpha Studio');
INSERT INTO company_name (id, country_code, name) VALUES (2, '[gb]', 'Beta Studio');
INSERT INTO company_name (id, country_code, name) VALUES (3, '[us]', 'Gamma Guardrail');

INSERT INTO company_type (id, kind) VALUES (1, 'production companies');

INSERT INTO info_type (id, info) VALUES (1, 'genres');
INSERT INTO info_type (id, info) VALUES (2, 'rating');

INSERT INTO movie_companies (id, company_id, company_type_id, movie_id) VALUES (1, 1, 1, 1);
INSERT INTO movie_companies (id, company_id, company_type_id, movie_id) VALUES (2, 2, 1, 2);
INSERT INTO movie_companies (id, company_id, company_type_id, movie_id) VALUES (3, 3, 1, 3);

INSERT INTO movie_info (id, movie_id, info_type_id, info) VALUES (1, 1, 1, 'Drama');
INSERT INTO movie_info (id, movie_id, info_type_id, info) VALUES (2, 2, 1, 'Horror');
INSERT INTO movie_info (id, movie_id, info_type_id, info) VALUES (3, 3, 1, 'Comedy');

INSERT INTO movie_info_idx (id, movie_id, info_type_id, info) VALUES (1, 1, 2, '8.7');
INSERT INTO movie_info_idx (id, movie_id, info_type_id, info) VALUES (2, 2, 2, '8.9');
INSERT INTO movie_info_idx (id, movie_id, info_type_id, info) VALUES (3, 3, 2, '9.1');

INSERT INTO title (id, production_year, title) VALUES (1, 2006, 'Alpha Drama');
INSERT INTO title (id, production_year, title) VALUES (2, 2007, 'Beta Horror');
INSERT INTO title (id, production_year, title) VALUES (3, 2008, 'Gamma Comedy');
