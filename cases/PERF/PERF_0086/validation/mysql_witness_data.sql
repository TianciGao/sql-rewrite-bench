-- Case-local witness data for PERF_0086 on MySQL
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO aka_name (id, name, person_id) VALUES (1, 'Alpha Person', 1);
INSERT INTO aka_name (id, name, person_id) VALUES (101, 'Alpha Person', 1);

INSERT INTO cast_info (id, movie_id, note, person_id, role_id) VALUES (1, 1, '(voice: English version)', 1, 1);

INSERT INTO company_name (id, country_code) VALUES (1, '[jp]');

INSERT INTO movie_companies (id, company_id, movie_id, note) VALUES (1, 1, 1, 'pre(Japan)post');

INSERT INTO name (id, name) VALUES (1, 'preYopost');

INSERT INTO role_type (id, role) VALUES (1, 'actress');

INSERT INTO title (id, title) VALUES (1, 'Alpha Movie');
