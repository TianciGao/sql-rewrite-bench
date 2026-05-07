/* case_id: PORT_0004 */ /* draft source id: PORT_PARROT_DRAFT_0004 */ /* draft-only / not validated */ /* source dialect: mysql_like_candidate */
SELECT
  CAST(SUM(CASE WHEN `patient`.`sex` = 'F' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`patient`.`id`) AS `_col_0`
FROM `patient` AS `patient`
WHERE
  `patient`.`diagnosis` = 'RA'
  AND DATE_FORMAT(CAST(`patient`.`birthday` AS TIMESTAMP), '%yyyy') = '1980'
