SELECT *
FROM `t0`
WHERE `t0a` < (SELECT SUM(`c`)
FROM (SELECT `t1c` `c`
FROM `t1`
WHERE `t1a` = `t0`.`t0a`
UNION ALL
SELECT `t2c` `c`
FROM `t2`
WHERE `t2b` = `t0`.`t0b`) `t5`)
