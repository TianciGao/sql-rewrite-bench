from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, LongType, StringType

ROOT = Path(__file__).resolve().parent.parent
CASE_DIR = ROOT / "cases/PORT/PORT_0002"
OUT_DIR = ROOT / "runs/port_0002/spark"
OUT_DIR.mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("sql-rewrite-bench-port-0002")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

schema = StructType([
    StructField("id", LongType(), False),
    StructField("creationdate", StringType(), False),
])

rows = [
    (1, "2010-01-05 10:00:00"),
    (2, "2010-06-12 09:30:00"),
    (3, "2010-12-31 23:59:59"),
    (4, "2011-02-01 08:00:00"),
    (5, "2011-09-09 14:15:00"),
    (6, "2012-01-01 00:00:00"),
]

df = spark.createDataFrame(rows, schema=schema)
df.createOrReplaceTempView("votes")

for name in ["rewrite_pos_02_spark", "rewrite_neg_02_spark"]:
    sql_text = (CASE_DIR / f"{name}.sql").read_text(encoding="utf-8")
    result = spark.sql(sql_text)
    out_path = OUT_DIR / f"{name}.tsv"
    with out_path.open("w", encoding="utf-8") as f:
        for row in result.collect():
            f.write("\t".join("" if v is None else str(v) for v in row) + "\n")
    print(f"Wrote {out_path}")
    print(out_path.read_text(encoding="utf-8").strip())

spark.stop()
