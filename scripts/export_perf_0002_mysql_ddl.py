from pathlib import Path
import os
import sys
import pymysql

tables = ["date_dim", "item", "store", "store_sales"]

host = os.environ.get("MYSQL_HOST", "127.0.0.1")
port = int(os.environ.get("MYSQL_PORT", "3306"))
user = os.environ.get("MYSQL_USER", "bench")
password = os.environ.get("MYSQL_PASSWORD", "benchpass")
database = os.environ.get("MYSQL_DATABASE", "bench")

out = Path("cases/PERF/PERF_0002/schema/ddl_mysql.sql")
out.parent.mkdir(parents=True, exist_ok=True)

print("=== export_perf_0002_mysql_ddl.py ===")
print(f"MYSQL_HOST={host}")
print(f"MYSQL_PORT={port}")
print(f"MYSQL_DATABASE={database}")
print(f"MYSQL_USER={user}")

try:
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )
except Exception as e:
    print(f"[ERROR] failed to connect to MySQL: {e}", file=sys.stderr)
    raise

try:
    with conn.cursor() as cur, out.open("w", encoding="utf-8") as f:
        for t in tables:
            print(f"[INFO] exporting {t}")
            cur.execute(f"SHOW CREATE TABLE `{t}`")
            row = cur.fetchone()
            if not row or len(row) < 2:
                raise RuntimeError(f"SHOW CREATE TABLE returned unexpected result for {t}: {row!r}")
            ddl = row[1]
            f.write(ddl.rstrip() + ";\n\n")
finally:
    conn.close()

print(f"[OK] wrote {out}")
