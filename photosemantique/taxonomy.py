"""Local consultation of attributed controlled-vocabulary snapshots."""
# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
import argparse
import json
from pathlib import Path
import unicodedata

DATA = Path(__file__).parent / 'taxonomies'


def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text.casefold())
                   if not unicodedata.combining(c))


def validate_concepts(concepts, closed=True):
    index = {c['uri']: c for c in concepts}
    if len(index) != len(concepts):
        raise ValueError('Duplicate concept URI')
    for c in concepts:
        if not c['labels'] or not c['uri'].startswith(('http://cv.iptc.org/newscodes/mediatopic/', 'http://vocab.getty.edu/aat/')):
            raise ValueError('Missing labels or unexpected source URI')
        if closed and any(p not in index for p in c['broader']):
            raise ValueError('Unknown parent')
    visiting, visited = set(), set()
    def visit(uri):
        if uri in visiting:
            raise ValueError('Hierarchy cycle')
        if uri in visited:
            return
        visiting.add(uri)
        for parent in index[uri]['broader']:
            if parent in index:
                visit(parent)
        visiting.remove(uri)
        visited.add(uri)
    for uri in index:
        visit(uri)
    return index


def search(query, include_retired=False, source='iptc'):
    data = json.loads((DATA / (source + '.json')).read_text(encoding='utf-8'))
    needle = normalize(query)
    return [c for c in data['concepts'] if (include_retired or not c.get('retired'))
            and needle in normalize(' '.join([c['uri'], *c['labels'].values(), c.get('editorial_label_fr',''), *c.get('aliases', [])]))]


def main(argv=None):
    parser = argparse.ArgumentParser(description='GNU APMG vocabulary lookup; no photo tagging')
    parser.add_argument('query')
    parser.add_argument('--source', choices=['iptc', 'getty'], default='iptc')
    parser.add_argument('--include-retired', action='store_true')
    args = parser.parse_args(argv)
    print(json.dumps(search(args.query, args.include_retired, args.source), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
