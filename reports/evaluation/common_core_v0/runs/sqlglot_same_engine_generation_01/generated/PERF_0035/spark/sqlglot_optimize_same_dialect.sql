WITH `v1` AS (
  SELECT
    `i`.`i_category` AS `i_category`,
    `i`.`i_brand` AS `i_brand`,
    `cc`.`cc_name` AS `cc_name`,
    `d`.`d_year` AS `d_year`,
    `d`.`d_moy` AS `d_moy`,
    SUM(`cs`.`cs_sales_price`) AS `sum_sales`,
    AVG(SUM(`cs`.`cs_sales_price`)) OVER (PARTITION BY `i`.`i_category`, `i`.`i_brand`, `cc`.`cc_name`, `d`.`d_year`) AS `avg_monthly_sales`,
    RANK() OVER (
      PARTITION BY `i`.`i_category`, `i`.`i_brand`, `cc`.`cc_name`
      ORDER BY `d`.`d_year`, `d`.`d_moy`
    ) AS `rn`
  FROM `item` AS `i`
  JOIN `catalog_sales` AS `cs`
    ON `cs`.`cs_item_sk` = `i`.`i_item_sk`
  JOIN `call_center` AS `cc`
    ON `cc`.`cc_call_center_sk` = `cs`.`cs_call_center_sk`
  JOIN `date_dim` AS `d`
    ON `cs`.`cs_sold_date_sk` = `d`.`d_date_sk`
    AND (
      `d`.`d_moy` = 1 OR `d`.`d_moy` = 12 OR `d`.`d_year` = 2000
    )
    AND (
      `d`.`d_moy` = 1 OR `d`.`d_year` = 1999 OR `d`.`d_year` = 2000
    )
    AND (
      `d`.`d_moy` = 12 OR `d`.`d_year` = 2000 OR `d`.`d_year` = 2001
    )
    AND (
      `d`.`d_year` = 1999 OR `d`.`d_year` = 2000 OR `d`.`d_year` = 2001
    )
  GROUP BY
    `i`.`i_category`,
    `i`.`i_brand`,
    `cc`.`cc_name`,
    `d`.`d_year`,
    `d`.`d_moy`
)
SELECT
  `v1`.`cc_name` AS `cc_name`,
  `v1`.`d_year` AS `d_year`,
  `v1`.`d_moy` AS `d_moy`,
  `v1`.`avg_monthly_sales` AS `avg_monthly_sales`,
  `v1`.`sum_sales` AS `sum_sales`,
  `v1_lag`.`sum_sales` AS `psum`,
  `v1_lead`.`sum_sales` AS `nsum`
FROM `v1` AS `v1`
JOIN `v1` AS `v1_lag`
  ON `v1`.`cc_name` = `v1_lag`.`cc_name`
  AND `v1`.`i_brand` = `v1_lag`.`i_brand`
  AND `v1`.`i_category` = `v1_lag`.`i_category`
  AND `v1`.`rn` = `v1_lag`.`rn` + 1
JOIN `v1` AS `v1_lead`
  ON `v1`.`cc_name` = `v1_lead`.`cc_name`
  AND `v1`.`i_brand` = `v1_lead`.`i_brand`
  AND `v1`.`i_category` = `v1_lead`.`i_category`
  AND `v1`.`rn` = `v1_lead`.`rn` - 1
WHERE
  `v1`.`avg_monthly_sales` > 0
  AND `v1`.`d_year` = 2000
  AND CASE
    WHEN `v1`.`avg_monthly_sales` > 0
    THEN ABS(`v1`.`sum_sales` - `v1`.`avg_monthly_sales`) / `v1`.`avg_monthly_sales`
    ELSE NULL
  END > 0.1
ORDER BY
  `v1`.`sum_sales` - `v1`.`avg_monthly_sales`,
  `v1_lead`.`sum_sales`
LIMIT 100
