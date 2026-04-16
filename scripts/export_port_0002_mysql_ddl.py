from pathlib import Path
import os
import sys
import pymysql

table = "votes"

host = os.environ.get("MYSQL_HOST", "127.0.0.1")
port = int(os.environ.get("MYSQL_PORT", "3306"))
user = os.environ.get("MYSQL_USER", "bench")
password = os.environ.get("MYSQL_PASSWORD", "benchpass")
database = os.environ.get("MYSQL_DATABASE", "bench")

out = Path("cases/PORT/PORT_0002/schema/ddl_mysql.sql")
out.parent.mkdir(parents=True, exist_ok=True)

print("=== export_port_0002_mysql_ddl.py ===")
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
        cur.execute(f"SHOW CREATE TABLE `{table}`")
        row = cur.fetchone()
        if not row or len(row) < 2:
            raise RuntimeError(f"SHOW CREATE TABLE returned unexpected result: {row!r}")
        ddl = row[1]
        f.write(ddl.rstrip() + ";\n")
finally:
    conn.close()

print(f"[OK] wrote {out}")
