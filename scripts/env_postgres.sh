#!/usr/bin/env bash
set -euo pipefail

export PGHOST="${PGHOST:-$("$PWD"/scripts/detect_windows_host_ip.sh)}"
export PGPORT="${PGPORT:-5432}"
export PGDATABASE="${PGDATABASE:-postgres}"
export PGUSER="${PGUSER:-postgres}"

if [ -z "${PGPASSWORD:-}" ]; then
  echo "PGPASSWORD is not set. Please export it before sourcing this script." >&2
  return 1 2>/dev/null || exit 1
fi

echo "PostgreSQL env loaded:"
echo "  PGHOST=$PGHOST"
echo "  PGPORT=$PGPORT"
echo "  PGDATABASE=$PGDATABASE"
echo "  PGUSER=$PGUSER"
