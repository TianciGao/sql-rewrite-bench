#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mkdir -p runs/perf_0002/mysql

echo "=== MySQL :: PERF_0002 :: source ==="
mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  < cases/PERF/PERF_0002/source.sql | tee runs/perf_0002/mysql/source.tsv

echo
echo "=== MySQL :: PERF_0002 :: rewrite_pos_01 ==="
mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  < cases/PERF/PERF_0002/rewrite_pos_01.sql | tee runs/perf_0002/mysql/rewrite_pos_01.tsv

echo
echo "=== MySQL :: PERF_0002 :: rewrite_neg_01 ==="
mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  < cases/PERF/PERF_0002/rewrite_neg_01.sql | tee runs/perf_0002/mysql/rewrite_neg_01.tsv
