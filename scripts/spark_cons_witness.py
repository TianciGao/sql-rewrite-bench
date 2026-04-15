from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
from pyspark.sql import SparkSession

ROOT = Path(__file__).resolve().parents[1]

CASE_CONFIG: Dict[str, Dict] = {
    "CONS_0003": {
        "tables": {
            "EMP": {
                "schema": ["DEPTNO", "SLACKER"],
                "rows": [
                    (10, 1),
                    (10, 1),
                    (10, 2),
                    (20, 3),
                    (20, 3),
                ],
            },
            "DEPT": {
                "schema": ["DEPTNO"],
                "rows": [
                    (10,),
                    (20,),
                ],
            },
        },
        "expected": {
            "source": "10\t2\n20\t1",
            "rewrite_pos_01": "10\t2\n20\t1",
            "rewrite_neg_01": "10\t3\n20\t2",
        },
    },
    "CONS_0004": {
        "tables": {
            "EMP": {
                "schema": "EMPNO INT, MGR INT, JOB STRING",
                "rows": [
                    (1, None, "Clerk"),
                    (2, None, "Clerk"),
                    (3, None, "Clerk"),
                    (4, None, "Clerk"),
                    (5, None, "Analyst"),
                    (6, 100, "Clerk"),
                ],
            },
        },
        "expected": {
            "source": "Clerk",
            "rewrite_pos_01": "Clerk",
            "rewrite_neg_01": "",
        },
    },
}


def ensure_case_id(case_id: str) -> str:
    if case_id not in CASE_CONFIG:
        raise ValueError(f"Unsupported case_id: {case_id}")
    return case_id


def make_spark(app_name: str) -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def register_tables(spark: SparkSession, case_id: str) -> None:
    case_id = ensure_case_id(case_id)
    for table_name, spec in CASE_CONFIG[case_id]["tables"].items():
        df = spark.createDataFrame(spec["rows"], spec["schema"])
        df.createOrReplaceTempView(table_name)


def case_dir(case_id: str) -> Path:
    ensure_case_id(case_id)
    return ROOT / "cases" / "CONS" / case_id


def sql_text(case_id: str, variant: str) -> str:
    path = case_dir(case_id) / f"{variant}.sql"
    return path.read_text(encoding="utf-8")


def run_variant(spark: SparkSession, case_id: str, variant: str) -> List[Tuple[str, ...]]:
    query = sql_text(case_id, variant)
    rows = spark.sql(query).collect()
    normalized = [
        tuple("" if value is None else str(value) for value in row)
        for row in rows
    ]
    normalized.sort()
    return normalized


def rows_to_text(rows: List[Tuple[str, ...]]) -> str:
    return "\n".join("\t".join(row) for row in rows)


def write_variant_output(case_id: str, variant: str, rows: List[Tuple[str, ...]]) -> Path:
    out_dir = ROOT / "runs" / case_id.lower() / "spark"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{variant}.tsv"
    out_path.write_text(rows_to_text(rows), encoding="utf-8")
    return out_path


def expected_text(case_id: str, variant: str) -> str:
    ensure_case_id(case_id)
    return CASE_CONFIG[case_id]["expected"][variant]


def plan_dir(case_id: str) -> Path:
    out_dir = ROOT / "runs" / case_id.lower() / "plans" / "spark"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir
