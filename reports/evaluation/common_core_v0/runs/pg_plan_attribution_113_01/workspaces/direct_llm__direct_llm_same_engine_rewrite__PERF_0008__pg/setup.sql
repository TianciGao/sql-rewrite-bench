drop schema if exists attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0008_ cascade;
create schema attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0008_;
set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0008_;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0008/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0008/validation/pg_witness_data.sql
