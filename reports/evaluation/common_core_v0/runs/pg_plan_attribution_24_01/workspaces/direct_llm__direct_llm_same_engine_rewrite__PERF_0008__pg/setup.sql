drop schema if exists attr24_direct_llm__direct_llm_same_engine_rewrite__perf_0008 cascade;
create schema attr24_direct_llm__direct_llm_same_engine_rewrite__perf_0008;
set search_path to attr24_direct_llm__direct_llm_same_engine_rewrite__perf_0008;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0008/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0008/validation/pg_witness_data.sql
