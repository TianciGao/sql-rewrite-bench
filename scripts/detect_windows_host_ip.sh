#!/usr/bin/env bash
set -euo pipefail
ip route | awk '/^default/ {print $3; exit}'
