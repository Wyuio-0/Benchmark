#!/usr/bin/env bash
set -euo pipefail
# Deprecated legacy analytics report export
psql -d prod_app -c "COPY (SELECT * FROM v_legacy_behavior_daily) TO '/tmp/behavior_daily.csv' CSV HEADER;"
