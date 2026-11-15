"""Reversible keyword sidecars in a new private bundle; sources are read-only."""
# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import unicodedata
import xml.etree.ElementTree as ET

from .inventory import discover, hash_file, _ensure_output_outside
from .review import snapshot, canonical, digest
from .storage import now_utc

NS={'x':'adobe:ns:meta/','rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'dc':'http://purl.org/dc/elements/1.1/','lr':'http://ns.adobe.com/lightroom/1.0/',
    'Iptc4xmpExt':'http://iptc.org/std/Iptc4xmpExt/2008-02-29/'}
for prefix,uri in NS.items(): ET.register_namespace(prefix,uri)
def tag(prefix,name): return '{'+NS[prefix]+'}'+name
def label(c): return c.get('editorial_label_fr') or c['labels'].get('fr') or c['labels'].get('en-US') or c['labels'].get('en-GB') or c['labels']['en']


def selected(payload):
    obs={o['observation_id']:o for o in payload['observations']}
    concepts={c['uri']:c for c in payload['catalogue']}
    result={}
    for oid,d in payload['decisions'].items():
        if d['action'] not in ('accept','correct'):continue
        photo=obs[oid]['photo_id'];bucket=result.setdefault(photo,{})
        for uri in d['concept_uris']:
            if uri not in concepts or concepts[uri].get('retired'):raise ValueError('Invalid validated concept')
            bucket[uri]=concepts[uri]
    return result


def hierarchies(c,index,seen=()):
    if c['uri'] in seen:raise ValueError('Concept cycle')
    name=label(c)
    if '|' in name:raise ValueError('Hierarchy delimiter inside label')
    parents=[index[u] for u in c['broader'] if u in index]
    if not parents:return [(('Getty AAT' if c['source']=='getty' else 'IPTC Media Topics')+'|'+name)]
    paths=[path+'|'+name for parent in parents for path in hierarchies(parent,index,(*seen,c['uri']))]
    if len(paths)>32:raise ValueError('Too many hierarchy paths')
    return sorted(set(paths))


def merge_xmp(previous,concepts,index):
    if previous:
        if len(previous)>10_000_000:raise ValueError('XMP too large')
        text=previous.decode('utf-8-sig')
        if '\x00' in text or '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
            raise ValueError('Unsupported/unsafe XMP XML')
        root=ET.fromstring(text,parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True,insert_pis=True)))
        rdf=root if root.tag==tag('rdf','RDF') else root.find('rdf:RDF',NS)
        if rdf is None:raise ValueError('XMP RDF root missing')
    else:
        root=ET.Element(tag('x','xmpmeta'));rdf=ET.SubElement(root,tag('rdf','RDF'))
    descriptions=rdf.findall('rdf:Description',NS)
    description=descriptions[0] if descriptions else ET.SubElement(rdf,tag('rdf','Description'),{tag('rdf','about'):''})
    def bag(prefix,name):
        key=tag(prefix,name)
        holders=[d for d in rdf.findall('rdf:Description',NS) if key in d.attrib or d.find(key) is not None]
        if sum(len(d.findall(key))+(key in d.attrib) for d in holders)>1:raise ValueError('Ambiguous repeated XMP property')
        holder=holders[0] if holders else description
        prop=holder.find(key)
        if prop is not None and key in holder.attrib:raise ValueError('Ambiguous attribute and element property')
        if prop is None:
            prop=ET.SubElement(holder,key);items=ET.SubElement(prop,tag('rdf','Bag'))
            if key in holder.attrib:ET.SubElement(items,tag('rdf','li')).text=holder.attrib.pop(key)
        else:
            items=prop.find('rdf:Bag',NS)
            if items is None:raise ValueError('Unsupported XMP property shape')
        return items
    subjects=bag('dc','subject');paths=bag('lr','hierarchicalSubject');terms=bag('Iptc4xmpExt','AboutCvTerm')
    def append_unique(container,values):
        existing=set()
        for node in container:
            if node.tag!=tag('rdf','li') or len(node):raise ValueError('Unsupported keyword item')
            existing.add(unicodedata.normalize('NFC',node.text or ''))
        for value in values:
            value=unicodedata.normalize('NFC',value)
            if value not in existing:ET.SubElement(container,tag('rdf','li')).text=value;existing.add(value)
    append_unique(subjects,[label(c) for c in concepts])
    append_unique(paths,[p for c in concepts for p in hierarchies(c,index)])
    existing={n.text or n.get(tag('rdf','resource')) for n in terms.findall('.//Iptc4xmpExt:CvTermId',NS)}
    for c in concepts:
        if c['uri'] in existing:continue
        item=ET.SubElement(terms,tag('rdf','li'),{tag('rdf','parseType'):'Resource'})
        ET.SubElement(item,tag('Iptc4xmpExt','CvId')).text=('http://cv.iptc.org/newscodes/mediatopic/' if c['source']=='iptc' else 'http://vocab.getty.edu/aat/')
        ET.SubElement(item,tag('Iptc4xmpExt','CvTermId')).text=c['uri']
        name=ET.SubElement(item,tag('Iptc4xmpExt','CvTermName'));alt=ET.SubElement(name,tag('rdf','Alt'))
        ET.SubElement(alt,tag('rdf','li'),{'{http://www.w3.org/XML/1998/namespace}lang':'x-default'}).text=label(c)
        existing.add(c['uri'])
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)


