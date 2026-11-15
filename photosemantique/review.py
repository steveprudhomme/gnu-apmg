"""Private, offline keyword proposals and explicit human-decision journal."""
# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
from __future__ import annotations
import argparse
import base64
from contextlib import closing
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import uuid

from .taxonomy import DATA, normalize
from .inventory import _ensure_output_outside
from .phase2 import prepared
from .storage import now_utc

ALIASES = {
    '300211102': ['planeur', 'glider'], '300212616': ['avion', 'airplane'],
    '300178739': ['automobile', 'voiture', 'car'], '300178749': ['bateau', 'boat'],
    '300266506': ['oiseau', 'bird'], '300250130': ['chien', 'dog'],
    '300265960': ['chat domestique', 'domestic cat'], '300004792': ['bâtiment', 'building'],
    '300007836': ['pont', 'bridge'], '300132410': ['arbre', 'tree'],
    '300132399': ['fleur', 'flower'], '300008795': ['montagne', 'mountain'],
    '300008680': ['lac', 'lake'], '300008707': ['rivière', 'river']}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def catalogue():
    rows = []
    for source in ('iptc', 'getty'):
        for c in json.loads((DATA/(source+'.json')).read_text(encoding='utf-8'))['concepts']:
            if not c.get('retired'):
                rows.append(dict(c, source=source))
    return rows


def candidates(observation, concepts):
    """Lexical hints only, not semantic equivalences or confidence scores."""
    if observation['type'] != 'object':
        return []
    index = {c['uri']:c for c in concepts}
    def sensitive(uri, seen=None):
        seen = set() if seen is None else seen
        if uri in seen: return False
        seen.add(uri)
        if uri.rsplit('/',1)[-1] in {'07000000','12000000','14000000'}: return True
        return any(sensitive(p, seen) for p in index.get(uri, {}).get('broader', []))
    text = normalize(observation['literal'])
    found = []
    for c in concepts:
        if c.get('retired') or sensitive(c['uri']): continue
        labels = list(c['labels'].values()) + c.get('aliases', [])
        if c.get('editorial_label_fr'): labels.append(c['editorial_label_fr'])
        terms = [(s,'label') for s in labels] + [(s,'reviewed_alias') for s in ALIASES.get(c['uri'].rsplit('/',1)[-1],[])]
        matches = [(term, method) for term,method in terms if len(normalize(term)) >= 3
                   and re.search(r'(?<!\w)'+re.escape(normalize(term))+r'(?!\w)',text)]
        if matches:
            term, method = max(matches,key=lambda item:len(item[0]))
            found.append({'uri':c['uri'], 'matched_text':term, 'method':method,
                          'match_kind':'exact_label' if normalize(term)==text else 'phrase_in_object'})
    return sorted(found,key=lambda c:(c['match_kind']!='exact_label', c['uri']))[:12]


def read_observations(paths):
    from jsonschema import Draft202012Validator, FormatChecker
    schema = json.loads((Path(__file__).parent/'schemas/phase2-observation.schema.json').read_text(encoding='utf-8'))
    validator = Draft202012Validator(schema,format_checker=FormatChecker())
    rows = {}
    for path in paths:
        if path.stat().st_size > 25_000_000: raise ValueError('Observation file too large')
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            row = json.loads(line); validator.validate(row)
            key = row['observation_id']
            if key in rows and rows[key] != row: raise ValueError('Conflicting observation identity')
            rows[key] = row
            if len(rows)>10000: raise ValueError('Too many observations for one review')
    if not rows: raise ValueError('No observations')
    return list(rows.values())


def safe_session(folder):
    folder = _ensure_output_outside(DATA.resolve().parents[1],folder,'Private review')
    db = folder/'review.sqlite'
    if db.is_symlink() or (db.exists() and db.stat().st_nlink > 1):
        raise ValueError('Linked review database refused')
    return folder


