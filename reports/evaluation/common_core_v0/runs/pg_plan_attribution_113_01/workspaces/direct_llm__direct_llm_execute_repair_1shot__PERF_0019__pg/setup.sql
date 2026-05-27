drop schema if exists attr113_direct_llm_direct_llm_execute_repair_1shot_perf_0019 cascade;
create schema attr113_direct_llm_direct_llm_execute_repair_1shot_perf_0019;
set search_path to attr113_direct_llm_direct_llm_execute_repair_1shot_perf_0019;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0019/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0019/validation/pg_witness_data.sql
