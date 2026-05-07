SELECT
  CAST(SUM(0) AS FLOAT) * 100 / NULLIF(COUNT('id'), 0) AS `_col_0`
FROM `patient` AS `patient`
WHERE
  FALSE
