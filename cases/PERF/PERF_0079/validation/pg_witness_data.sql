-- PostgreSQL witness data for PERF_0079
-- draft_origin: JOB_DRAFT_0010

INSERT INTO char_name (id, name) VALUES (1, 'Alpha Person');
INSERT INTO char_name (id, name) VALUES (2, 'Beta Person');

INSERT INTO cast_info (id, movie_id, note, person_role_id, role_id) VALUES (1, 1, 'x(voice)y(uncredited)z', 1, 1);
INSERT INTO cast_info (id, movie_id, note, person_role_id, role_id) VALUES (2, 2, '(voice)x(uncredited)tail', 2, 1);
INSERT INTO cast_info (id, movie_id, note, person_role_id, role_id) VALUES (3, 3, 'x(uncredited)z', 2, 1);

INSERT INTO company_name (id, country_code) VALUES (1, '[ru]');
INSERT INTO company_name (id, country_code) VALUES (2, '[ru]');
INSERT INTO company_name (id, country_code) VALUES (3, '[ru]');

INSERT INTO company_type (id) VALUES (1);

INSERT INTO movie_companies (id, company_id, company_type_id, movie_id) VALUES (1, 1, 1, 1);
INSERT INTO movie_companies (id, company_id, company_type_id, movie_id) VALUES (2, 2, 1, 2);
INSERT INTO movie_companies (id, company_id, company_type_id, movie_id) VALUES (3, 3, 1, 3);

INSERT INTO role_type (id, role) VALUES (1, 'actor');

INSERT INTO title (id, production_year, title) VALUES (1, 2006, 'Alpha Movie');
INSERT INTO title (id, production_year, title) VALUES (2, 2007, 'Beta Movie');
INSERT INTO title (id, production_year, title) VALUES (3, 2008, 'Gamma Movie');
