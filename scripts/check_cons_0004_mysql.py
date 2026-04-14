from pathlib import Path

def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip()

source = read_text("runs/cons_0004/mysql/source.tsv")
pos = read_text("runs/cons_0004/mysql/rewrite_pos_01.tsv")
neg = read_text("runs/cons_0004/mysql/rewrite_neg_01.tsv")

print("=== CONS_0004 :: MySQL consistency check ===")
print("source:", repr(source))
print("rewrite_pos_01:", repr(pos))
print("rewrite_neg_01:", repr(neg))
print()
print("source == rewrite_pos_01:", source == pos)
print("source == rewrite_neg_01:", source == neg)
print()
print("expected source/positive rows:")
print(repr("Clerk"))
print("expected negative rows:")
print(repr(""))
