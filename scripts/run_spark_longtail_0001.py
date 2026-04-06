from pathlib import Path
from pyspark.sql import SparkSession

root = Path.cwd()
case_dir = root / "cases" / "LONGTAIL" / "LONGTAIL_0001"
out_dir = root / "runs" / "longtail_case" / "spark"
out_dir.mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("sql-rewrite-bench-longtail-0001")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

data = [
    (1, "eng", "alice", 120),
    (2, "eng", "bob", 115),
    (3, "eng", "carol", 115),
    (4, "sales", "dan", 95),
    (5, "sales", "emma", 110),
    (6, "sales", "frank", 90),
]
df = spark.createDataFrame(data, ["emp_id", "dept", "emp_name", "salary"])
df.createOrReplaceTempView("employees")

for name in ["source", "rewrite_pos_01", "rewrite_neg_01"]:
    sql_text = (case_dir / f"{name}.sql").read_text(encoding="utf-8")
    result = spark.sql(sql_text)
    rows = result.collect()

    with open(out_dir / f"{name}.tsv", "w", encoding="utf-8") as f:
        for row in rows:
            f.write("\t".join(str(x) for x in row) + "\n")

    print(f"=== Spark :: {name} ===")
    for row in rows:
        print(row)

spark.stop()
