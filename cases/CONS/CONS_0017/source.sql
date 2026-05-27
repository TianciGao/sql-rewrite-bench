SELECT *,
       EXISTS (
         SELECT *
         FROM (
           SELECT e2.deptno
           FROM tmp_emps e2
           WHERE e1.commission = e2.commission
         ) AS table3
         WHERE table3.deptno <> e1.deptno
       )
FROM tmp_emps e1;
