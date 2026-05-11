/* case_id: PORT_0005 */ /* draft source id: PORT_PARROT_DRAFT_0006 */ /* draft-only / not validated */ /* source dialect: postgres_like_candidate */
SELECT
  "drivers"."nationality" AS "nationality"
FROM "drivers" AS "drivers"
WHERE
  NOT "drivers"."dob" IS NULL
ORDER BY
  "drivers"."dob" NULLS FIRST
LIMIT 1
