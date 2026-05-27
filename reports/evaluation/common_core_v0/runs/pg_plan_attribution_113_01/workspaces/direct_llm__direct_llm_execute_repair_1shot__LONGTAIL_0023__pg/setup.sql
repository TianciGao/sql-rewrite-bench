drop schema if exists attr113_direct_llm_direct_llm_execute_repair_1shot_longtail_ cascade;
create schema attr113_direct_llm_direct_llm_execute_repair_1shot_longtail_;
set search_path to attr113_direct_llm_direct_llm_execute_repair_1shot_longtail_;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/LONGTAIL/LONGTAIL_0023/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/LONGTAIL/LONGTAIL_0023/validation/pg_witness_data.sql
