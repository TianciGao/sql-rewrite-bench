from pathlib import Path

base = Path("runs/cons_0002/pg")
files = {
    "source": base / "source.tsv",
    "rewrite_pos_01": base / "rewrite_pos_01.tsv",
    "rewrite_neg_01": base / "rewrite_neg_01.tsv",
}

texts = {}
for name, path in files.items():
    texts[name] = path.read_text(encoding="utf-8").strip()

print("=== CONS_0002 :: PostgreSQL consistency check ===")
for name, text in texts.items():
    print(f"{name}: {text!r}")

print()
print("source == rewrite_pos_01:", texts["source"] == texts["rewrite_pos_01"])
print("source == rewrite_neg_01:", texts["source"] == texts["rewrite_neg_01"])