def create(paths, output, prepared_dirs=()):
    paths = [p.resolve(strict=True) for p in paths]
    output = safe_session(output)
    for p in paths:
        _ensure_output_outside(p.parent,output,'Private review')
    if output.exists(): raise ValueError('Session exists; use a new directory')
    observations = read_observations(paths)
    concepts = catalogue()
    photos = {}
    for directory in prepared_dirs:
        manifest, data = prepared(directory)
        if not data.startswith(b'\x89PNG\r\n\x1a\n'): raise ValueError('Only prepared PNG previews accepted')
        photos[manifest['photo_id']] = base64.b64encode(data).decode('ascii')
    session_id = str(uuid.uuid4())
    payload = {'session_id':session_id,'revision':0,'catalogue_digest':digest(concepts),
        'catalogue':concepts, 'observations':observations,
        'candidates':{o['observation_id']:candidates(o,concepts) for o in observations},
        'photos':photos,'decisions':{}}
    output.mkdir(parents=True)
    with closing(sqlite3.connect(output/'review.sqlite')) as db:
        db.executescript('''CREATE TABLE metadata (id INTEGER PRIMARY KEY CHECK(id=1), payload TEXT NOT NULL, revision INTEGER NOT NULL);
            CREATE TABLE batches (batch_id TEXT PRIMARY KEY, digest TEXT NOT NULL, revision INTEGER NOT NULL);
            CREATE TABLE decisions (event_id TEXT PRIMARY KEY, batch_id TEXT NOT NULL REFERENCES batches(batch_id),
                observation_id TEXT NOT NULL, action TEXT NOT NULL, concepts TEXT NOT NULL,
                actor TEXT NOT NULL, note TEXT NOT NULL, created_at TEXT NOT NULL, revision INTEGER NOT NULL);''')
        with db: db.execute('INSERT INTO metadata VALUES(1,?,0)',(canonical(payload),))
    render(output)
    return {'session_id':session_id,'observations':len(observations),
            'objects':sum(o['type']=='object' for o in observations),
            'with_candidates':sum(bool(v) for v in payload['candidates'].values()),'decisions':0}


def snapshot(folder):
    folder = safe_session(folder)
    db_path = folder/'review.sqlite'
    if not db_path.is_file(): raise ValueError('Session missing')
    with closing(sqlite3.connect(db_path.as_uri()+'?mode=ro',uri=True)) as db:
        db.row_factory = sqlite3.Row
        meta = db.execute('SELECT payload,revision FROM metadata WHERE id=1').fetchone()
        payload = json.loads(meta['payload']);payload['revision']=meta['revision']
        for row in db.execute('SELECT * FROM decisions ORDER BY revision,rowid'):
            payload['decisions'][row['observation_id']] = {'action':row['action'],
                'concept_uris':json.loads(row['concepts']),'note':row['note'],
                'actor':row['actor'],'created_at':row['created_at']}
        return payload


def apply_decisions(folder, decision_file, actor):
    folder = safe_session(folder)
    if not (folder/'review.sqlite').is_file(): raise ValueError('Session missing')
    if not actor.strip() or len(actor)>200: raise ValueError('Actor declaration required')
    if decision_file.stat().st_size>5_000_000: raise ValueError('Decision file too large')
    batch = json.loads(decision_file.read_text(encoding='utf-8'))
    if not isinstance(batch,dict) or set(batch)!={'version','batch_id','session_id','base_revision','catalogue_digest','decisions'}:
        raise ValueError('Invalid decision envelope')
    if type(batch['version']) is not int or batch['version']!=1 or type(batch['base_revision']) is not int or batch['base_revision']<0:
        raise ValueError('Invalid decision version/revision')
    uuid.UUID(batch['batch_id'])
    batch_digest = digest({'batch':batch,'actor':actor})
    with closing(sqlite3.connect(folder/'review.sqlite')) as db:
        db.execute('PRAGMA foreign_keys=ON');db.execute('BEGIN IMMEDIATE')
        try:
            previous=db.execute('SELECT digest,revision FROM batches WHERE batch_id=?',(batch['batch_id'],)).fetchone()
            if previous:
                if previous[0]!=batch_digest: raise ValueError('Batch identity reused with different content')
                return {'status':'already_applied','revision':previous[1]}
            raw, revision = db.execute('SELECT payload,revision FROM metadata WHERE id=1').fetchone()
            payload=json.loads(raw)
            if batch['session_id']!=payload['session_id'] or batch['base_revision']!=revision:
                raise ValueError('Wrong session or stale decision revision')
            if batch['catalogue_digest']!=payload['catalogue_digest'] or digest(catalogue())!=payload['catalogue_digest']:
                raise ValueError('Vocabulary snapshot changed; create a new review')
            obs={o['observation_id']:o for o in payload['observations']}
            index={c['uri']:c for c in payload['catalogue']}
            decisions=batch['decisions']
            if not isinstance(decisions,list) or not decisions: raise ValueError('No decisions')
            seen=set()
            for d in decisions:
                if set(d)!={'observation_id','action','concept_uris','note'}: raise ValueError('Invalid decision fields')
                oid=d['observation_id'];uris=d['concept_uris']
                if oid not in obs or oid in seen: raise ValueError('Unknown or duplicate observation')
                seen.add(oid)
                if d['action'] not in ('accept','correct','reject'): raise ValueError('Invalid action')
                if not isinstance(d['note'],str) or len(d['note'])>2000: raise ValueError('Invalid note')
                if not isinstance(uris,list) or len(uris)>30 or any(not isinstance(u,str) for u in uris) or len(set(uris))!=len(uris): raise ValueError('Invalid concepts')
                if d['action']=='reject' and uris: raise ValueError('Rejection cannot accept a concept')
                if d['action']!='reject' and not uris: raise ValueError('A concept selection is required')
                if any(u not in index or index[u].get('retired') for u in uris): raise ValueError('Unknown/retired concept')
                offered={c['uri'] for c in payload['candidates'][oid]}
                if d['action']=='accept' and not set(uris)<=offered: raise ValueError('Use correction for manual concepts')
            next_revision=revision+1
            db.execute('INSERT INTO batches VALUES(?,?,?)',(batch['batch_id'],batch_digest,next_revision))
            for d in decisions:
                db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?,?,?,?)',(str(uuid.uuid4()),batch['batch_id'],
                    d['observation_id'],d['action'],canonical(d['concept_uris']),actor,d['note'],now_utc(),next_revision))
            db.execute('UPDATE metadata SET revision=? WHERE id=1',(next_revision,));db.commit()
        except Exception:
            db.rollback();raise
    # Rendering is repeatable independently if the HTML write fails after commit.
    render(folder)
    return {'status':'applied','revision':next_revision,'decisions':len(decisions)}


