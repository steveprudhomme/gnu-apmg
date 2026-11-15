"""Review decisions use synthetic observations; never validate real user photos."""
# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
from contextlib import closing
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
import uuid

from photosemantique.review import catalogue, candidates, create, snapshot, apply_decisions
from photosemantique.phase2 import observation

AIRCRAFT='http://vocab.getty.edu/aat/300211102'
CAR='http://vocab.getty.edu/aat/300178739'


@unittest.skipUnless(importlib.util.find_spec('jsonschema'),'Install preparation extra')
class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='gnu-apmg-review-')
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.inputs=self.base/'inputs';self.inputs.mkdir()
        self.path=self.inputs/'observations.jsonl';self.folder=self.base/'review'
        manifest={'photo_id':'sha256:'+'a'*64,'derivative_sha256':'b'*64}
        self.row=observation(manifest,'object','model','planeur','Ollama','c'*64,tool_version='test')
        self.path.write_text(json.dumps(self.row)+'\n',encoding='utf-8')

    def session(self):
        create([self.path],self.folder)
        return snapshot(self.folder)

    def batch(self,payload,action='accept',uris=None):
        return {'version':1,'batch_id':str(uuid.uuid4()),'session_id':payload['session_id'],
            'base_revision':payload['revision'],'catalogue_digest':payload['catalogue_digest'],
            'decisions':[{'observation_id':self.row['observation_id'],'action':action,
                          'concept_uris':[AIRCRAFT] if uris is None else uris,'note':''}]}

    def write(self,batch):
        path=self.base/'decisions.json';path.write_text(json.dumps(batch),encoding='utf-8');return path

    def test_lexical_candidates_are_not_substrings_or_sensitive_inferences(self):
        concepts=catalogue()
        self.assertIn(AIRCRAFT,{c['uri'] for c in candidates(self.row,concepts)})
        self.assertFalse(candidates(dict(self.row,literal='avionique'),concepts))
        self.assertFalse(candidates(dict(self.row,type='text'),concepts))
        self.assertFalse(candidates(dict(self.row,literal='catholicisme'),concepts))

    def test_new_session_does_not_accept_anything_or_overwrite(self):
        p=self.session();self.assertEqual(p['revision'],0);self.assertEqual(p['decisions'],{})
        with self.assertRaises(ValueError):create([self.path],self.folder)

    def test_accept_replay_correction_and_history_preserve_sources(self):
        original=self.path.read_bytes();p=self.session();batch=self.batch(p)
        file=self.write(batch)
        self.assertEqual(apply_decisions(self.folder,file,'tester')['revision'],1)
        self.assertEqual(apply_decisions(self.folder,file,'tester')['status'],'already_applied')
        corrected=self.batch(snapshot(self.folder),'correct',[CAR])
        apply_decisions(self.folder,self.write(corrected),'tester')
        self.assertEqual(snapshot(self.folder)['decisions'][self.row['observation_id']]['concept_uris'],[CAR])
        with closing(sqlite3.connect(self.folder/'review.sqlite')) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM decisions').fetchone()[0],2)
        self.assertEqual(original,self.path.read_bytes())

    def test_stale_batches_do_not_overwrite_decisions(self):
        p=self.session();a=self.batch(p);b=self.batch(p,'reject',[])
        apply_decisions(self.folder,self.write(a),'tester')
        with self.assertRaisesRegex(ValueError,'stale'):apply_decisions(self.folder,self.write(b),'tester')
        self.assertEqual(snapshot(self.folder)['revision'],1)

    def test_invalid_batch_is_atomic(self):
        p=self.session();batch=self.batch(p)
        batch['decisions'].append({'observation_id':str(uuid.uuid4()),'action':'reject','concept_uris':[],'note':''})
        with self.assertRaises(ValueError):apply_decisions(self.folder,self.write(batch),'tester')
        self.assertEqual(snapshot(self.folder)['revision'],0)
        self.assertEqual(snapshot(self.folder)['decisions'],{})

    def test_retired_concept_and_manual_acceptance_are_refused(self):
        p=self.session()
        for action,uri in [('correct','http://cv.iptc.org/newscodes/mediatopic/20000564'),('accept',CAR)]:
            with self.assertRaises(ValueError):apply_decisions(self.folder,self.write(self.batch(p,action,[uri])),'tester')

    def test_decision_wrong_identity_and_duplicate_rows_are_refused(self):
        p=self.session();b=self.batch(p);b['session_id']=str(uuid.uuid4())
        with self.assertRaises(ValueError):apply_decisions(self.folder,self.write(b),'tester')
        b=self.batch(p);b['decisions']*=2
        with self.assertRaises(ValueError):apply_decisions(self.folder,self.write(b),'tester')

    def test_html_model_text_cannot_close_the_script(self):
        self.row['literal']='</script><img src=x onerror=alert(1)>'
        self.path.write_text(json.dumps(self.row),encoding='utf-8')
        self.session()
        html=(self.folder/'review.html').read_text(encoding='utf-8')
        self.assertNotIn(self.row['literal'],html)
        self.assertIn('\\u003c/script\\u003e',html)
        self.assertIn("connect-src 'none'",html)

    def test_outputs_in_input_or_git_are_refused(self):
        with self.assertRaises(ValueError):create([self.path],self.inputs/'review')
        repo=self.base/'repo';repo.mkdir();(repo/'.git').mkdir()
        with self.assertRaises(ValueError):create([self.path],repo/'review')

    def test_same_observation_id_with_changed_content_is_refused(self):
        other=self.inputs/'other.jsonl';other.write_text(json.dumps(dict(self.row,literal='changed')),encoding='utf-8')
        with self.assertRaises(ValueError):create([self.path,other],self.folder)

    def test_boolean_version_is_not_an_integer_version(self):
        p=self.session();batch=self.batch(p);batch['version']=True
        with self.assertRaises(ValueError):apply_decisions(self.folder,self.write(batch),'tester')

    def test_vocabulary_change_does_not_silently_reinterpret_decisions(self):
        from unittest.mock import patch
        p=self.session();file=self.write(self.batch(p))
        with patch('photosemantique.review.catalogue',return_value=[]):
            with self.assertRaisesRegex(ValueError,'snapshot changed'):apply_decisions(self.folder,file,'tester')
        self.assertEqual(snapshot(self.folder)['revision'],0)
