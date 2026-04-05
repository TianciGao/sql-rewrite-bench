#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"
mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1;"
