drop schema if exists attr24_direct_llm__direct_llm_execute_repair_1shot__perf_001 cascade;
create schema attr24_direct_llm__direct_llm_execute_repair_1shot__perf_001;
set search_path to attr24_direct_llm__direct_llm_execute_repair_1shot__perf_001;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0019/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0019/validation/pg_witness_data.sql
