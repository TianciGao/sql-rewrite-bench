from pathlib import Path

def read_text(path_str: str) -> str:
    return Path(path_str).read_text(encoding="utf-8").strip()

engines = {
    "pg": "runs/perf_0002/pg",
    "mysql": "runs/perf_0002/mysql",
    "spark": "runs/perf_0002/spark",
}

print("=== PERF_0002 :: rewrite consistency check ===")
for engine, base in engines.items():
    source = read_text(f"{base}/source.tsv")
    pos = read_text(f"{base}/rewrite_pos_01.tsv")
    neg = read_text(f"{base}/rewrite_neg_01.tsv")
    print(f"[{engine}] source == rewrite_pos_01:", source == pos)
    print(f"[{engine}] source == rewrite_neg_01:", source == neg)
    print()
