drop schema if exists attr113_direct_llm_direct_llm_same_engine_rewrite_longtail_0 cascade;
create schema attr113_direct_llm_direct_llm_same_engine_rewrite_longtail_0;
set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_longtail_0;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/LONGTAIL/LONGTAIL_0024/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/LONGTAIL/LONGTAIL_0024/validation/pg_witness_data.sql
