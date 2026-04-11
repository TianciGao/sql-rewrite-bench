from decimal import Decimal
from pathlib import Path

pg_path = Path("runs/perf_0002/pg/source.tsv")
my_path = Path("runs/perf_0002/mysql/source.tsv")
sp_path = Path("runs/perf_0002/spark/source.tsv")

def parse(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            raise ValueError(f"Unexpected row shape in {path}: {line!r}")
        rows.append((int(parts[0]), Decimal(parts[1]), Decimal(parts[2])))
    return rows

pg_rows = parse(pg_path)
my_rows = parse(my_path)
sp_rows = parse(sp_path)

print("=== PERF_0002 :: PG/MySQL/Spark source comparison ===")
print("pg_rows:", pg_rows)
print("mysql_rows:", my_rows)
print("spark_rows:", sp_rows)
print()
print("pg_vs_mysql:", pg_rows == my_rows)
print("pg_vs_spark:", pg_rows == sp_rows)
print("mysql_vs_spark:", my_rows == sp_rows)
