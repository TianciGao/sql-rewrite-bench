-- Case-local witness data for PERF_0085 on Spark
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO aka_name (id, name, person_id) VALUES (1, 'preapost', 1);
INSERT INTO aka_name (id, name, person_id) VALUES (101, 'preapost', 1);

INSERT INTO cast_info (id, movie_id, person_id) VALUES (1, 1, 1);

INSERT INTO info_type (id, info) VALUES (1, 'mini biography');

INSERT INTO link_type (id, link) VALUES (1, 'features');

INSERT INTO movie_link (id, link_type_id, linked_movie_id) VALUES (1, 1, 1);

INSERT INTO name (id, gender, name, name_pcode_cf) VALUES (1, 'f', 'Btail', 'A');

INSERT INTO person_info (id, info_type_id, note, person_id) VALUES (1, 1, 'Volker Boehm', 1);

INSERT INTO title (id, production_year, title) VALUES (1, 1980, 'Alpha Movie');
