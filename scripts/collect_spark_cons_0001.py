from pathlib import Path
from contextlib import redirect_stdout
from pyspark.sql import SparkSession

root = Path.cwd()
case_dir = root / "cases" / "CONS" / "CONS_0001"
out_dir = root / "runs" / "plans_cons" / "spark"
out_dir.mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("sql-rewrite-bench-cons-plans")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

data = [
    (1, "eng", "alice", 10),
    (2, "eng", "bob", None),
    (3, "eng", "carol", 10),
    (4, "sales", "dan", None),
    (5, "sales", "emma", 20),
    (6, "hr", "frank", None),
]
df = spark.createDataFrame(data, ["emp_id", "dept", "emp_name", "manager_id"])
df.createOrReplaceTempView("employees_nulls")

for name in ["source", "rewrite_pos_01", "rewrite_neg_01"]:
    sql_text = (case_dir / f"{name}.sql").read_text(encoding="utf-8")
    result = spark.sql(sql_text)
    with open(out_dir / f"{name}.txt", "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            result.explain(mode="formatted")

spark.stop()
