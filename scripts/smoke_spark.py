from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("sql-rewrite-bench-smoke")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

data = [(1, "a"), (2, "b"), (3, "c")]
df = spark.createDataFrame(data, ["id", "val"])
df.createOrReplaceTempView("t")

result = spark.sql("SELECT id, val FROM t WHERE id >= 2 ORDER BY id")
result.show()

print("=== EXPLAIN FORMATTED ===")
result.explain(mode="formatted")

spark.stop()
