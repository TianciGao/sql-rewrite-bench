set search_path to attr24_direct_llm__direct_llm_same_engine_rewrite__port_0003;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
-- case_id: PORT_0003
-- draft source id: PORT_PARROT_DRAFT_0002
-- draft-only / not validated
-- source dialect: postgres_like_candidate
SELECT "gsoffered" FROM "schools" ORDER BY ABS( "longitude" ) DESC NULLS LAST LIMIT 1;
rollback;
