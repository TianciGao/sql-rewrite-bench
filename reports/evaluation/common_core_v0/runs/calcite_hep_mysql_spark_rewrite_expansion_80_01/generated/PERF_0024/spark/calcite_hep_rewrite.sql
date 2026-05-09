SELECT `supplier`.`s_name`, `supplier`.`s_address`
FROM `supplier`
CROSS JOIN `nation`
WHERE `supplier`.`s_suppkey` IN (SELECT `ps_suppkey`
FROM `partsupp`
WHERE `ps_partkey` IN (SELECT `p_partkey`
FROM `part`
WHERE `p_name` LIKE 'pale%') AND CAST(`ps_availqty` AS DECIMAL(19, 1)) > (SELECT 0.5 * SUM(`l_quantity`)
FROM `lineitem`
WHERE `l_partkey` = `partsupp`.`ps_partkey` AND `l_suppkey` = `partsupp`.`ps_suppkey` AND `l_shipdate` >= DATE '1997-01-01' AND `l_shipdate` < (DATE '1997-01-01' + INTERVAL '1' YEAR))) AND `supplier`.`s_nationkey` = `nation`.`n_nationkey` AND `nation`.`n_name` = 'BRAZIL'
ORDER BY `supplier`.`s_name` NULLS LAST
