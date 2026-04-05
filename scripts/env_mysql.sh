#!/usr/bin/env bash
set -euo pipefail

export MYSQL_HOST="${MYSQL_HOST:-127.0.0.1}"
export MYSQL_PORT="${MYSQL_PORT:-3306}"
export MYSQL_DATABASE="${MYSQL_DATABASE:-bench}"
export MYSQL_USER="${MYSQL_USER:-bench}"
export MYSQL_PASSWORD="${MYSQL_PASSWORD:-benchpass}"

echo "MySQL env loaded:"
echo "  MYSQL_HOST=$MYSQL_HOST"
echo "  MYSQL_PORT=$MYSQL_PORT"
echo "  MYSQL_DATABASE=$MYSQL_DATABASE"
echo "  MYSQL_USER=$MYSQL_USER"
