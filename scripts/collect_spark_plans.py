from pathlib import Path
from pyspark.sql import SparkSession
from contextlib import redirect_stdout

root = Path.cwd()
case_dir = root / "cases" / "PERF" / "PERF_0001"
out_dir = root / "runs" / "plans" / "spark"
out_dir.mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("sql-rewrite-bench-plans")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

data = [(1, "a"), (2, "b"), (3, "c")]
df = spark.createDataFrame(data, ["id", "val"])
df.createOrReplaceTempView("t")

for name in ["source", "rewrite_pos_01", "rewrite_neg_01"]:
    sql_text = (case_dir / f"{name}.sql").read_text(encoding="utf-8")
    result = spark.sql(sql_text)
    with open(out_dir / f"{name}.txt", "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            result.explain(mode="formatted")

spark.stop()
