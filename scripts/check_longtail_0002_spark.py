from pathlib import Path

def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").rstrip("\n")

base = Path("runs/longtail_0002/spark")
source = read_text(str(base / "source.tsv"))
pos = read_text(str(base / "rewrite_pos_01.tsv"))
neg = read_text(str(base / "rewrite_neg_01.tsv"))

print("=== LONGTAIL_0002 :: Spark consistency check ===")
print("source:", repr(source))
print("rewrite_pos_01:", repr(pos))
print("rewrite_neg_01:", repr(neg))
print()
print("source == rewrite_pos_01:", source == pos)
print("source == rewrite_neg_01:", source == neg)