def existing_sidecar(source):
    paths={p for p in (source.with_name(source.name+'.xmp'),source.with_suffix('.xmp')) if p.exists()}
    if len(paths)>1:raise ValueError('Two possible sidecars; resolve ambiguity first')
    if not paths:return None
    path=paths.pop()
    if path.is_symlink() or not path.is_file():raise ValueError('Linked/non-regular sidecar refused')
    return path


def plan(session,images):
    payload=snapshot(session);wanted=selected(payload)
    if not wanted:raise ValueError('No human-validated keywords')
    images=images.resolve(strict=True);resolved={};errors=0
    for path,error in discover(images):
        if error:errors+=1;continue
        try:photo='sha256:'+hash_file(path)[0]
        except OSError:errors+=1;continue
        if photo in wanted and photo not in resolved:resolved[photo]=path
    if set(resolved)!=set(wanted):raise ValueError('Validated photos not all resolved by hash')
    index={c['uri']:c for c in payload['catalogue']}
    items=[]
    for photo in sorted(wanted):
        source=resolved[photo];sidecar=existing_sidecar(source)
        concepts=sorted(wanted[photo].values(),key=lambda c:c['uri'])
        items.append({'photo_id':photo,'source':str(source),'source_sidecar':str(sidecar) if sidecar else None,
            'sidecar_sha256':hash_file(sidecar)[0] if sidecar else None,
            'keywords':[label(c) for c in concepts],'concept_uris':[c['uri'] for c in concepts],
            'hierarchies':sorted({p for c in concepts for p in hierarchies(c,index)})})
    return {'version':1,'session_id':payload['session_id'],'revision':payload['revision'],
            'catalogue_digest':payload['catalogue_digest'],'resolution_errors':errors,'items':items}


def private_output(session,images,output):
    for root in (session.resolve(),images.resolve()):output=_ensure_output_outside(root,output,'Private export')
    return output


def export_bundle(session,images,output):
    output=private_output(session,images,output)
    if output.exists():raise ValueError('Export directory already exists')
    export_plan=plan(session,images);payload=snapshot(session)
    if payload['revision']!=export_plan['revision']:raise ValueError('Review changed during planning')
    index={c['uri']:c for c in payload['catalogue']}
    output.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.gnu-apmg-export-',dir=output.parent)).resolve()
    assert stage.parent==output.parent and stage.name.startswith('.gnu-apmg-export-')
    try:
        (stage/'files').mkdir();(stage/'backups').mkdir()
        journal=dict(export_plan,created_at=now_utc(),status='exported',files=[])
        for item in export_plan['items']:
            source=Path(item['source']);expected=item['photo_id'].split(':',1)[1]
            copied=stage/'files'/(expected+source.suffix.lower());shutil.copyfile(source,copied)
            if hash_file(source)[0]!=expected or hash_file(copied)[0]!=expected:raise ValueError('Photo integrity changed')
            old=None;backup=None
            if item['source_sidecar']:
                source_xmp=Path(item['source_sidecar']);old=source_xmp.read_bytes()
                if hash_file(source_xmp)[0]!=item['sidecar_sha256']:raise ValueError('Source sidecar changed')
                backup=stage/'backups'/(expected+'.xmp');backup.write_bytes(old)
            target=copied.with_name(copied.name+'.xmp')
            target.write_bytes(merge_xmp(old,[index[u] for u in item['concept_uris']],index))
            journal['files'].append({'photo':copied.relative_to(stage).as_posix(),'photo_sha256':expected,
                'sidecar':target.relative_to(stage).as_posix(),'export_sha256':hash_file(target)[0],
                'backup':backup.relative_to(stage).as_posix() if backup else None,
                'backup_sha256':item['sidecar_sha256']})
        if snapshot(session)['revision']!=export_plan['revision']:raise ValueError('Review changed during export')
        (stage/'journal.json').write_text(canonical(journal),encoding='utf-8')
        stage.rename(output)
        return {'status':'exported','photos':len(journal['files']),'revision':journal['revision']}
    finally:
        if stage.exists():
            if stage.parent!=output.parent or not stage.name.startswith('.gnu-apmg-export-') or stage.is_symlink():raise ValueError('Unsafe staging cleanup')
            shutil.rmtree(stage)


