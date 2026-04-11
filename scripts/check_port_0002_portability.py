from decimal import Decimal
from pathlib import Path

pg_source = Decimal(Path("runs/port_0002/pg/source.tsv").read_text(encoding="utf-8").strip())
mysql_pos = Decimal(Path("runs/port_0002/mysql/rewrite_pos_01.tsv").read_text(encoding="utf-8").strip())
mysql_neg = Decimal(Path("runs/port_0002/mysql/rewrite_neg_01.tsv").read_text(encoding="utf-8").strip())

print("=== PORT_0002 :: portability check ===")
print("pg_source:", pg_source)
print("mysql_rewrite_pos_01:", mysql_pos)
print("mysql_rewrite_neg_01:", mysql_neg)
print()
print("pg_source == mysql_rewrite_pos_01:", pg_source == mysql_pos)
print("pg_source == mysql_rewrite_neg_01:", pg_source == mysql_neg)
