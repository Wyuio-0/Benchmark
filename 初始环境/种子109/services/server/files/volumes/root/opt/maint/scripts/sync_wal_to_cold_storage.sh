#!/usr/bin/env bash
set -euo pipefail
pg_archivecleanup -d /var/lib/postgresql/wal_archive
rclone sync /var/lib/postgresql/wal_archive cold_dr:prod-pg-wal/
