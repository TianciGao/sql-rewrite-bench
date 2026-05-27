drop schema if exists attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0006_ cascade;
create schema attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0006_;
set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_perf_0006_;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/validation/pg_witness_data.sql
