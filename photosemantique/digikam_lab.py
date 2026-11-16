"""Private, non-destructive round-trip laboratory; never asserts GUI success."""
# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

RDF = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def properties(path):
    """Conservative XML comparison, not a complete RDF equivalence engine."""
    raw = path.read_bytes()
    if len(raw) > 10_000_000:
        raise ValueError('XMP too large')
    text = raw.decode('utf-8-sig')
    if '\0' in text or '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise ValueError('Unsupported XML')
    root = ET.fromstring(text)

    def value(node):
        children = [value(child) for child in node]
        if node.tag in (RDF+'Bag', RDF+'Alt'):
            children.sort(key=lambda item: json.dumps(item, sort_keys=True))
        text_value = (node.text or '').strip() if children else (node.text or '')
        return [node.tag, [list(pair) for pair in sorted(node.attrib.items())], text_value, children]

    result = {}
    for desc in root.iter(RDF+'Description'):
        # Only top-level descriptions: nested structures belong to their property.
        if not any(desc is child for rdf in root.iter(RDF+'RDF') for child in rdf):
            continue
        for key, val in desc.attrib.items():
            if key != RDF+'about':
                result.setdefault(key, []).append(['attribute', val])
        for child in desc:
            result.setdefault(child.tag, []).append(value(child))
    if not result:
        raise ValueError('No XMP properties')
    return result


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def regular(path):
    if path.is_symlink() or path.is_junction() or not path.is_file():
        raise ValueError('Expected a regular file')


def outside_git(path):
    if any((parent/'.git').exists() for parent in (path, *path.parents)):
        raise ValueError('Private laboratory must be outside Git')


def prepare(export, lab):
    export = Path(export).resolve(strict=True)
    lab = Path(lab).absolute()
    outside_git(lab.resolve())
    if lab.exists() or lab.resolve().is_relative_to(export):
        raise ValueError('Laboratory must be new and outside reference export')
    source = export/'files'
    if source.is_symlink() or source.is_junction():
        raise ValueError('Linked collection refused')
    files = sorted(source.iterdir())
    images = [p for p in files if p.suffix.lower() != '.xmp']
    if not images or {p.name for p in files} != {n for p in images for n in (p.name, p.name+'.xmp')}:
        raise ValueError('Expected image plus image.ext.xmp pairs only')
    records = {}
    for path in files:
        regular(path)
        records[path.name] = {'sha256': sha(path)}
        if path.suffix.lower() == '.xmp':
            records[path.name]['properties'] = properties(path)
    lab.mkdir(parents=True, exist_ok=False)
    for folder in ('collection', 'database', 'config'):
        (lab/folder).mkdir()
    for path in files:
        shutil.copyfile(path, lab/'collection'/path.name)
        if sha(lab/'collection'/path.name) != records[path.name]['sha256']:
            raise ValueError('Copy verification failed; incomplete lab retained')
    (lab/'config'/'digikamrc').write_text('', encoding='utf-8')
    save(lab/'baseline.json', {'format': 1, 'reference': str(export), 'files': records})
    save(lab/'observations.json', {
        'heic_preview': 'not_tested', 'sidecar_association': 'not_tested',
        'keywords': 'not_tested', 'hierarchy': 'not_tested',
        'cv_uri_visible': 'not_tested', 'sidecar_roundtrip': 'not_tested',
        'notes': ''})
    return {'photos': len(images), 'copied_files': len(files), 'gui_tested': False}


def compare(lab):
    lab = Path(lab).resolve(strict=True)
    outside_git(lab)
    collection = lab/'collection'
    if collection.is_symlink() or collection.is_junction():
        raise ValueError('Linked collection refused')
    baseline = json.loads((lab/'baseline.json').read_text(encoding='utf-8'))
    if baseline['format'] != 1:
        raise ValueError('Unsupported baseline')
    results = []
    for name, before in baseline['files'].items():
        if Path(name).name != name or '/' in name or '\\' in name:
            raise ValueError('Unsafe baseline filename')
        current = lab/'collection'/name
        reference = Path(baseline['reference'])/'files'/name
        regular(current)
        regular(reference)
        row = {'name': name, 'reference_unchanged': sha(reference) == before['sha256'],
               'bytes_unchanged': sha(current) == before['sha256']}
        if name.lower().endswith('.xmp'):
            after = properties(current)
            old = before['properties']
            row['changed_properties'] = sorted(k for k in old if old[k] != after.get(k))
            row['added_properties'] = sorted(set(after)-set(old))
        results.append(row)
    extras = sorted(p.name for p in (lab/'collection').iterdir() if p.name not in baseline['files'])
    report = {'format': 1, 'gui_success_inferred': False, 'results': results,
              'extra_collection_entries': extras,
              'all_reference_bytes_unchanged': all(r['reference_unchanged'] for r in results),
              'all_image_bytes_unchanged': all(r['bytes_unchanged'] for r in results if not r['name'].lower().endswith('.xmp')),
              'all_prior_xmp_properties_unchanged': all(not r.get('changed_properties') for r in results),
              'any_sidecar_bytes_changed': any(not r['bytes_unchanged'] for r in results if r['name'].lower().endswith('.xmp'))}
    save(lab/'comparison.json', report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    new = sub.add_parser('prepare')
    new.add_argument('--export', required=True)
    new.add_argument('--lab', required=True)
    check = sub.add_parser('compare')
    check.add_argument('--lab', required=True)
    args = parser.parse_args()
    try:
        result = prepare(args.export, args.lab) if args.command == 'prepare' else compare(args.lab)
    except (OSError, ValueError, ET.ParseError) as error:
        parser.exit(1, f'Laboratory refused: {error}\n')
    # Detailed metadata and paths remain exclusively in the private report.
    print(json.dumps({k: v for k, v in result.items() if k != 'results'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