def local_file(root,value):
    path=PurePosixPath(value)
    if not path.parts or path.is_absolute() or '..' in path.parts or '\\' in value or ':' in value or path.parts[0] not in ('files','backups'):
        raise ValueError('Unsafe journal path')
    result=root.joinpath(*path.parts)
    if root not in result.resolve().parents or any(p.is_symlink() or getattr(p,'is_junction',lambda:False)() for p in (result,*result.parents) if p!=root):
        raise ValueError('Linked/escaped export path')
    if result.exists() and result.stat().st_nlink>1:raise ValueError('Hard-linked export file refused')
    return result


def atomic_write(path,data):
    fd,name=tempfile.mkstemp(prefix='.gnu-apmg-write-',dir=path.parent)
    temporary=Path(name)
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(data);stream.flush();os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def rollback(output):
    output=_ensure_output_outside(Path(__file__).resolve().parents[1],output,'Export rollback')
    journal_path=output/'journal.json'
    if journal_path.is_symlink() or journal_path.stat().st_nlink>1:raise ValueError('Linked journal refused')
    journal=json.loads(journal_path.read_text(encoding='utf-8'))
    if journal['status']=='rolled_back':return {'status':'already_rolled_back'}
    if journal['status'] not in ('exported','rolling_back'):raise ValueError('Unsupported export state')
    resuming=journal['status']=='rolling_back'
    files=[]
    seen=set()
    for record in journal['files']:
        if record['sidecar']!=record['photo']+'.xmp' or not record['photo'].startswith('files/') or (record['backup'] and not record['backup'].startswith('backups/')) or record['sidecar'] in seen:
            raise ValueError('Invalid journal file roles')
        seen.add(record['sidecar'])
        photo=local_file(output,record['photo']);sidecar=local_file(output,record['sidecar'])
        backup=local_file(output,record['backup']) if record['backup'] else None
        already_done=resuming and ((backup and sidecar.exists() and hash_file(sidecar)[0]==record['backup_sha256']) or (not backup and not sidecar.exists()))
        if sidecar.suffix!='.xmp' or hash_file(photo)[0]!=record['photo_sha256'] or (not already_done and (not sidecar.exists() or hash_file(sidecar)[0]!=record['export_sha256'])):
            raise ValueError('Export changed; rollback refused')
        if backup and hash_file(backup)[0]!=record['backup_sha256']:raise ValueError('Backup changed')
        files.append((sidecar,backup,already_done,record['export_sha256']))
    journal['status']='rolling_back'
    atomic_write(journal_path,canonical(journal).encode('utf-8'))
    for sidecar,backup,already_done,expected in files:
        if already_done:continue
        if hash_file(sidecar)[0]!=expected:raise ValueError('Sidecar changed during rollback')
        if backup:atomic_write(sidecar,backup.read_bytes())
        else:sidecar.unlink()
    journal['status']='rolled_back';journal['rolled_back_at']=now_utc()
    atomic_write(journal_path,canonical(journal).encode('utf-8'))
    return {'status':'rolled_back','sidecars':len(files),'photos_retained':len(files)}


def main(argv=None):
    parser=argparse.ArgumentParser(description='GNU APMG private XMP export on copies')
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ('plan','export'):
        p=sub.add_parser(name);p.add_argument('--session',type=Path,required=True);p.add_argument('--images',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('rollback');p.add_argument('output',type=Path)
    a=parser.parse_args(argv)
    try:
        if a.command=='plan':
            out=private_output(a.session,a.images,a.output)
            if out.exists():raise ValueError('Plan output exists')
            data=plan(a.session,a.images);out.parent.mkdir(parents=True,exist_ok=True)
            with out.open('x',encoding='utf-8') as f:f.write(canonical(data))
            result={'status':'planned','photos':len(data['items']),'revision':data['revision']}
        elif a.command=='export':result=export_bundle(a.session,a.images,a.output)
        else:result=rollback(a.output)
        print(json.dumps(result));return 0
    except Exception as exc:
        print(json.dumps({'status':'failed','error_type':type(exc).__name__}));return 1


if __name__=='__main__':raise SystemExit(main())
