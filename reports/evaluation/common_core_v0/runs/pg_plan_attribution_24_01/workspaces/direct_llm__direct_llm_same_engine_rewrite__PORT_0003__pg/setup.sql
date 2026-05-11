drop schema if exists attr24_direct_llm__direct_llm_same_engine_rewrite__port_0003 cascade;
create schema attr24_direct_llm__direct_llm_same_engine_rewrite__port_0003;
set search_path to attr24_direct_llm__direct_llm_same_engine_rewrite__port_0003;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0003/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0003/validation/pg_witness_data.sql
