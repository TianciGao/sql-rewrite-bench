SELECT `ename` `ENAME`
FROM `emp`
WHERE EXISTS (SELECT *
FROM `dept`
LEFT JOIN `bonus` ON `dept`.`dname` = `bonus`.`ename` AND `bonus`.`job` = `emp`.`job`
WHERE `bonus`.`ename` IS NULL)
