"""Découverte récursive, hachage en flux et orchestration lecture seule."""
# SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
# SPDX-License-Identifier: GPL-3.0-only
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import stat
import uuid
from pathlib import Path
from typing import Iterator

from .exiftool import ExifToolError, ExifToolReader
from .storage import connect, finish_scan, save_item, start_scan, now_utc

IMAGE_EXTENSIONS = frozenset({
    ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".heif", ".webp",
    ".bmp", ".gif", ".dng", ".nef", ".cr2", ".cr3", ".arw", ".raf", ".orf", ".rw2",
})


class ChangedDuringReadError(OSError):
    """Le fichier source a changé pendant son analyse."""


def _snapshot(path: Path) -> os.stat_result:
    info = path.stat(follow_symlinks=False)
    if not stat.S_ISREG(info.st_mode):
        raise OSError("Le chemin n'est pas un fichier ordinaire")
    return info


def _same_snapshot(a: os.stat_result, b: os.stat_result) -> bool:
    return (a.st_size, a.st_mtime_ns, a.st_ino, a.st_dev) == (b.st_size, b.st_mtime_ns, b.st_ino, b.st_dev)


def hash_file(path: Path) -> tuple[str, os.stat_result]:
    before = _snapshot(path)
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        opened = os.fstat(handle.fileno())
        if not _same_snapshot(before, opened):
            raise ChangedDuringReadError("Fichier changé entre la découverte et l'ouverture")
        while block := handle.read(1024 * 1024):
            digest.update(block)
        consumed = os.fstat(handle.fileno())
    after = _snapshot(path)
    if not _same_snapshot(before, consumed) or not _same_snapshot(before, after):
        raise ChangedDuringReadError("Fichier modifié durant le calcul SHA-256")
    return digest.hexdigest(), after


def discover(root: Path) -> Iterator[tuple[Path, str | None]]:
    """Émet les fichiers candidats et les erreurs de traversée sans suivre les liens."""
    def on_error(err: OSError) -> None:
        failures.append((Path(err.filename or str(root)), "Répertoire inaccessible"))

    failures: list[tuple[Path, str]] = []
    for directory, dirs, files in os.walk(root, topdown=True, followlinks=False, onerror=on_error):
        here = Path(directory)
        dirs[:] = [d for d in sorted(dirs) if not (here / d).is_symlink() and not getattr(here / d, "is_junction", lambda: False)()]
        for name in sorted(files):
            path = here / name
            if path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            if path.is_symlink():
                yield path, "Lien symbolique ignoré"
            else:
                yield path, None
    for path, message in failures:
        yield path, message


def _ensure_output_outside(root: Path, output: Path, label: str) -> Path:
    resolved = output.expanduser().resolve(strict=False)
    if resolved == root or root in resolved.parents:
        raise ValueError(f"{label} doit être hors du répertoire photographique source")
    # Interdire de placer une base contenant des chemins/GPS personnels dans un dépôt Git.
    for parent in (resolved.parent, *resolved.parents):
        if (parent / ".git").exists():
            raise ValueError(f"{label} ne peut pas être placé dans un dépôt Git")
    return resolved


def scan(
    *, root: Path, db_path: Path, exiftool: str = "exiftool", no_exif: bool = False,
    jsonl_path: Path | None = None,
) -> dict[str, object]:
    root = root.expanduser()
    if root.is_symlink() or getattr(root, "is_junction", lambda: False)():
        raise ValueError("La racine source ne doit pas être un lien symbolique ou une jonction")
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("La source doit être un répertoire ordinaire")
    db_path = _ensure_output_outside(root, db_path, "La base SQLite")
    if db_path.exists() and db_path.stat().st_nlink > 1:
        raise ValueError("La base SQLite ne doit pas avoir de liens physiques")
    if jsonl_path is not None:
        jsonl_path = _ensure_output_outside(root, jsonl_path, "Le manifeste JSONL")
        reserved = [db_path, *(db_path.with_name(db_path.name + suffix) for suffix in ("-journal", "-wal", "-shm"))]
        if any(jsonl_path == path or (jsonl_path.exists() and path.exists() and jsonl_path.samefile(path)) for path in reserved):
            raise ValueError("Le manifeste ne peut pas remplacer la base SQLite ou ses journaux")

    reader = None if no_exif else ExifToolReader(exiftool)
    db = connect(db_path)
    scan_id = str(uuid.uuid4())
    discovered = indexed = errors = 0
    start_scan(db, scan_id, root, "skipped_explicitly" if no_exif else "exiftool", reader.version if reader else None)
    try:
        for path, discovery_error in discover(root):
            discovered += 1
            sha = None
            size = mtime_ns = None
            metadata = None
            error_code = error_detail = None
            status = "indexed"
            if discovery_error:
                status = "failed"
                error_code = "discovery_error"
                error_detail = discovery_error
            else:
                try:
                    sha, info = hash_file(path)
                    size, mtime_ns = info.st_size, info.st_mtime_ns
                    if reader is not None:
                        try:
                            metadata = reader.read(path)
                            if not _same_snapshot(info, _snapshot(path)):
                                raise ChangedDuringReadError("Fichier modifié durant l'extraction EXIF")
                        except ChangedDuringReadError:
                            raise
                        except ExifToolError as exc:
                            status = "metadata_failed"
                            error_code, error_detail = "exiftool_error", str(exc)
                except ChangedDuringReadError as exc:
                    # Ne pas conserver un SHA-256 potentiellement périmé.
                    sha = size = mtime_ns = None
                    status, error_code, error_detail = "failed", "changed_during_read", str(exc)
                except (OSError, ValueError) as exc:
                    status, error_code, error_detail = "failed", "unreadable", type(exc).__name__
            save_item(db, scan_id=scan_id, path=path, sha256=sha, size=size, mtime_ns=mtime_ns,
                      metadata=metadata, exiftool_version=reader.version if reader else None,
                      status=status, error_code=error_code, error_detail=error_detail)
            if status != "indexed":
                errors += 1
            else:
                indexed += 1
        finish_scan(db, scan_id, discovered, indexed, errors)
        if jsonl_path is not None:
            _export_manifest(db, scan_id, jsonl_path)
    except BaseException:
        with db:
            db.execute("UPDATE scans SET status='interrupted', finished_at=? WHERE scan_id=?", ( now_utc(), scan_id))
        raise
    finally:
        db.close()
    return {"scan_id": scan_id, "discovered": discovered, "indexed": indexed, "errors": errors, "status": "partial" if errors else "completed", "exif_mode": "skipped_explicitly" if no_exif else "exiftool"}


def _export_manifest(db: sqlite3.Connection, scan_id: str, destination: Path) -> None:
    """Export privé atomique, jamais dans Git ni dans l'arbre source."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp = destination.with_name(destination.name + f".{uuid.uuid4().hex}.tmp")
    try:
        with tmp.open("w", encoding="utf-8", newline="\n") as out:
            for record in db.execute(
                "SELECT path_local,asset_sha256,status,error_code,error_detail FROM scan_items WHERE scan_id=? ORDER BY path_local", (scan_id,)
            ):
                out.write(json.dumps(dict(record), ensure_ascii=False) + "\n")
        tmp.replace(destination)
    finally:
        tmp.unlink(missing_ok=True)
