from pathlib import Path
import re

src = Path("cases/PORT/PORT_0002/schema/ddl_pg.sql")
out = Path("cases/PORT/PORT_0002/schema/ddl_spark.sql")

text = src.read_text(encoding="utf-8")
lines = text.splitlines()
new_lines = []

for line in lines:
    stripped = line.strip().lower()

    if stripped.startswith("primary key"):
        continue

    line = re.sub(r'\binteger\b', 'INT', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbigint\b', 'BIGINT', line, flags=re.IGNORECASE)
    line = re.sub(r'\bdouble precision\b', 'DOUBLE', line, flags=re.IGNORECASE)
    line = re.sub(r'\bchar\s*\(\s*\d+\s*\)', 'STRING', line, flags=re.IGNORECASE)
    line = re.sub(r'\bvarchar\s*\(\s*\d+\s*\)', 'STRING', line, flags=re.IGNORECASE)
    line = re.sub(r'\btimestamp with time zone\b', 'TIMESTAMP', line, flags=re.IGNORECASE)
    line = re.sub(r'\btimestamp without time zone\b', 'TIMESTAMP', line, flags=re.IGNORECASE)
    line = re.sub(r'\bnot null\b', '', line, flags=re.IGNORECASE)
    line = re.sub(r'\s+,', ',', line)
    new_lines.append(line.rstrip())

for i in range(len(new_lines) - 1):
    if new_lines[i + 1].strip() == ');' and new_lines[i].rstrip().endswith(','):
        new_lines[i] = new_lines[i].rstrip().rstrip(',')

out.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
print("wrote", out)
