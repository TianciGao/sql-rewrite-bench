SELECT *
FROM `tmp_emps`
WHERE EXISTS (SELECT *
FROM (SELECT `deptno`
FROM `tmp_emps` `tmp_emps0`
WHERE `commission` = `tmp_emps`.`commission`) `t0`
WHERE `deptno` <> `tmp_emps`.`deptno`)
