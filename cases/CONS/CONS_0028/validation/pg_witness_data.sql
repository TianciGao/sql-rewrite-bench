INSERT INTO emp (empno, ename, job, mgr, hiredate, sal, comm, deptno) VALUES
(1, 'ALICE', 'CLERK', NULL, DATE '2020-01-01', 500.00, 2.00, 10);
INSERT INTO bonus (ename, job, sal, comm) VALUES
('X', 'CLERK', 100.00, 0.00),
('Y', 'MANAGER', 200.00, 0.00);
INSERT INTO dept (deptno, dname, loc) VALUES
(10, 'ACCOUNTING', 'NEW YORK');
