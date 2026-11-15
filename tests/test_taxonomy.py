"""Validate public vocabulary provenance, lifecycle and semantic distinctions."""
# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

from photosemantique.taxonomy import DATA, search, validate_concepts

ROOT = Path(__file__).resolve().parents[1]


class TaxonomyTests(unittest.TestCase):
    def test_closed_iptc_hierarchy_and_retired_filter(self):
        records = json.loads((DATA/'iptc.json').read_text(encoding='utf-8'))['concepts']
        validate_concepts(records)
        self.assertEqual(len(records),1394)
        self.assertEqual(sum(c['top_concept'] for c in records),17)
        self.assertEqual(sum(bool(c['retired']) for c in records),335)
        self.assertEqual(len(search('')),1059)
        self.assertTrue(all(not c['retired'] for c in search('tourisme')))

    def test_homonymous_marriage_concepts_are_not_merged(self):
        rows = search('MARIAGE')
        ids = {r['uri'].rsplit('/',1)[-1] for r in rows}
        self.assertIn('20000786',ids)  # marriage as institution
        self.assertIn('20001236',ids)  # wedding as ceremony

    def test_getty_glider_is_aircraft_not_furniture(self):
        rows = search('planeur',source='getty')
        self.assertEqual([c['uri'].rsplit('/',1)[-1] for c in rows],['300211102'])
        self.assertEqual(rows[0]['labels']['en'],'gliders (aircraft)')
        self.assertNotIn('fr',rows[0]['labels'])  # editorial translation is separate

    def test_reference_and_cycle_failures_are_not_accepted(self):
        uri='http://cv.iptc.org/newscodes/mediatopic/1'
        with self.assertRaisesRegex(ValueError,'cycle'):
            validate_concepts([{'uri':uri,'labels':{'fr':'test'},'broader':[uri]}])
        with self.assertRaisesRegex(ValueError,'Unknown parent'):
            validate_concepts([{'uri':uri,'labels':{'fr':'test'},'broader':[uri+'2']}])

    def test_reproducible_offline_generation(self):
        completed = subprocess.run([sys.executable,'-X','utf8','scripts/build_taxonomy.py','--check'],
            cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(completed.returncode,0,completed.stdout+completed.stderr)

    @unittest.skipUnless(importlib.util.find_spec('rdflib'),'Install taxonomy-validation extra')
    def test_export_is_parseable_skos_with_original_ids(self):
        from rdflib import Graph, Namespace, RDF
        g=Graph().parse(ROOT/'docs/ontology/iptc-mediatopics.fr-en.ttl',format='turtle')
        skos=Namespace('http://www.w3.org/2004/02/skos/core#')
        self.assertEqual(len(set(g.subjects(RDF.type,skos.Concept))),1394)
        self.assertEqual(len(list(g.triples((None, skos.topConceptOf, None)))),17)
