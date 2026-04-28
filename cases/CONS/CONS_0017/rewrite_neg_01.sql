SELECT e1.*, CASE WHEN EXISTS (
         SELECT 1
         FROM tmp_emps e2
         WHERE e2.commission = e1.commission
       ) THEN TRUE ELSE FALSE END
FROM tmp_emps e1;
