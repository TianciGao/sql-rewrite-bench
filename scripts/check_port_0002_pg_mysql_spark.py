from decimal import Decimal
from pathlib import Path

def read_scalar(path_str: str) -> Decimal:
    text = Path(path_str).read_text(encoding="utf-8").strip()
    first = text.splitlines()[0].split("\t")[0].strip()
    return Decimal(first)

pg_source = read_scalar("runs/port_0002/pg/source.tsv")
mysql_pos = read_scalar("runs/port_0002/mysql/rewrite_pos_01.tsv")
mysql_neg = read_scalar("runs/port_0002/mysql/rewrite_neg_01.tsv")
spark_pos = read_scalar("runs/port_0002/spark/rewrite_pos_02_spark.tsv")
spark_neg = read_scalar("runs/port_0002/spark/rewrite_neg_02_spark.tsv")

print("=== PORT_0002 :: PG/MySQL/Spark portability check ===")
print("pg_source:", pg_source)
print("mysql_pos:", mysql_pos)
print("mysql_neg:", mysql_neg)
print("spark_pos:", spark_pos)
print("spark_neg:", spark_neg)
print()
print("pg_source == mysql_pos:", pg_source == mysql_pos)
print("pg_source == mysql_neg:", pg_source == mysql_neg)
print("pg_source == spark_pos:", pg_source == spark_pos)
print("pg_source == spark_neg:", pg_source == spark_neg)
