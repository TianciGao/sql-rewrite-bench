drop schema if exists attr24_direct_llm__direct_llm_same_engine_rewrite__perf_0007 cascade;
create schema attr24_direct_llm__direct_llm_same_engine_rewrite__perf_0007;
set search_path to attr24_direct_llm__direct_llm_same_engine_rewrite__perf_0007;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0007/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0007/validation/pg_witness_data.sql
