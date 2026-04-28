INSERT INTO emp (empno, ename, job, mgr, hiredate, sal, comm, deptno) VALUES
(1, 'ALICE', 'CLERK', NULL, '2020-01-01', 50.00, 3.00, 10),
(2, 'BOB', 'CLERK', NULL, '2020-01-02', 250.00, 2.00, 20);
INSERT INTO bonus (ename, job, sal, comm) VALUES
('X', 'CLERK', 100.00, 0.00),
('Y', 'MANAGER', 300.00, 0.00);
INSERT INTO dept (deptno, dname, loc) VALUES
(10, 'ACCOUNTING', 'NEW YORK'),
(10, 'ACCOUNTING_AUX', 'BOSTON'),
(20, 'RESEARCH', 'DALLAS');
