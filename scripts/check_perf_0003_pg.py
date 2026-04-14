from pathlib import Path

def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip()

source = read("runs/perf_0003/pg/source.tsv")
pos = read("runs/perf_0003/pg/rewrite_pos_01.tsv")
neg = read("runs/perf_0003/pg/rewrite_neg_01.tsv")

print("=== PERF_0003 :: PostgreSQL source/positive/negative check ===")
print("source:", repr(source))
print("rewrite_pos_01:", repr(pos))
print("rewrite_neg_01:", repr(neg))
print()
print("source == rewrite_pos_01:", source == pos)
print("source == rewrite_neg_01:", source == neg)
