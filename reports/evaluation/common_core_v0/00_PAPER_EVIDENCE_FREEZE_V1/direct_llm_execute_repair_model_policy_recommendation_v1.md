# Direct LLM Execute-and-Repair Model Policy Recommendation v1

This is a read-only policy note based on retained Direct LLM generation artifacts. No LLM calls were made. No DB, checker, or timing runs were performed.

## Findings

1. Is the original Direct LLM model explicitly recorded?

Yes. The retained generation packet explicitly records:
- provider: `api.gptsapi.net`
- base URL family: `https://api.gptsapi.net/v1`
- model: `gpt-4o-mini`

2. Is the original prompt template explicitly recorded?

Yes. The retained runner and generation plan both reference:
- `reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_prompt_template.md`

In addition, the realized run retained per-row materialized prompt files under:
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/prompts/<case_id>/<engine>/prompt.txt`

3. Is the original temperature / decoding policy explicitly recorded?

Yes. The retained generation artifacts explicitly record:
- `temperature = 0`
- `top_p = 1`
- `max_tokens = 2048`
- `seed_if_available = null`

4. Can Execute-and-Repair safely use the same model/policy?

Partially.

It is safe to say the original first-pass route used the retained model/prompt family above. It is not safe to claim strict reproducibility parity unless the repair route explicitly freezes:
- the exact model identifier
- the exact provider/runtime
- the repair prompt template
- temperature / top_p / max_tokens
- output contract
- any extraction / post-processing rule

Because the repair route adds feedback fields and changes the prompt task, it should be treated as a separately versioned route even if it reuses `gpt-4o-mini`.

5. If not, what must be frozen before repair?

Freeze all of the following before any actual Execute-and-Repair run:
- repair route id and protocol name
- model identifier
- provider / runtime endpoint family
- repair prompt template
- temperature
- top_p
- max_tokens
- candidate count (`1`)
- extraction rule / output acceptance rule
- retry policy (`0` or `1` retries must be stated explicitly, not implied)
- timestamped run manifest

6. Recommended repair model policy

- If you want the closest possible family match, reuse the explicitly retained original model string: `gpt-4o-mini`.
- Even then, mark the repair baseline as separately versioned because the prompt and task are different.
- If you do not want to rely on the original provider/runtime family, freeze a new repair model policy and state clearly that Direct LLM + Repair is a new route, not model-identity-equivalent evidence.

Recommended paper-safe stance:
- use the same model only if the realized run metadata is explicitly cited from the retained generation packet
- otherwise freeze a new model policy and mark the repair route as separately versioned from original Direct LLM

## Boundary

Do not claim Direct LLM + Repair is directly comparable to original Direct LLM on model identity unless model identity is confirmed from the retained generation packet and the repair route’s own model policy is frozen before execution.
