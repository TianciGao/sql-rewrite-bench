-- Case-local witness data for PERF_0087 on MySQL
-- Prepared for future validation runs; no validation claim is made by package construction alone.

INSERT INTO company_name (id, country_code, name) VALUES (1, '[us]', 'preWarnerpost');
INSERT INTO company_name (id, country_code, name) VALUES (101, '[us]', 'preWarnerpost');

INSERT INTO company_type (id, kind) VALUES (1, 'production companies');

INSERT INTO keyword (id, keyword) VALUES (1, 'sequel');

INSERT INTO link_type (id, link) VALUES (1, 'prefollowpost');

INSERT INTO movie_companies (id, company_id, company_type_id, movie_id, note) VALUES (1, 1, 1, 1, NULL);

INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (1, 1, 1);

INSERT INTO movie_link (id, link_type_id, movie_id) VALUES (1, 1, 1);

INSERT INTO title (id, production_year, title) VALUES (1, '1950', 'Alpha Movie');
