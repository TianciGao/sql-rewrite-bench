from pathlib import Path
import re

src = Path("cases/PERF/PERF_0002/schema/ddl_pg.sql")
out = Path("cases/PERF/PERF_0002/schema/ddl_spark.sql")

text = src.read_text(encoding="utf-8")
blocks = [b for b in text.split("\n\n") if b.strip()]
out_blocks = []

for block in blocks:
    lines = block.splitlines()
    new_lines = []

    for line in lines:
        stripped = line.strip().lower()

        if stripped.startswith("primary key"):
            continue

        line = re.sub(r'\binteger\b', 'INT', line, flags=re.IGNORECASE)
        line = re.sub(r'\bchar\s*\(\s*\d+\s*\)', 'STRING', line, flags=re.IGNORECASE)
        line = re.sub(r'\bvarchar\s*\(\s*\d+\s*\)', 'STRING', line, flags=re.IGNORECASE)
        line = re.sub(r'\bnot null\b', '', line, flags=re.IGNORECASE)
        line = re.sub(r'\s+,', ',', line)
        new_lines.append(line.rstrip())

    # 去掉 ");" 前一行多余的逗号
    for i in range(len(new_lines) - 1):
        if new_lines[i + 1].strip() == ');' and new_lines[i].rstrip().endswith(','):
            new_lines[i] = new_lines[i].rstrip().rstrip(',')

    out_blocks.append("\n".join(new_lines))

out.write_text("\n\n".join(out_blocks) + "\n", encoding="utf-8")
print("wrote", out)
