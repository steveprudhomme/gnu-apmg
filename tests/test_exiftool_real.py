"""Opt-in integration against a real, separately installed ExifTool."""
# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
from __future__ import annotations

from contextlib import closing
import hashlib
import os
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
import zlib

from photosemantique.inventory import scan
from photosemantique.storage import connect, summary


def synthetic_png() -> bytes:
    """Build a valid 1x1 RGB PNG with known UTF-8 documentary fields."""
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (struct.pack('>I', len(payload)) + kind + payload
                + struct.pack('>I', zlib.crc32(kind + payload) & 0xffffffff))

    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
            + chunk(b'tEXt', b'Title\0GNU APMG synthetic')
            + chunk(b'iTXt', b'Description\0\0\0\0\0' + 'École — essai synthétique'.encode('utf-8'))
            + chunk(b'IDAT', zlib.compress(b'\x00\x30\x80\xc0'))
            + chunk(b'IEND', b''))


EXIFTOOL = os.environ.get('GNU_APMG_EXIFTOOL') or shutil.which('exiftool')


@unittest.skipUnless(EXIFTOOL, 'Real ExifTool unavailable; set GNU_APMG_EXIFTOOL')
class RealExifToolTests(unittest.TestCase):
    def test_unicode_metadata_duplicates_corruption_and_integrity(self):
        with tempfile.TemporaryDirectory(prefix='gnu-apmg-exif-') as tmp:
            base = Path(tmp)
            source = base / 'Échantillon synthétique'
            source.mkdir()
            (source / 'école.png').write_bytes(synthetic_png())
            (source / 'copie.png').write_bytes(synthetic_png())
            (source / 'autre.png').write_bytes(synthetic_png())
            (source / 'corrompu.jpg').write_bytes(b'\xff\xd8\xff\xe1\x00\x20truncated')

            def fingerprints():
                return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in source.iterdir()}

            before = fingerprints()
            db_path = base / 'state' / 'inventory.sqlite'
            for _ in range(2):
                result = scan(root=source, db_path=db_path, exiftool=str(EXIFTOOL))
                self.assertEqual(result['exif_mode'], 'exiftool')
                self.assertEqual((result['discovered'], result['indexed'], result['errors']), (4, 3, 1))
                self.assertEqual(result['status'], 'partial')
            with closing(connect(db_path)) as db:
                stats = summary(db)
                self.assertEqual(stats['known_paths'], 4)
                self.assertEqual(stats['unique_assets'], 2)
                self.assertEqual(stats['exact_duplicate_groups'], 1)
                self.assertEqual(stats['partial_scans'], 2)
                values = [r[0] for r in db.execute('SELECT value_json FROM source_metadata')]
                self.assertIn('"GNU APMG synthetic"', values)
                self.assertIn('"École — essai synthétique"', values)
                self.assertEqual(db.execute("SELECT count(*) FROM scan_items WHERE status='metadata_failed'").fetchone()[0], 2)
                self.assertFalse(db.execute('PRAGMA foreign_key_check').fetchall())
            self.assertEqual(before, fingerprints())


if __name__ == '__main__':
    unittest.main()
