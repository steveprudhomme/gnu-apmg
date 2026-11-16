# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
import json
from pathlib import Path
import tempfile
import unittest

from photosemantique.digikam_lab import prepare, compare, properties

XMP = '''<x:xmpmeta xmlns:x="adobe:ns:meta/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">
<rdf:RDF><rdf:Description rdf:about=""><dc:subject><rdf:Bag><rdf:li>Arbre</rdf:li><rdf:li>Jardin</rdf:li></rdf:Bag></dc:subject><dc:title><rdf:Alt><rdf:li xml:lang="x-default">Titre fictif</rdf:li></rdf:Alt></dc:title></rdf:Description></rdf:RDF></x:xmpmeta>'''


class DigiKamLabTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.export = self.root/'export'
        (self.export/'files').mkdir(parents=True)
        self.image = self.export/'files'/'sample.heic'
        self.image.write_bytes(b'synthetic placeholder, not a decodable HEIC')
        self.sidecar = self.image.with_name('sample.heic.xmp')
        self.sidecar.write_text(XMP, encoding='utf-8')
        self.lab = self.root/'lab'

    def test_baseline_and_copy_are_independent(self):
        self.assertEqual(prepare(self.export, self.lab)['photos'], 1)
        report = compare(self.lab)
        self.assertTrue(report['all_image_bytes_unchanged'])
        self.assertTrue(report['all_prior_xmp_properties_unchanged'])
        self.assertFalse(report['any_sidecar_bytes_changed'])
        self.assertFalse(report['gui_success_inferred'])
        (self.lab/'collection'/'sample.heic').write_bytes(b'edited copy')
        report = compare(self.lab)
        self.assertFalse(report['all_image_bytes_unchanged'])
        self.assertTrue(report['all_reference_bytes_unchanged'])
        self.assertEqual(self.image.read_bytes(), b'synthetic placeholder, not a decodable HEIC')

    def test_loss_and_reference_change_detected(self):
        prepare(self.export, self.lab)
        copied = self.lab/'collection'/'sample.heic.xmp'
        copied.write_text(XMP.replace('Titre fictif', 'Titre modifié'), encoding='utf-8')
        self.image.write_bytes(b'external edit')
        report = compare(self.lab)
        self.assertFalse(report['all_reference_bytes_unchanged'])
        self.assertFalse(report['all_prior_xmp_properties_unchanged'])
        self.assertTrue(report['any_sidecar_bytes_changed'])
        self.assertEqual(len(report['results'][1]['changed_properties']), 1)

    def test_bag_order_and_prefix_do_not_matter(self):
        prepare(self.export, self.lab)
        copy = self.lab/'collection'/'sample.heic.xmp'
        copy.write_text(XMP.replace('<rdf:li>Arbre</rdf:li><rdf:li>Jardin</rdf:li>', '<rdf:li>Jardin</rdf:li><rdf:li>Arbre</rdf:li>').replace('dc:', 'd:').replace('xmlns:dc=', 'xmlns:d='), encoding='utf-8')
        self.assertTrue(compare(self.lab)['all_prior_xmp_properties_unchanged'])

    def test_refuse_existing_git_and_malformed_pairs(self):
        prepare(self.export, self.lab)
        with self.assertRaises(ValueError):
            prepare(self.export, self.lab)
        (self.root/'.git').mkdir()
        with self.assertRaises(ValueError):
            prepare(self.export, self.root/'other')
        (self.root/'.git').rmdir()
        self.sidecar.unlink()
        with self.assertRaises(ValueError):
            prepare(self.export, self.root/'other')

    def test_unsafe_xml_refused_and_missing_file_not_success(self):
        self.sidecar.write_text('<!DOCTYPE x><x/>', encoding='utf-8')
        with self.assertRaises(ValueError):
            prepare(self.export, self.lab)
        self.assertFalse(self.lab.exists())
        self.sidecar.write_text(XMP, encoding='utf-8')
        prepare(self.export, self.lab)
        (self.lab/'collection'/'sample.heic').unlink()
        with self.assertRaises(ValueError):
            compare(self.lab)


if __name__ == '__main__':
    unittest.main()