def render(folder):
    payload=snapshot(folder)
    template=(Path(__file__).parent/'templates/review.html').read_text(encoding='utf-8')
    data=canonical(payload).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    target=folder/'review.html'
    if target.is_symlink() or (target.exists() and target.stat().st_nlink>1): raise ValueError('Linked HTML refused')
    target.write_text(template.replace('/*__REVIEW_DATA__*/',data),encoding='utf-8')


def main(argv=None):
    parser=argparse.ArgumentParser(description='GNU APMG offline keyword review')
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('create');p.add_argument('--input',type=Path,action='append',required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--prepared',type=Path,action='append',default=[])
    p=sub.add_parser('apply');p.add_argument('session',type=Path);p.add_argument('--decisions',type=Path,required=True);p.add_argument('--actor',required=True)
    for name in ('render','status'):
        p=sub.add_parser(name);p.add_argument('session',type=Path)
    a=parser.parse_args(argv)
    try:
        if a.command=='create':result=create(a.input,a.output,a.prepared)
        elif a.command=='apply':result=apply_decisions(a.session,a.decisions,a.actor)
        elif a.command=='render':render(a.session);result={'status':'rendered'}
        else:
            payload=snapshot(a.session)
            result={'session_id':payload['session_id'],'revision':payload['revision'],
                'observations':len(payload['observations']),'decided':len(payload['decisions'])}
        print(json.dumps(result));return 0
    except Exception as exc:
        messages={
            'Wrong session or stale decision revision':('stale_session','La page ou le fichier ne correspond pas à la révision actuelle. Rouvrez la page actualisée.'),
            'Vocabulary snapshot changed; create a new review':('vocabulary_changed','Le vocabulaire a changé. Créez une nouvelle session ; les décisions précédentes sont conservées.'),
            'Session exists; use a new directory':('session_exists','Ce dossier existe déjà. Choisissez un nouveau dossier de session.'),
            'Unknown/retired concept':('invalid_concept','Un concept est inconnu ou retiré. Aucun changement importé.'),
            'Use correction for manual concepts':('manual_correction_required','Un choix manuel doit être enregistré comme correction.'),
            'Batch identity reused with different content':('batch_conflict','Ce lot a déjà été importé avec un contenu ou acteur différent.')}
        code,message=messages.get(str(exc),('invalid_review','Opération refusée. Vérifiez les fichiers, leurs champs et les chemins privés indiqués dans le tutoriel.'))
        print(json.dumps({'status':'failed','error_type':type(exc).__name__,'error_code':code,'message':message},ensure_ascii=False));return 1


if __name__=='__main__':raise SystemExit(main())
