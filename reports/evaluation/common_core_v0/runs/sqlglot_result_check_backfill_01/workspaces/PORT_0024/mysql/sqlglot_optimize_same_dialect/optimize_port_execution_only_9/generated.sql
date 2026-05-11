SELECT
  CAST(SUM(
    CASE
      WHEN `cards`.`isstoryspotlight` = 1 AND `cards`.`istextless` = 0
      THEN 1
      ELSE 0
    END
  ) AS DOUBLE) * 100 / COUNT(`cards`.`id`) AS `_col_0`
FROM `cards` AS `cards`
