import re
from pathlib import Path
from contextlib import redirect_stdout
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType, LongType, DecimalType, DoubleType
)

ROOT = Path(__file__).resolve().parent.parent
DDL_PATH = ROOT / "datasets/raw/tpcds/DSGen-software-code-4.0.0/tools/tpcds.sql"
DATA_DIR = ROOT / "datasets/loaded/tpcds_sf1_perf0002_pg"
SQL_PATH = ROOT / "cases/PERF/PERF_0002/source.sql"
OUT_DIR = ROOT / "runs/perf_0002/plans/spark"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = ["date_dim", "item", "store", "store_sales"]

def parse_table_ddls(ddl_path: Path, targets):
    text = ddl_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    found = {}
    capturing = False
    current = None
    buf = []

    for line in text:
        m = re.match(r'^\s*create\s+table\s+([A-Za-z_][A-Za-z0-9_]*)', line, re.IGNORECASE)
        if m:
            name = m.group(1).lower()
            if name in targets:
                capturing = True
                current = name
                buf = [line]
                continue

        if capturing:
            buf.append(line)
            if ';' in line:
                found[current] = list(buf)
                capturing = False
                current = None
                buf = []

    missing = [t for t in targets if t not in found]
    if missing:
        raise RuntimeError(f"Missing DDL for: {missing}")
    return found

def parse_columns(lines):
    cols = []
    col_re = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z]+(?:\(\d+(?:,\s*\d+)?\))?)', re.IGNORECASE)
    for line in lines[1:]:
        s = line.strip().rstrip(',')
        if not s or s in {"(", ")", ");"} or s.startswith(')'):
            continue
        head = s.split()[0].lower()
        if head in {"primary", "foreign", "constraint", "unique", "key"}:
            continue
        m = col_re.match(s)
        if not m:
            continue
        cols.append((m.group(1), m.group(2)))
    return cols

def spark_type(sql_type: str):
    t = sql_type.upper()
    if t.startswith("VARCHAR") or t.startswith("CHAR"):
        return StringType()
    if t.startswith("DECIMAL") or t.startswith("NUMERIC"):
        m = re.match(r'^(?:DECIMAL|NUMERIC)\((\d+),\s*(\d+)\)$', t)
        if m:
            return DecimalType(int(m.group(1)), int(m.group(2)))
        return DoubleType()
    if t.startswith("BIGINT"):
        return LongType()
    if t.startswith("INTEGER") or t.startswith("INT") or t.startswith("SMALLINT"):
        return IntegerType()
    if t.startswith("DATE") or t.startswith("TIMESTAMP") or t.startswith("TIME"):
        return StringType()
    return StringType()

def build_schema(cols):
    return StructType([StructField(name, spark_type(tp), True) for name, tp in cols])

table_ddls = parse_table_ddls(DDL_PATH, TARGETS)

spark = (
    SparkSession.builder
    .appName("sql-rewrite-bench-perf-0002-plans")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

for table in TARGETS:
    cols = parse_columns(table_ddls[table])
    schema = build_schema(cols)
    path = DATA_DIR / f"{table}.dat"
    df = (
        spark.read
        .option("sep", "|")
        .option("header", "false")
        .option("quote", "\u0000")
        .schema(schema)
        .csv(str(path))
    )
    df.createOrReplaceTempView(table)

sql_text = SQL_PATH.read_text(encoding="utf-8")
result = spark.sql(sql_text)

out_path = OUT_DIR / "source.txt"
with out_path.open("w", encoding="utf-8") as f:
    with redirect_stdout(f):
        result.explain(mode="formatted")

print(f"Wrote {out_path}")
spark.stop()
