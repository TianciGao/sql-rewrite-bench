from pathlib import Path
from contextlib import redirect_stdout
from pyspark.sql import SparkSession

ROOT = Path(__file__).resolve().parents[1]

def rows_to_text(rows):
    def norm(v):
        return "" if v is None else str(v)
    return "\n".join("\t".join(norm(x) for x in row) for row in rows)

spark = (
    SparkSession.builder
    .appName("longtail-0002-spark")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

users = [
    (1, "Alice", 1000),
    (2, "Bob", 800),
    (3, "Carol", 700),
    (4, "Dave", 500),
]
posts = [
    (101, 1, 1, 10, 100),
    (102, 1, 2, 7, 90),
    (103, 1, 2, 5, 80),
    (201, 2, 1, 8, 50),
    (202, 2, 1, 7, 70),
    (301, 3, 2, 8, 40),
    (401, 4, 1, 2, 10),
    (402, 4, 2, 3, 30),
]
badges = [
    (1, 1, 1, "Teacher"),
    (2, 1, 2, "Student"),
    (3, 2, 3, "Supporter"),
    (4, 3, 2, "Editor"),
]

spark.createDataFrame(users, "Id long, DisplayName string, Reputation long").createOrReplaceTempView("Users")
spark.createDataFrame(posts, "Id long, OwnerUserId long, PostTypeId long, Score long, ViewCount long").createOrReplaceTempView("Posts")
spark.createDataFrame(badges, "Id long, UserId long, Class long, Name string").createOrReplaceTempView("Badges")

out_dir = ROOT / "runs" / "longtail_0002" / "spark"
plan_dir = ROOT / "runs" / "longtail_0002" / "plans" / "spark"
out_dir.mkdir(parents=True, exist_ok=True)
plan_dir.mkdir(parents=True, exist_ok=True)

for rel in ["source.sql", "rewrite_pos_01.sql", "rewrite_neg_01.sql"]:
    sql_path = ROOT / "cases" / "LONGTAIL" / "LONGTAIL_0002" / rel
    base = sql_path.stem
    query = sql_path.read_text(encoding="utf-8")
    df = spark.sql(query)
    rows = [tuple(r) for r in df.collect()]

    (out_dir / f"{base}.tsv").write_text(rows_to_text(rows) + "\n", encoding="utf-8")

    with (plan_dir / f"{base}.txt").open("w", encoding="utf-8") as f:
        with redirect_stdout(f):
            df.explain(mode="formatted")

    print(f"=== Spark :: LONGTAIL_0002 :: {base} ===")
    print(rows_to_text(rows))
    print()

spark.stop()
