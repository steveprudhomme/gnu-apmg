"""Phase 2 regression checks without downloading or invoking AI models."""
# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from photosemantique.phase2 import prepare, prepared, vision, sha, main

AVAILABLE = all(importlib.util.find_spec(m) for m in ('PIL', 'pillow_heif', 'jsonschema'))


@unittest.skipUnless(AVAILABLE, 'Install the preparation extra for Phase 2 tests')
class Phase2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='gnu-apmg-p2-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.sources = self.base/'sources'
        self.sources.mkdir()
        self.source = self.sources/'école.jpg'
        from PIL import Image
        image = Image.new('RGB', (120, 80), 'red')
        exif = image.getexif()
        exif[274] = 6
        exif[270] = 'PRIVATE SYNTHETIC METADATA'
        image.save(self.source, exif=exif)
        self.folder = self.base/'derived'

    def test_orientation_metadata_stripping_integrity_and_no_overwrite(self):
        from PIL import Image
        before = self.source.read_bytes()
        result = prepare(self.source, self.folder)
        self.assertEqual([result['width'], result['height']], [80,120])
        self.assertEqual(result['photo_id'], 'sha256:'+sha(before))
        with Image.open(self.folder/'image.png') as image:
            self.assertFalse(image.getexif())
            self.assertNotIn('exif', image.info)
            self.assertNotIn('xmp', image.info)
        self.assertEqual(before, self.source.read_bytes())
        with self.assertRaises(ValueError): prepare(self.source, self.folder)

    def test_source_and_git_output_rejected_before_creation(self):
        with self.assertRaises(ValueError): prepare(self.source, self.sources/'output')
        repo = self.base/'repo'
        repo.mkdir(); (repo/'.git').mkdir()
        with self.assertRaises(ValueError): prepare(self.source, repo/'output')
        self.assertFalse((repo/'output').exists())

    def test_tampered_derivative_rejected(self):
        prepare(self.source, self.folder)
        (self.folder/'image.png').write_bytes(b'changed')
        with self.assertRaises(ValueError): prepared(self.folder)

    def test_vision_schema_and_provenance(self):
        prepare(self.source, self.folder)
        def api(path, payload=None):
            if path == '/api/tags': return {'models':[{'name':'test:local','digest':'a'*64,'details':{'format':'gguf'}}]}
            if path == '/api/show': return {'capabilities':['vision']}
            if path == '/api/version': return {'version':'synthetic'}
            return {'done':True,'response':json.dumps({'description':'Test','objects':['red']})}
        with patch('photosemantique.phase2.local_api', side_effect=api):
            rows = vision(self.folder, 'test:local')
        self.assertEqual(len(rows),2)
        self.assertTrue(all(r['confidence'] is None and r['status']=='suggested' for r in rows))
        self.assertTrue(all(r['model_digest']=='a'*64 for r in rows))
        self.assertTrue(all(len(r['prompt_digest'])==64 for r in rows))

    def test_no_implicit_model_pull(self):
        prepare(self.source, self.folder)
        with patch('photosemantique.phase2.local_api', return_value={'models':[]}) as api:
            with self.assertRaises(ValueError): vision(self.folder, 'missing')
        self.assertEqual(api.call_count,1)

    def test_remote_model_and_invalid_response_rejected(self):
        prepare(self.source, self.folder)
        with patch('photosemantique.phase2.local_api', return_value={
            'models':[{'name':'test:local','digest':'a'*64,'remote_host':'example.invalid'}]}):
            with self.assertRaises(ValueError): vision(self.folder, 'test:local')
        def api(path, payload=None):
            if path == '/api/tags': return {'models':[{'name':'test:local','digest':'a'*64,'details':{'format':'gguf'}}]}
            if path == '/api/show': return {'capabilities':['vision']}
            return {'done':True,'response':'{"description":"test","objects":[],"status":"validated"}'}
        from jsonschema import ValidationError
        with patch('photosemantique.phase2.local_api', side_effect=api):
            with self.assertRaises(ValidationError): vision(self.folder, 'test:local')

    def test_corrupt_image_creates_no_output(self):
        self.source.write_bytes(b'corrupt')
        self.assertEqual(main(['prepare',str(self.source),'--output',str(self.folder)]),1)
        self.assertFalse(self.folder.exists())

    def test_truncated_response_writes_no_observations(self):
        prepare(self.source, self.folder)
        output = self.base/'observations.jsonl'
        with patch('photosemantique.phase2.vision', side_effect=ValueError('Incomplete model response')):
            self.assertEqual(main(['vision', str(self.folder), '--model', 'test:local', '--output', str(output)]),1)
        self.assertFalse(output.exists())
