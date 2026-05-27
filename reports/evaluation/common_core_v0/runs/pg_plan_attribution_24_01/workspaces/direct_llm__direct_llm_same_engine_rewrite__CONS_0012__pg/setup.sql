drop schema if exists attr24_direct_llm__direct_llm_same_engine_rewrite__cons_0012 cascade;
create schema attr24_direct_llm__direct_llm_same_engine_rewrite__cons_0012;
set search_path to attr24_direct_llm__direct_llm_same_engine_rewrite__cons_0012;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0012/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0012/validation/pg_witness_data.sql
