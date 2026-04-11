from decimal import Decimal
from pathlib import Path

pg_path = Path("runs/perf_0002/pg/source.tsv")
my_path = Path("runs/perf_0002/mysql/source.tsv")

def parse(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            raise ValueError(f"Unexpected row shape in {path}: {line!r}")
        rows.append((
            int(parts[0]),
            Decimal(parts[1]),
            Decimal(parts[2])
        ))
    return rows

pg_rows = parse(pg_path)
my_rows = parse(my_path)

print("=== PERF_0002 :: PG vs MySQL source comparison ===")
print("pg_rows:", pg_rows)
print("mysql_rows:", my_rows)
print()
print("value_normalized_equal:", pg_rows == my_rows)
