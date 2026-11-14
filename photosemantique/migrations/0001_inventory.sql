-- PhotoSémantique : schéma d'inventaire initial, sans données biométriques.
-- SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
-- SPDX-License-Identifier: GPL-3.0-only
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS assets (
    sha256 TEXT PRIMARY KEY CHECK(length(sha256) = 64),
    size_bytes INTEGER NOT NULL CHECK(size_bytes >= 0),
    first_seen TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS file_locations (
    path_local TEXT PRIMARY KEY,
    asset_sha256 TEXT NOT NULL REFERENCES assets(sha256),
    mtime_ns INTEGER NOT NULL,
    size_bytes INTEGER NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_file_locations_asset ON file_locations(asset_sha256);
CREATE TABLE IF NOT EXISTS scans (
    scan_id TEXT PRIMARY KEY,
    root_local TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL CHECK(status IN ('running','completed','partial','interrupted')),
    exif_mode TEXT NOT NULL,
    exiftool_version TEXT,
    discovered_count INTEGER NOT NULL DEFAULT 0,
    indexed_count INTEGER NOT NULL DEFAULT 0,
    error_count INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS scan_items (
    scan_id TEXT NOT NULL REFERENCES scans(scan_id),
    path_local TEXT NOT NULL,
    asset_sha256 TEXT REFERENCES assets(sha256),
    status TEXT NOT NULL CHECK(status IN ('indexed','metadata_failed','failed')),
    error_code TEXT,
    error_detail TEXT,
    PRIMARY KEY (scan_id, path_local)
);
CREATE INDEX IF NOT EXISTS idx_scan_items_asset ON scan_items(asset_sha256);
CREATE TABLE IF NOT EXISTS source_metadata (
    asset_sha256 TEXT NOT NULL REFERENCES assets(sha256),
    tag TEXT NOT NULL,
    value_json TEXT NOT NULL,
    exiftool_version TEXT NOT NULL,
    captured_at TEXT NOT NULL,
    PRIMARY KEY (asset_sha256, tag)
);
