from pathlib import Path
from contextlib import redirect_stdout
from pyspark.sql import SparkSession

root = Path.cwd()
case_dir = root / "cases" / "PORT" / "PORT_0001"
out_dir = root / "runs" / "plans_port" / "spark"
out_dir.mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("sql-rewrite-bench-port-plans")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

data = [
    (1, "eng",   "2024-01-01 09:00:00"),
    (2, "eng",   "2024-01-31 23:59:59"),
    (3, "eng",   "2024-02-01 00:00:00"),
    (4, "sales", "2024-01-15 12:00:00"),
    (5, "sales", "2023-01-20 08:00:00"),
]
df = spark.createDataFrame(data, ["event_id", "dept", "event_ts_str"])
df = df.selectExpr("event_id", "dept", "CAST(event_ts_str AS TIMESTAMP) AS event_ts")
df.createOrReplaceTempView("events_monthly")

for name in ["source", "rewrite_pos_01", "rewrite_neg_01"]:
    sql_text = (case_dir / f"{name}.sql").read_text(encoding="utf-8")
    result = spark.sql(sql_text)
    with open(out_dir / f"{name}.txt", "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            result.explain(mode="formatted")

spark.stop()
