set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_port_0008_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT t2.admemail1, t2.admemail2 FROM frpm AS t1 INNER JOIN schools AS t2 ON t1.cdscode = t2.cdscode WHERE t2.county = 'San Bernardino' AND t2.city = 'San Bernardino' AND t2.doc::integer = 54 AND EXTRACT(YEAR FROM t2.opendate) BETWEEN 2009 AND 2010 AND t2.soc::integer = 62;
rollback;
