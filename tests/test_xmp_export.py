"""Sidecar merge, source integrity and rollback on synthetic data."""
# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from photosemantique.xmp_export import NS,merge_xmp,selected,export_bundle,rollback,tag
from photosemantique.inventory import hash_file


class XmpTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='gnu-apmg-xmp-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.images=self.root/'images';self.images.mkdir()
        self.image=self.images/'école.heic';self.image.write_bytes(b'synthetic-source-bytes')
        self.photo='sha256:'+hash_file(self.image)[0]
        self.concept={'uri':'http://vocab.getty.edu/aat/300211102','source':'getty','labels':{'en':'gliders (aircraft)'},'editorial_label_fr':'Planeurs','broader':[],'retired':None}
        self.payload={'session_id':'synthetic','revision':1,'catalogue_digest':'a'*64,
            'catalogue':[self.concept],'observations':[{'observation_id':'o1','photo_id':self.photo}],
            'decisions':{'o1':{'action':'accept','concept_uris':[self.concept['uri']]}}}
        self.session=self.root/'review';self.session.mkdir();self.out=self.root/'export'

    def export(self):
        with patch('photosemantique.xmp_export.snapshot',return_value=self.payload):
            return export_bundle(self.session,self.images,self.out)

    def test_only_current_human_decisions_are_exported(self):
        self.payload['decisions']['o1']['action']='reject'
        self.assertFalse(selected(self.payload))
        self.payload['decisions']={}
        self.assertFalse(selected(self.payload))

    def test_merge_preserves_other_fields_and_deduplicates(self):
        previous=f'''<x:xmpmeta xmlns:x="adobe:ns:meta/" xmlns:rdf="{NS['rdf']}" xmlns:dc="{NS['dc']}"><rdf:RDF><rdf:Description><dc:title><rdf:Alt><rdf:li xml:lang="x-default">Titre existant</rdf:li></rdf:Alt></dc:title><dc:subject><rdf:Bag><rdf:li>Ancien</rdf:li><rdf:li>Planeurs</rdf:li></rdf:Bag></dc:subject></rdf:Description></rdf:RDF></x:xmpmeta>'''.encode()
        result=merge_xmp(previous,[self.concept,self.concept],{self.concept['uri']:self.concept})
        root=ET.fromstring(result)
        self.assertEqual([n.text for n in root.findall('.//dc:subject/rdf:Bag/rdf:li',NS)],['Ancien','Planeurs'])
        self.assertEqual(root.find('.//dc:title/rdf:Alt/rdf:li',NS).text,'Titre existant')
        self.assertEqual(len(root.findall('.//Iptc4xmpExt:CvTermId',NS)),1)

    def test_no_sidecar_export_and_rollback_preserve_photo_bytes(self):
        before=self.image.read_bytes();self.export()
        sidecar=next((self.out/'files').glob('*.xmp'))
        copied=next(p for p in (self.out/'files').iterdir() if p.suffix!='.xmp')
        self.assertTrue(sidecar.name.endswith('.heic.xmp'))
        self.assertEqual(copied.read_bytes(),before)
        self.assertEqual(rollback(self.out)['status'],'rolled_back')
        self.assertFalse(sidecar.exists());self.assertTrue(copied.exists())
        self.assertEqual(self.image.read_bytes(),before)
        self.assertEqual(rollback(self.out)['status'],'already_rolled_back')

    def test_existing_sidecar_restored_byte_for_byte(self):
        original=merge_xmp(None,[],{})
        self.image.with_name(self.image.name+'.xmp').write_bytes(original)
        self.export();rollback(self.out)
        self.assertEqual(next((self.out/'files').glob('*.xmp')).read_bytes(),original)
        self.assertEqual(self.image.with_name(self.image.name+'.xmp').read_bytes(),original)

    def test_changed_sidecar_prevents_rollback(self):
        self.export();sidecar=next((self.out/'files').glob('*.xmp'));sidecar.write_bytes(b'user-edit')
        with self.assertRaises(ValueError):rollback(self.out)
        self.assertEqual(sidecar.read_bytes(),b'user-edit')

    def test_output_inside_sources_and_overwrite_are_refused(self):
        with self.assertRaises(ValueError):export_bundle(self.session,self.images,self.images/'export')
        self.export()
        with self.assertRaises(ValueError):self.export()

    def test_ambiguous_sidecars_and_dtd_are_refused(self):
        self.image.with_suffix('.xmp').write_bytes(b'one')
        self.image.with_name(self.image.name+'.xmp').write_bytes(b'two')
        with self.assertRaises(ValueError):self.export()
        with self.assertRaises(ValueError):merge_xmp(b'<!DOCTYPE x><x/>',[],{})
        with self.assertRaises((ValueError,UnicodeError)):merge_xmp('<!DOCTYPE x><x/>'.encode('utf-16'),[],{})

    def test_interrupted_rollback_can_resume(self):
        original=merge_xmp(None,[],{})
        self.image.with_name(self.image.name+'.xmp').write_bytes(original)
        other=self.images/'second.jpg';other.write_bytes(b'second-synthetic-source')
        other.with_name(other.name+'.xmp').write_bytes(original)
        self.payload['observations'].append({'observation_id':'o2','photo_id':'sha256:'+hash_file(other)[0]})
        self.payload['decisions']['o2']=self.payload['decisions']['o1']
        self.export()
        from photosemantique.xmp_export import atomic_write as real_write
        count=0
        def interrupted(path,data):
            nonlocal count
            if path.suffix=='.xmp':
                count+=1
                if count==2:raise OSError('synthetic interruption')
            return real_write(path,data)
        with patch('photosemantique.xmp_export.atomic_write',side_effect=interrupted):
            with self.assertRaises(OSError):rollback(self.out)
        self.assertEqual(rollback(self.out)['status'],'rolled_back')
        self.assertTrue(all(p.read_bytes()==original for p in (self.out/'files').glob('*.xmp')))

    def test_journal_path_escape_is_refused(self):
        self.export()
        path=self.out/'journal.json';data=json.loads(path.read_text(encoding='utf-8'))
        data['files'][0]['photo']='../outside.heic'
        path.write_text(json.dumps(data),encoding='utf-8')
        with self.assertRaises(ValueError):rollback(self.out)
