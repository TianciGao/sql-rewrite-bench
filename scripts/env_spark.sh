#!/usr/bin/env bash

# 这是给当前交互 shell source 的环境脚本，不要在这里用 set -euo pipefail

if [ -z "${SPARK_LOCAL_IP:-}" ]; then
  SPARK_LOCAL_IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
fi

if [ -z "${SPARK_DRIVER_MEMORY:-}" ]; then
  SPARK_DRIVER_MEMORY="8g"
fi

export SPARK_LOCAL_IP
export SPARK_DRIVER_MEMORY

echo "Spark env loaded:"
echo "  SPARK_LOCAL_IP=$SPARK_LOCAL_IP"
echo "  SPARK_DRIVER_MEMORY=$SPARK_DRIVER_MEMORY"
