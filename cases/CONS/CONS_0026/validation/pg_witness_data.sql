INSERT INTO dept (deptno, dname, loc) VALUES
(10, 'ACCOUNTING', 'NEW YORK'),
(20, 'SALES', 'CHICAGO'),
(30, 'RESEARCH', 'DALLAS');
INSERT INTO emp (empno, ename, job, mgr, hiredate, sal, comm, deptno) VALUES
(1, 'ALICE', 'CLERK', NULL, DATE '2020-01-01', 100.00, NULL, 10),
(2, 'BOB', 'CLERK', NULL, DATE '2020-01-02', 110.00, NULL, 10),
(3, 'CAROL', 'ANALYST', NULL, DATE '2020-01-03', 120.00, NULL, 30);
