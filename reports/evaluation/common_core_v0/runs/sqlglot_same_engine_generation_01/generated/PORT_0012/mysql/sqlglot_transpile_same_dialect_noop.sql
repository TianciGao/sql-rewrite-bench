SELECT
  CAST(SUM(CASE WHEN 'sex' = 'F' THEN 1 ELSE 0 END) AS FLOAT) * 100 / NULLIF(COUNT('id'), 0)
FROM `patient`
WHERE
  'diagnosis' = 'RA' AND CAST(TIMESTAMP('birthday') AS CHAR) = '1980'
