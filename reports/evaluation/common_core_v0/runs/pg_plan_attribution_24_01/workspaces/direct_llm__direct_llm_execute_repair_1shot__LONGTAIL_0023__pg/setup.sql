drop schema if exists attr24_direct_llm__direct_llm_execute_repair_1shot__longtail cascade;
create schema attr24_direct_llm__direct_llm_execute_repair_1shot__longtail;
set search_path to attr24_direct_llm__direct_llm_execute_repair_1shot__longtail;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/LONGTAIL/LONGTAIL_0023/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/LONGTAIL/LONGTAIL_0023/validation/pg_witness_data.sql
