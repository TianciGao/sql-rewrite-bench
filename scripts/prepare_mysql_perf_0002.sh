#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

DDL_SQL="$PWD/datasets/raw/tpcds/DSGen-software-code-4.0.0/tools/tpcds.sql"
DATA_DIR="$PWD/datasets/loaded/tpcds_sf1_perf0002_pg"
TMP_DDL="$(mktemp)"
TMP_LOAD="$(mktemp)"

python - "$DDL_SQL" "$TMP_DDL" "$TMP_LOAD" "$DATA_DIR" <<'PY2'
import re
import sys
from pathlib import Path

ddl_path = Path(sys.argv[1])
ddl_out = Path(sys.argv[2])
load_out = Path(sys.argv[3])
data_dir = Path(sys.argv[4])

targets = ["date_dim", "item", "store", "store_sales"]
text = ddl_path.read_text(encoding="utf-8", errors="ignore").splitlines()

capturing = False
current = None
buf = []
found = {}
columns = {}

for line in text:
    m = re.match(r'^\s*create\s+table\s+([A-Za-z_][A-Za-z0-9_]*)', line, re.IGNORECASE)
    if m:
        name = m.group(1).lower()
        if name in targets:
            capturing = True
            current = name
            buf = [line]
            columns[current] = []
            continue

    if capturing:
        buf.append(line)

        s = line.strip().rstrip(',')

        # 跳过单独的 "("、")"、以及各种约束行
        if not s or s in {"(", ")"} or s.startswith(")") or s == ");":
            pass
        else:
            head = s.split()[0]
            head_l = head.lower()
            if head_l not in {"primary", "foreign", "constraint", "unique", "key"}:
                columns[current].append(head)

        if ';' in line:
            found[current] = list(buf)
            capturing = False
            current = None
            buf = []

missing = [t for t in targets if t not in found]
if missing:
    raise SystemExit(f"Missing DDL for: {missing}")

ddl_lines = []
for t in ["store_sales", "store", "item", "date_dim"]:
    ddl_lines.append(f"DROP TABLE IF EXISTS {t};")
ddl_lines.append("SET SESSION sql_mode='';")
ddl_lines.append("")

for t in targets:
    ddl_lines.extend(found[t])
    ddl_lines.append("")

ddl_out.write_text("\n".join(ddl_lines), encoding="utf-8")

load_lines = []
for t in targets:
    col_names = columns[t]
    vars_ = [f"@v{i+1}" for i in range(len(col_names))]
    set_clause = ", ".join(f"{c}=NULLIF({v},'')" for c, v in zip(col_names, vars_))
    data_file = str((data_dir / f"{t}.dat").resolve()).replace("\\", "/")
    load_lines.append(
        "LOAD DATA LOCAL INFILE '{path}'\n"
        "INTO TABLE {table}\n"
        "FIELDS TERMINATED BY '|'\n"
        "LINES TERMINATED BY '\\n'\n"
        "({vars})\n"
        "SET {set_clause};\n".format(
            path=data_file,
            table=t,
            vars=", ".join(vars_),
            set_clause=set_clause
        )
    )

load_out.write_text("\n".join(load_lines), encoding="utf-8")
print(f"Wrote DDL to {ddl_out}")
print(f"Wrote LOAD statements to {load_out}")
PY2

echo "=== checking local_infile ==="
mysql --local-infile=1 -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  -e "SHOW VARIABLES LIKE 'local_infile';"

mysql --local-infile=1 -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$TMP_DDL"
mysql --local-infile=1 -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$TMP_LOAD"

echo
echo "=== row counts ==="
for t in date_dim item store store_sales; do
  mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
    -e "SELECT '${t}', COUNT(*) FROM ${t};"
done

rm -f "$TMP_DDL" "$TMP_LOAD"
