SELECT CASE WHEN COUNT(`l_extendedprice` * `l_discount`) = 0 THEN NULL ELSE COALESCE(SUM(`l_extendedprice` * `l_discount`), 0) END `revenue`
FROM `lineitem`
WHERE `l_shipdate` >= DATE '1995-01-01' AND `l_shipdate` < (DATE '1995-01-01' + INTERVAL '1' YEAR) AND `l_discount` >= 0.09 - 0.01 AND `l_discount` <= 0.09 + 0.01 AND `l_quantity` < 25
