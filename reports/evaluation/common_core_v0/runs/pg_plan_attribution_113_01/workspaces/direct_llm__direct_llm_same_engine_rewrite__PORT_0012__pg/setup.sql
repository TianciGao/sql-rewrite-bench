drop schema if exists attr113_direct_llm_direct_llm_same_engine_rewrite_port_0012_ cascade;
create schema attr113_direct_llm_direct_llm_same_engine_rewrite_port_0012_;
set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_port_0012_;
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0012/schema/ddl_pg.sql
\i /home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0012/validation/pg_witness_data.sql
