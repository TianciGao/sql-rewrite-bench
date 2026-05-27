set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_port_0005_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
-- case_id: PORT_0005
-- draft source id: PORT_PARROT_DRAFT_0006
-- draft-only / not validated
-- source dialect: postgres_like_candidate
SELECT "nationality" FROM "drivers" WHERE NOT "dob" IS NULL ORDER BY "dob" ASC NULLS FIRST LIMIT 1;
rollback;
