"""SQLite : identité des contenus, emplacements, balayages et métadonnées brutes."""
# SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
# SPDX-License-Identifier: GPL-3.0-only
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MIGRATIONS = Path(__file__).resolve().parent / "migrations"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(path: Path) -> sqlite3.Connection:
    """Ouvre une base *hors sources*, et exécute les migrations transactionnelles."""
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=5000")
    # journal DELETE pour que la base pilote reste simple à copier hors scan.
    db.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)")
    migrations = sorted(MIGRATIONS.glob("[0-9][0-9][0-9][0-9]_*.sql"))
    if not migrations:
        db.close()
        raise RuntimeError("Migrations SQL introuvables dans le paquet GNU APMG")
    latest = max(int(m.name.split("_", 1)[0]) for m in migrations)
    recorded = [r[0] for r in db.execute("SELECT version FROM schema_migrations")]
    if any(v > latest for v in recorded):
        db.close()
        raise RuntimeError("Base SQLite créée par une version plus récente du logiciel")
    for sql_file in migrations:
        version = int(sql_file.name.split("_", 1)[0])
        if db.execute("SELECT 1 FROM schema_migrations WHERE version=?", (version,)).fetchone():
            continue
        try:
            # La transaction et le commit se trouvent explicitement dans le script.
            # Un échec ne doit jamais enregistrer une migration comme appliquée.
            script = "BEGIN IMMEDIATE;\n" + sql_file.read_text(encoding="utf-8")
            script += f"\nINSERT INTO schema_migrations(version,applied_at) VALUES ({version},'{now_utc()}');\nCOMMIT;"
            db.executescript(script)
        except Exception:
            db.rollback()
            db.close()
            raise
    return db


def start_scan(db: sqlite3.Connection, scan_id: str, root: Path, exif_mode: str, version: str | None) -> None:
    with db:
        db.execute(
            "INSERT INTO scans(scan_id,root_local,started_at,status,exif_mode,exiftool_version) VALUES(?,?,?,?,?,?)",
            (scan_id, str(root), now_utc(), "running", exif_mode, version),
        )


def save_item(
    db: sqlite3.Connection,
    *,
    scan_id: str,
    path: Path,
    sha256: str | None,
    size: int | None,
    mtime_ns: int | None,
    metadata: dict[str, Any] | None,
    exiftool_version: str | None,
    status: str,
    error_code: str | None = None,
    error_detail: str | None = None,
) -> None:
    """Un fichier = une transaction ; reprise sûre en relançant le scan."""
    now = now_utc()
    with db:
        if sha256 is not None:
            assert size is not None and mtime_ns is not None
            db.execute("INSERT OR IGNORE INTO assets VALUES(?,?,?)", (sha256, size, now))
            db.execute(
                """INSERT INTO file_locations(path_local,asset_sha256,mtime_ns,size_bytes,first_seen,last_seen)
                   VALUES(?,?,?,?,?,?)
                   ON CONFLICT(path_local) DO UPDATE SET
                     asset_sha256=excluded.asset_sha256,
                     mtime_ns=excluded.mtime_ns,
                     size_bytes=excluded.size_bytes,
                     last_seen=excluded.last_seen""",
                (str(path), sha256, mtime_ns, size, now, now),
            )
            if metadata is not None and exiftool_version is not None:
                for tag, value in metadata.items():
                    db.execute(
                        """INSERT INTO source_metadata(asset_sha256,tag,value_json,exiftool_version,captured_at)
                           VALUES(?,?,?,?,?)
                           ON CONFLICT(asset_sha256,tag) DO UPDATE SET
                              value_json=excluded.value_json,
                              exiftool_version=excluded.exiftool_version,
                              captured_at=excluded.captured_at""",
                        (sha256, tag, json.dumps(value, ensure_ascii=False, separators=(",", ":")), exiftool_version, now),
                    )
        db.execute(
            """INSERT INTO scan_items(scan_id,path_local,asset_sha256,status,error_code,error_detail)
               VALUES(?,?,?,?,?,?)""",
            (scan_id, str(path), sha256, status, error_code, error_detail),
        )


def finish_scan(db: sqlite3.Connection, scan_id: str, discovered: int, indexed: int, errors: int) -> None:
    status = "partial" if errors else "completed"
    with db:
        db.execute(
            "UPDATE scans SET finished_at=?, status=?, discovered_count=?, indexed_count=?, error_count=? WHERE scan_id=?",
            (now_utc(), status, discovered, indexed, errors, scan_id),
        )


def summary(db: sqlite3.Connection) -> dict[str, int]:
    def count(sql: str) -> int:
        return int(db.execute(sql).fetchone()[0])

    return {
        "unique_assets": count("SELECT count(*) FROM assets"),
        "known_paths": count("SELECT count(*) FROM file_locations"),
        "exact_duplicate_groups": count("SELECT count(*) FROM (SELECT asset_sha256 FROM file_locations GROUP BY asset_sha256 HAVING count(*) > 1)"),
        "scans": count("SELECT count(*) FROM scans"),
        "completed_scans": count("SELECT count(*) FROM scans WHERE status='completed'"),
        "partial_scans": count("SELECT count(*) FROM scans WHERE status='partial'"),
        "metadata_tags": count("SELECT count(*) FROM source_metadata"),
    }
