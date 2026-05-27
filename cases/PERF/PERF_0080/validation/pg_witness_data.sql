-- PostgreSQL witness data for PERF_0080
-- draft_origin: JOB_DRAFT_0001

INSERT INTO company_type (id, kind) VALUES (1, 'production companies');
INSERT INTO company_type (id, kind) VALUES (2, 'distributors');

INSERT INTO info_type (id, info) VALUES (1, 'bottom 10 rank');

INSERT INTO movie_companies (id, company_type_id, movie_id, note) VALUES (1, 1, 1, 'Alpha Production');
INSERT INTO movie_companies (id, company_type_id, movie_id, note) VALUES (2, 2, 2, 'Beta Distribution');
INSERT INTO movie_companies (id, company_type_id, movie_id, note) VALUES (3, 1, 3, '(as Metro-Goldwyn-Mayer Pictures)');

INSERT INTO movie_info_idx (id, movie_id, info_type_id, info) VALUES (1, 1, 1, '6.1');
INSERT INTO movie_info_idx (id, movie_id, info_type_id, info) VALUES (2, 2, 1, '7.4');
INSERT INTO movie_info_idx (id, movie_id, info_type_id, info) VALUES (3, 3, 1, '8.5');

INSERT INTO title (id, production_year, title) VALUES (1, 2006, 'Alpha Baseline');
INSERT INTO title (id, production_year, title) VALUES (2, 2007, 'Beta Baseline');
INSERT INTO title (id, production_year, title) VALUES (3, 2008, 'Metro Guardrail');
