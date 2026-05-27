-- case_id: PORT_0007
-- draft source id: PORT_PARROT_DRAFT_0001
-- draft-only / not validated
-- target dialect: spark_like_positive
-- DRAFT: Spark adaptation requires review
SELECT text
FROM comments
WHERE postid IN (
  SELECT id
  FROM posts
  WHERE viewcount BETWEEN 100 AND 150
)
ORDER BY CASE WHEN score IS NULL THEN 1 ELSE 0 END, score DESC
LIMIT 1
