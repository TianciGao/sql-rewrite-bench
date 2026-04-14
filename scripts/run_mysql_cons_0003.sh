#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mkdir -p runs/cons_0003/mysql

echo "=== MySQL :: CONS_0003 :: source ==="
mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  < cases/CONS/CONS_0003/source.sql | sort | tee runs/cons_0003/mysql/source.tsv

echo
echo "=== MySQL :: CONS_0003 :: rewrite_pos_01 ==="
mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  < cases/CONS/CONS_0003/rewrite_pos_01.sql | sort | tee runs/cons_0003/mysql/rewrite_pos_01.tsv

echo
echo "=== MySQL :: CONS_0003 :: rewrite_neg_01 ==="
mysql -N -B -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  < cases/CONS/CONS_0003/rewrite_neg_01.sql | sort | tee runs/cons_0003/mysql/rewrite_neg_01.tsv
