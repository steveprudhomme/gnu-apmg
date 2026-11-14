"""Tests Phase 1 sur octets synthétiques : aucune photo personnelle en dépôt."""
# SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
# SPDX-License-Identifier: GPL-3.0-only
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
from contextlib import closing
import unittest
from pathlib import Path
from unittest.mock import patch

from photosemantique.exiftool import ExifToolError, ExifToolReader
from photosemantique.inventory import ChangedDuringReadError, hash_file, scan
from photosemantique.storage import connect, summary


class Phase1Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="photo-sem-test-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / "Photos échantillon"
        self.source.mkdir()
        self.work = self.base / "state"
        self.db = self.work / "inventory.sqlite"
        (self.source / "Sous-dossier").mkdir()
        (self.source / "école_avion.JPG").write_bytes(b"fake-jpeg-a")
        (self.source / "Sous-dossier" / "same.jpg").write_bytes(b"fake-jpeg-a")
        (self.source / "Sous-dossier" / "autre.png").write_bytes(b"fake-png-b")
        (self.source / "notice.txt").write_text("not an image", encoding="utf-8")

    def test_manifest_cannot_replace_sqlite_journals(self):
        for suffix in ("", "-journal", "-wal", "-shm"):
            with self.subTest(suffix=suffix):
                with self.assertRaisesRegex(ValueError, "journaux"):
                    scan(root=self.source, db_path=self.db, no_exif=True,
                         jsonl_path=self.db.with_name(self.db.name + suffix))
        self.assertFalse(self.db.exists())

    def test_database_hardlink_cannot_modify_source(self):
        source = self.source / "école_avion.JPG"
        before = source.read_bytes()
        self.work.mkdir()
        try:
            self.db.hardlink_to(source)
        except OSError:
            self.skipTest("Liens physiques indisponibles")
        with self.assertRaisesRegex(ValueError, "liens physiques"):
            scan(root=self.source, db_path=self.db, no_exif=True)
        self.assertEqual(source.read_bytes(), before)

    def test_hash_file_streaming(self):
        path = self.source / "école_avion.JPG"
        actual, info = hash_file(path)
        self.assertEqual(actual, hashlib.sha256(b"fake-jpeg-a").hexdigest())
        self.assertEqual(info.st_size, len(b"fake-jpeg-a"))

    def test_recursive_duplicates_unicode_integrity(self):
        originals = {p.relative_to(self.source).as_posix(): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
        manifest = self.work / "scan.jsonl"
        result = scan(root=self.source, db_path=self.db, no_exif=True, jsonl_path=manifest)
        self.assertEqual((result["discovered"], result["indexed"], result["errors"]), (3, 3, 0))
        self.assertEqual(result["exif_mode"], "skipped_explicitly")
        with closing(connect(self.db)) as db:
            stats = summary(db)
            self.assertEqual(stats["unique_assets"], 2)
            self.assertEqual(stats["known_paths"], 3)
            self.assertEqual(stats["exact_duplicate_groups"], 1)
            self.assertEqual(db.execute("SELECT count(*) FROM source_metadata").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT count(*) FROM schema_migrations").fetchone()[0], 1)
        lines = [json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(lines), 3)
        self.assertTrue(any("école_avion.JPG" in line["path_local"] for line in lines))
        self.assertEqual(originals, {p.relative_to(self.source).as_posix(): p.read_bytes() for p in self.source.rglob("*") if p.is_file()})

    def test_repeated_scans_do_not_duplicate_assets_or_locations(self):
        first = scan(root=self.source, db_path=self.db, no_exif=True)
        second = scan(root=self.source, db_path=self.db, no_exif=True)
        self.assertNotEqual(first["scan_id"], second["scan_id"])
        with closing(connect(self.db)) as db:
            self.assertEqual(summary(db)["scans"], 2)
            self.assertEqual(summary(db)["unique_assets"], 2)
            self.assertEqual(summary(db)["known_paths"], 3)
            self.assertEqual(db.execute("SELECT count(*) FROM scan_items").fetchone()[0], 6)

    def test_path_replacement_updates_location_without_losing_asset_history(self):
        scan(root=self.source, db_path=self.db, no_exif=True)
        (self.source / "école_avion.JPG").write_bytes(b"different-content")
        scan(root=self.source, db_path=self.db, no_exif=True)
        with closing(connect(self.db)) as db:
            self.assertEqual(summary(db)["unique_assets"], 3)
            self.assertEqual(summary(db)["known_paths"], 3)

    def test_guard_prevents_writing_sqlite_and_manifest_inside_sources(self):
        with self.assertRaisesRegex(ValueError, "hors du répertoire"):
            scan(root=self.source, db_path=self.source / "data.sqlite", no_exif=True)
        with self.assertRaisesRegex(ValueError, "hors du répertoire"):
            scan(root=self.source, db_path=self.db, no_exif=True, jsonl_path=self.source / "scan.jsonl")
        self.assertFalse(self.db.exists())

    def test_guard_prevents_working_database_in_git_checkout(self):
        (self.base / ".git").mkdir()
        with self.assertRaisesRegex(ValueError, "dépôt Git"):
            scan(root=self.source, db_path=self.db, no_exif=True)

    def test_symlinks_are_skipped_and_cannot_cause_cycle(self):
        try:
            (self.source / "Sous-dossier" / "back").symlink_to(self.source, target_is_directory=True)
            (self.source / "link.jpg").symlink_to(self.source / "école_avion.JPG")
        except (OSError, NotImplementedError):
            self.skipTest("création des liens symboliques interdite sur cet environnement")
        result = scan(root=self.source, db_path=self.db, no_exif=True)
        self.assertEqual(result["discovered"], 4)
        self.assertEqual(result["indexed"], 3)
        self.assertEqual(result["errors"], 1)
        with closing(connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM scan_items WHERE error_code='discovery_error'").fetchone()[0], 1)

    def test_partial_failure_is_recorded_and_next_file_continues(self):
        from photosemantique.inventory import hash_file as real_hash
        def broken_on_one(path):
            if path.name == "autre.png":
                raise ChangedDuringReadError("Fichier modifié durant la lecture")
            return real_hash(path)
        with patch("photosemantique.inventory.hash_file", side_effect=broken_on_one):
            result = scan(root=self.source, db_path=self.db, no_exif=True)
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["indexed"], 2)
        self.assertEqual(result["errors"], 1)
        with closing(connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM scan_items WHERE error_code='changed_during_read'").fetchone()[0], 1)

    def test_missing_exiftool_is_a_clear_error_no_silent_skip(self):
        with patch("photosemantique.exiftool.shutil.which", return_value=None):
            with self.assertRaisesRegex(ExifToolError, "introuvable"):
                scan(root=self.source, db_path=self.db)
        self.assertFalse(self.db.exists())

    def test_exiftool_reads_grouped_tags_and_omits_sourcefile(self):
        good_json = json.dumps([{"SourceFile": "private-path", "EXIF:DateTimeOriginal": "2020:01:02 03:04:05", "GPS:GPSLatitude": "45.5", "XMP-dc:Subject": ["avion"]}])
        def mocked_run(argv, **_):
            if "-ver" in argv:
                return subprocess.CompletedProcess(argv, 0, "13.00\n", "")
            return subprocess.CompletedProcess(argv, 0, good_json, "")
        with patch("photosemantique.exiftool.shutil.which", return_value="exiftool"), patch("photosemantique.exiftool.subprocess.run", side_effect=mocked_run) as proc:
            result = scan(root=self.source, db_path=self.db)
            self.assertTrue(any("-G1:4" in c.args[0] for c in proc.call_args_list))
        self.assertEqual(result["indexed"], 3)
        with closing(connect(self.db)) as db:
            self.assertEqual(summary(db)["metadata_tags"], 3 * 2)  # 2 contenus distincts
            self.assertIsNone(db.execute("SELECT 1 FROM source_metadata WHERE tag='SourceFile'").fetchone())
            self.assertEqual(json.loads(db.execute("SELECT value_json FROM source_metadata WHERE tag='EXIF:DateTimeOriginal' LIMIT 1").fetchone()[0]), "2020:01:02 03:04:05")

    def test_exif_failure_is_separate_from_content_hash(self):
        def mocked_run(argv, **_):
            if "-ver" in argv:
                return subprocess.CompletedProcess(argv, 0, "13.00\n", "")
            return subprocess.CompletedProcess(argv, 1, "", "invalid image")
        with patch("photosemantique.exiftool.shutil.which", return_value="exiftool"), patch("photosemantique.exiftool.subprocess.run", side_effect=mocked_run):
            result = scan(root=self.source, db_path=self.db)
        self.assertEqual(result["errors"], 3)
        with closing(connect(self.db)) as db:
            self.assertEqual(summary(db)["unique_assets"], 2)
            self.assertEqual(db.execute("SELECT count(*) FROM scan_items WHERE status='metadata_failed'").fetchone()[0], 3)

    def test_interrupted_scan_is_marked_and_can_be_restarted(self):
        from photosemantique.inventory import save_item as real_save
        called = 0
        def interrupt_once(*args, **kwargs):
            nonlocal called
            called += 1
            if called == 2:
                raise KeyboardInterrupt()
            return real_save(*args, **kwargs)
        with patch("photosemantique.inventory.save_item", side_effect=interrupt_once):
            with self.assertRaises(KeyboardInterrupt):
                scan(root=self.source, db_path=self.db, no_exif=True)
        with closing(connect(self.db)) as db:
            self.assertEqual(db.execute("SELECT status FROM scans LIMIT 1").fetchone()[0], "interrupted")
            self.assertEqual(db.execute("SELECT count(*) FROM scan_items").fetchone()[0], 1)
        subsequent = scan(root=self.source, db_path=self.db, no_exif=True)
        self.assertEqual(subsequent["status"], "completed")
        with closing(connect(self.db)) as db:
            self.assertEqual(summary(db)["known_paths"], 3)
            self.assertEqual(summary(db)["scans"], 2)

    def test_source_symlink_rejected(self):
        link = self.base / "source-link"
        try:
            link.symlink_to(self.source, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("création de liens symboliques non autorisée")
        with self.assertRaisesRegex(ValueError, "racine source"):
            scan(root=link, db_path=self.db, no_exif=True)

    def test_report_is_aggregate_and_private_paths_not_shown(self):
        scan(root=self.source, db_path=self.db, no_exif=True)
        result = subprocess.run([sys.executable, "-X", "utf8", "-m", "photosemantique", "report", "--db", str(self.db)], cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"unique_assets": 2', result.stdout)
        self.assertNotIn("école_avion", result.stdout)
        self.assertNotIn(str(self.source), result.stdout)

if __name__ == "__main__":
    unittest.main()
