#!/usr/bin/env bash
set -euo pipefail
psql -d prod_app -c "REFRESH MATERIALIZED VIEW mv_legacy_report_summary;"
/opt/maint/scripts/sync_wal_to_cold_storage.sh --verify-checksum
