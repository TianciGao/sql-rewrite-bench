from pathlib import Path
from contextlib import redirect_stdout
import re

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType, LongType, DoubleType
)

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_SQL = ROOT / "datasets/raw/job/staged/job/schema.sql"
CSV_DIR = ROOT / "datasets/loaded/job_perf0003_pg"
CASE_DIR = ROOT / "cases" / "PERF" / "PERF_0003"
RUN_DIR = ROOT / "runs" / "perf_0003" / "spark"
PLAN_DIR = ROOT / "runs" / "perf_0003" / "plans" / "spark"

TARGETS = [
    "complete_cast",
    "comp_cast_type",
    "company_name",
    "company_type",
    "keyword",
    "link_type",
    "movie_companies",
    "movie_info",
    "movie_keyword",
    "movie_link",
    "title",
]


def extract_create_blocks(schema_text: str) -> dict[str, str]:
    lines = schema_text.splitlines()
    blocks: dict[str, str] = {}
    capturing = False
    current = None
    buf = []

    for line in lines:
        m = re.match(r"^\s*create\s+table\s+([A-Za-z_][A-Za-z0-9_]*)", line, re.IGNORECASE)
        if m:
            name = m.group(1).lower()
            if name in TARGETS:
                capturing = True
                current = name
                buf = [line]
                continue

        if capturing:
            buf.append(line)
            if ";" in line:
                blocks[current] = "\n".join(buf)
                capturing = False
                current = None
                buf = []

    return blocks


def sql_type_to_spark(type_text: str):
    t = type_text.lower().strip()

    if t.startswith("integer") or t.startswith("serial") or t.startswith("smallint"):
        return IntegerType()
    if t.startswith("bigint") or t.startswith("bigserial"):
        return LongType()
    if t.startswith("double precision") or t.startswith("real") or t.startswith("numeric") or t.startswith("decimal"):
        return DoubleType()

    # JOB text/varchar/char/date/timestamp 等，先统一成字符串最稳
    return StringType()


def parse_structs(schema_sql_path: Path) -> dict[str, StructType]:
    text = schema_sql_path.read_text(encoding="utf-8", errors="ignore")
    blocks = extract_create_blocks(text)

    missing = set(TARGETS) - set(blocks)
    if missing:
        raise RuntimeError(f"Missing CREATE TABLE blocks: {sorted(missing)}")

    schemas = {}

    for table in TARGETS:
        fields = []
        for raw in blocks[table].splitlines():
            s = raw.strip()
            low = s.lower()

            if not s:
                continue
            if low.startswith("create table"):
                continue
            if s == "(" or s == ");":
                continue
            if low.startswith("primary key"):
                continue
            if low.startswith("foreign key"):
                continue
            if low.startswith("unique "):
                continue
            if low.startswith("constraint"):
                continue

            m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+(.+?)(?:,)?\s*$", raw)
            if not m:
                continue

            col = m.group(1)
            rest = m.group(2)

            # 去掉 NOT NULL / DEFAULT 等尾部描述
            rest = re.split(r"\s+not\s+null|\s+default\s+", rest, maxsplit=1, flags=re.IGNORECASE)[0]
            dtype = sql_type_to_spark(rest)

            fields.append(StructField(col, dtype, True))

        schemas[table] = StructType(fields)

    return schemas


def rows_to_text(rows):
    def norm(v):
        return "" if v is None else str(v)
    return "\n".join("\t".join(norm(x) for x in row) for row in rows)


def load_tables(spark: SparkSession):
    schemas = parse_structs(SCHEMA_SQL)

    print("=== Spark table loading ===")
    for table in TARGETS:
        csv_path = CSV_DIR / f"{table}.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        df = (
            spark.read
            .option("header", "false")
            .option("inferSchema", "false")
            .option("quote", '"')
            .option("escape", '"')
            .option("nullValue", "")
            .schema(schemas[table])
            .csv(str(csv_path))
        )

        df.createOrReplaceTempView(table)
        print(f"{table}\tREGISTERED")


def run_query(spark: SparkSession, sql_file: str):
    sql_path = CASE_DIR / sql_file
    base = sql_path.stem
    query = sql_path.read_text(encoding="utf-8")

    df = spark.sql(query)
    rows = [tuple(r) for r in df.collect()]

    RUN_DIR.mkdir(parents=True, exist_ok=True)
    PLAN_DIR.mkdir(parents=True, exist_ok=True)

    (RUN_DIR / f"{base}.tsv").write_text(rows_to_text(rows) + "\n", encoding="utf-8")

    with (PLAN_DIR / f"{base}.txt").open("w", encoding="utf-8") as f:
        with redirect_stdout(f):
            df.explain(mode="formatted")

    print(f"=== Spark :: PERF_0003 :: {base} ===")
    print(rows_to_text(rows))
    print()


def main():
    spark = (
        SparkSession.builder
        .appName("perf_0003_spark_run")
        .master("local[4]")
        .config("spark.driver.memory", "8g")
        .config("spark.executor.memory", "8g")
        .config("spark.sql.shuffle.partitions", "32")
        .config("spark.sql.files.maxPartitionBytes", "64m")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )

    try:
        load_tables(spark)
        for rel in ["source.sql", "rewrite_pos_01.sql", "rewrite_neg_01.sql"]:
            run_query(spark, rel)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()