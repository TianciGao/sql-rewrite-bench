#!/usr/bin/env bash

# 这是给当前交互 shell source 的环境脚本，不要在这里用 set -euo pipefail

if [ -z "${PGHOST:-}" ]; then
  PGHOST="$(./scripts/detect_windows_host_ip.sh 2>/dev/null)"
fi

if [ -z "${PGPORT:-}" ]; then
  PGPORT="5432"
fi

if [ -z "${PGDATABASE:-}" ]; then
  PGDATABASE="postgres"
fi

if [ -z "${PGUSER:-}" ]; then
  PGUSER="postgres"
fi

export PGHOST
export PGPORT
export PGDATABASE
export PGUSER

if [ -z "${PGPASSWORD:-}" ]; then
  echo "PGPASSWORD is not set. Please export it in this shell before using PostgreSQL commands."
else
  echo "PostgreSQL env loaded:"
  echo "  PGHOST=$PGHOST"
  echo "  PGPORT=$PGPORT"
  echo "  PGDATABASE=$PGDATABASE"
  echo "  PGUSER=$PGUSER"
fi
