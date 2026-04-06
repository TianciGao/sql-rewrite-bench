from pathlib import Path

root = Path("runs/longtail_case")
systems = ["pg", "mysql", "spark"]
variants = ["source", "rewrite_pos_01", "rewrite_neg_01"]

for system in systems:
    print(f"=== {system} ===")
    data = {}
    for variant in variants:
        path = root / system / f"{variant}.tsv"
        text = path.read_text(encoding="utf-8").strip()
        data[variant] = text
        print(f"{variant}: {repr(text)}")
    print("source == rewrite_pos_01:", data["source"] == data["rewrite_pos_01"])
    print("source == rewrite_neg_01:", data["source"] == data["rewrite_neg_01"])
    print()
