| 检查 | 含义 |
|---|---|
| raw output exists | 方法确实返回了东西 |
| SQL extraction succeeds | 能从 raw output 中抽出 SQL，而不是解释文字 |
| candidate is non-empty | 不是空字符串、拒答、错误消息 |
| candidate is single statement | 不是多个混杂 SQL，除非 route 允许 |
| candidate has allowed statement type | 通常是 `SELECT` / `WITH SELECT`，不是 DDL/DML |
| target dialect / engine is known | 能知道它要送到 PG/MySQL/Spark 哪边跑 |
| optional parser/preflight passes | 如果 runner 有 parser/format gate，则通过基本语法门槛 |
| saved as candidate artifact | 有 candidate SQL 文件或 event row 可追溯 |这个判断的东西在哪里？https://github.com/TianciGao/sql-rewrite-bench
