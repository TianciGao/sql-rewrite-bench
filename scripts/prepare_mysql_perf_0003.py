#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_SQL = ROOT / "datasets/raw/job/staged/job/schema.sql"
CSV_DIR = ROOT / "datasets/loaded/job_perf0003_pg"
DDL_OUT = ROOT / "cases/PERF/PERF_0003/schema/ddl_mysql.sql"
PROFILE_JSON = ROOT / "cases/PERF/PERF_0003/data_profile.json"

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

MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "bench")
MYSQL_USER = os.environ.get("MYSQL_USER", "bench")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "benchpass")


def mysql_run_sql(sql: str, *, capture: bool = False) -> str:
    cmd = [
        "mysql",
        "--local-infile=1",
        "-N",
        "-B",
        "-h", MYSQL_HOST,
        "-P", str(MYSQL_PORT),
        "-u", MYSQL_USER,
        f"-p{MYSQL_PASSWORD}",
        MYSQL_DATABASE,
    ]
    res = subprocess.run(
        cmd,
        input=sql,
        text=True,
        capture_output=capture,
        check=True,
    )
    return res.stdout if capture else ""


def extract_create_blocks(schema_text: str) -> dict[str, str]:
    lines = schema_text.splitlines()
    blocks: dict[str, str] = {}
    capturing = False
    current = None
    buf: list[str] = []

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


def pg_type_to_mysql(line: str) -> str:
    line = re.sub(r"\binteger\b", "INT", line, flags=re.IGNORECASE)
    line = re.sub(r"\bbigint\b", "BIGINT", line, flags=re.IGNORECASE)
    line = re.sub(r"\bsmallint\b", "SMALLINT", line, flags=re.IGNORECASE)
    line = re.sub(r"\bserial\b", "INT", line, flags=re.IGNORECASE)
    line = re.sub(r"\bbigserial\b", "BIGINT", line, flags=re.IGNORECASE)
    line = re.sub(r"\bdouble precision\b", "DOUBLE", line, flags=re.IGNORECASE)
    line = re.sub(r"\breal\b", "FLOAT", line, flags=re.IGNORECASE)
    line = re.sub(r"\bcharacter varying\s*\((\d+)\)", r"VARCHAR(\1)", line, flags=re.IGNORECASE)
    line = re.sub(r"\bcharacter varying\b", "TEXT", line, flags=re.IGNORECASE)
    line = re.sub(r"\bcharacter\s*\((\d+)\)", r"CHAR(\1)", line, flags=re.IGNORECASE)
    line = re.sub(r"\bboolean\b", "BOOLEAN", line, flags=re.IGNORECASE)
    line = re.sub(r"\btext\b", "TEXT", line, flags=re.IGNORECASE)
    line = re.sub(r"\btimestamp without time zone\b", "DATETIME", line, flags=re.IGNORECASE)
    line = re.sub(r"\btimestamp with time zone\b", "DATETIME", line, flags=re.IGNORECASE)
    line = re.sub(r"\bbytea\b", "BLOB", line, flags=re.IGNORECASE)
    return line


def transform_block(pg_block: str) -> tuple[str, list[str]]:
    cols: list[str] = []
    out_lines: list[str] = []

    for raw in pg_block.splitlines():
        s = raw.strip()
        low = s.lower()

        if low.startswith("create table "):
            table = re.match(r"^\s*create\s+table\s+([A-Za-z_][A-Za-z0-9_]*)", raw, re.IGNORECASE).group(1)
            out_lines.append(f"CREATE TABLE `{table}` (")
            continue

        if s == "(":
            continue

        if s == ");":
            # 去掉最后一个列定义后多余的逗号
            if out_lines and out_lines[-1].rstrip().endswith(","):
                out_lines[-1] = out_lines[-1].rstrip().rstrip(",")
            out_lines.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
            continue

        if not s:
            continue

        # 保留主键，丢掉其他约束/引用
        if low.startswith("constraint") and "primary key" not in low:
            continue
        if "references" in low and "primary key" not in low:
            continue
        if low.startswith("foreign key"):
            continue
        if low.startswith("unique ") and "primary key" not in low:
            continue

        # 列定义
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+", raw)
        if m and not low.startswith("primary key"):
            col = m.group(1)
            cols.append(col)

        line = pg_type_to_mysql(raw.rstrip())
        out_lines.append(line)

    return "\n".join(out_lines), cols


def build_mysql_ddl() -> dict[str, list[str]]:
    text = SCHEMA_SQL.read_text(encoding="utf-8", errors="ignore")
    blocks = extract_create_blocks(text)

    missing = set(TARGETS) - set(blocks)
    if missing:
        raise SystemExit(f"Missing CREATE TABLE blocks for: {sorted(missing)}")

    DDL_OUT.parent.mkdir(parents=True, exist_ok=True)

    table_cols: dict[str, list[str]] = {}
    rendered: list[str] = []

    for table in TARGETS:
        ddl, cols = transform_block(blocks[table])
        table_cols[table] = cols
        rendered.append(ddl)
        rendered.append("")

    DDL_OUT.write_text("\n".join(rendered), encoding="utf-8")
    print(f"[OK] wrote {DDL_OUT}")
    return table_cols


def create_tables() -> None:
    ddl_text = DDL_OUT.read_text(encoding="utf-8")
    drop_sql = "\n".join([f"DROP TABLE IF EXISTS `{t}`;" for t in reversed(TARGETS)])
    mysql_run_sql("SET FOREIGN_KEY_CHECKS=0;\n" + drop_sql + "\nSET FOREIGN_KEY_CHECKS=1;\n")
    mysql_run_sql(ddl_text)
    print("[OK] created MySQL tables")


def load_table(table: str, cols: list[str]) -> None:
    csv_path = (CSV_DIR / f"{table}.csv").resolve()
    if not csv_path.exists():
        raise SystemExit(f"CSV file not found: {csv_path}")

    vars_ = [f"@v{i}" for i in range(1, len(cols) + 1)]
    assignments = ", ".join([f"`{c}` = NULLIF({v}, '')" for c, v in zip(cols, vars_)])
    column_vars = ", ".join(vars_)

    sql = f"""
LOAD DATA LOCAL INFILE '{str(csv_path)}'
INTO TABLE `{table}`
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '\\\\'
LINES TERMINATED BY '\\n'
({column_vars})
SET {assignments};
"""
    mysql_run_sql(sql)
    print(f"[OK] loaded {table} from {csv_path}")


def row_count(table: str) -> int:
    out = mysql_run_sql(f"SELECT COUNT(*) FROM `{table}`;\n", capture=True).strip()
    return int(out)


def main() -> int:
    print("=== prepare_mysql_perf_0003.py ===")
    print(f"MYSQL_HOST={MYSQL_HOST}")
    print(f"MYSQL_PORT={MYSQL_PORT}")
    print(f"MYSQL_DATABASE={MYSQL_DATABASE}")
    print(f"MYSQL_USER={MYSQL_USER}")
    print(f"SCHEMA_SQL={SCHEMA_SQL}")
    print(f"CSV_DIR={CSV_DIR}")

    expected = json.loads(PROFILE_JSON.read_text(encoding="utf-8"))["row_counts"]

    table_cols = build_mysql_ddl()
    create_tables()

    for table in TARGETS:
        load_table(table, table_cols[table])

    print("\n=== row counts after load ===")
    for table in TARGETS:
        actual = row_count(table)
        exp = expected.get(table)
        status = "OK" if exp == actual else "MISMATCH"
        print(f"{table}\tactual={actual}\texpected={exp}\t{status}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
