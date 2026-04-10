#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

DDL_SQL="$PWD/datasets/raw/tpcds/DSGen-software-code-4.0.0/tools/tpcds.sql"
DATA_DIR="$PWD/datasets/loaded/tpcds_sf1_perf0002_pg"
TMP_DDL="$(mktemp)"

python - "$DDL_SQL" "$TMP_DDL" <<'PY'
import re
import sys
from pathlib import Path

ddl_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])

targets = {"date_dim", "item", "store", "store_sales"}
text = ddl_path.read_text(encoding="utf-8", errors="ignore").splitlines()

capturing = False
current = None
buf = []
found = set()
blocks = []

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
            blocks.extend(buf)
            blocks.append("")
            found.add(current)
            capturing = False
            current = None
            buf = []

missing = targets - found
if missing:
    raise SystemExit(f"Missing DDL for: {sorted(missing)}")

out_path.write_text("\n".join(blocks), encoding="utf-8")
print(f"Wrote extracted DDL to {out_path}")
PY

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 <<SQL
DROP TABLE IF EXISTS store_sales CASCADE;
DROP TABLE IF EXISTS store CASCADE;
DROP TABLE IF EXISTS item CASCADE;
DROP TABLE IF EXISTS date_dim CASCADE;
SQL

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 -f "$TMP_DDL"

for t in date_dim item store store_sales; do
  echo "=== loading $t ==="
  psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 \
    -c "\copy ${t} FROM '${DATA_DIR}/${t}.dat' WITH (FORMAT csv, DELIMITER '|', NULL '')"
done

echo
echo "=== row counts ==="
for t in date_dim item store store_sales; do
  psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At \
    -c "SELECT '${t}', COUNT(*) FROM ${t};"
done

rm -f "$TMP_DDL"
