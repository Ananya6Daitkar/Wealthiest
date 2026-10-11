"""Frozen-build evaluation of assessor-provided document pairs. No independence claim."""
import argparse
import hashlib
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = {'same', 'separate', 'historical', 'update', 'conflict', 'review', 'blocked'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def fingerprint():
    paths = sorted(p for folder in ('nestproof', 'static') for p in (ROOT / folder).rglob('*') if p.is_file() and p.suffix in ('.py', '.js', '.css', '.html'))
    paths += [ROOT / 'requirements.lock.txt', Path(__file__)]
    return {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in paths}

def write_new(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2); f.write('\n')

def freeze(path):
    result = {'created_at': datetime.now(timezone.utc).isoformat(), 'files': fingerprint(),
              'packages': {p: importlib.metadata.version(p) for p in ('pypdf', 'scikit-learn', 'numpy')},
              'notice': 'Build fingerprint, not proof of independent authorship or pre-registration.'}
    write_new(path, result)

def contained_file(root, name):
    p = (root / name).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file():
        raise ValueError('Document must exist inside the manifest directory')
    if p.stat().st_size > 3 * 1024 * 1024:
        raise ValueError('Document exceeds 3 MB')
    return p

def evaluate(manifest_path, freeze_path):
    from nestproof.engine import parse_document, reconcile, FIELD_NAMES, normalize
    manifest_path = Path(manifest_path)
    frozen = json.loads(Path(freeze_path).read_text())
    if frozen['files'] != fingerprint():
        raise ValueError('Build changed since freeze. Preserve this run; explicitly freeze a new version.')
    packages = {p: importlib.metadata.version(p) for p in frozen['packages']}
    if packages != frozen['packages']:
        raise ValueError('Runtime package versions changed since freeze')
    raw = manifest_path.read_bytes(); manifest = json.loads(raw)
    cases = manifest.get('cases', [])
    if not cases or len(cases) > 500:
        raise ValueError('Supply between 1 and 500 cases')
    ids = set(); prepared = []
    for case in cases:
        if not isinstance(case.get('id'), str) or not case['id'] or case['id'] in ids:
            raise ValueError('Case IDs must be unique nonempty strings')
        ids.add(case['id'])
        if case.get('relation') not in RELATIONS | {'unsupported'}:
            raise ValueError('Invalid gold relation')
        sources = {}
        for side in ('left', 'right'):
            item = case[side]; path = contained_file(manifest_path.parent, item['file'])
            gold = item.get('facts', {})
            if not isinstance(gold, dict): raise ValueError('Gold facts must be an object')
            if set(gold) - set(FIELD_NAMES): raise ValueError('Unknown gold field')
            # Gold values use the same published canonical formats, not model predictions.
            normalized = {f: normalize(f, v) if v is not None else None for f, v in gold.items()}
            content = path.read_bytes()
            sources[side] = (path.name, content, normalized)
        prepared.append((case, sources))
    report = {'generated_at': datetime.now(timezone.utc).isoformat(), 'manifest_sha256': digest(raw),
              'freeze_sha256': digest(Path(freeze_path).read_bytes()),
              'authorship': manifest.get('authorship', 'not supplied'),
              'status': 'Assessor-supplied cases; independence is an external process, not verified by this runner.',
              'n': len(cases), 'methods': []}
    for method in ('exact', 'fuzzy', 'ml'):
        rows = []
        for case, sources in prepared:
            parsed = {}; errors = []; field_correct = field_n = unexpected = 0
            for side, (name, content, gold) in sources.items():
                try: parsed[side] = parse_document(content, name, method)
                except Exception as exc:
                    # Parser failures stay in the denominator. Do not export source text.
                    errors.append({'side': side, 'type': type(exc).__name__})
                    parsed[side] = {'facts': {}}
                for field, expected in gold.items():
                    field_n += 1
                    field_correct += not any(e['side'] == side for e in errors) and parsed[side]['facts'].get(field) == expected
                    unexpected += expected is None and field in parsed[side]['facts']
            pred = 'unsupported' if errors else reconcile(parsed['left'], parsed['right'])['relation']
            rows.append({'id': case['id'], 'gold': case['relation'], 'prediction': pred,
                         'parser_errors': errors, 'correct_annotated_fields': field_correct,
                         'annotated_fields': field_n, 'unexpected_annotated_fields': unexpected,
                         'source_sha256': {side: digest(data[1]) for side, data in sources.items()}})
        same = sum(r['prediction'] == 'same' for r in rows)
        false_same = sum(r['prediction'] == 'same' and r['gold'] != 'same' for r in rows)
        fields = sum(r['annotated_fields'] for r in rows)
        report['methods'].append({'method': method, 'correct_relations': sum(r['gold'] == r['prediction'] for r in rows),
                                 'same_decisions': same, 'false_same': false_same,
                                 'same_precision': (same-false_same)/same if same else None,
                                 'review_or_blocked': sum(r['prediction'] in ('review', 'blocked') for r in rows),
                                 'parser_failures': sum(bool(r['parser_errors']) for r in rows),
                                 'annotated_field_accuracy': sum(r['correct_annotated_fields'] for r in rows)/fields if fields else None,
                                 'annotated_fields': fields, 'rows': rows})
    report['limitations'] = 'Pairwise extraction/reconciliation only; not live API authorization, user impact, document authenticity or production safety. Field accuracy covers only supplied annotations. Unsupported includes any parser exception; inspect failure types. Small samples and related templates limit generalization.'
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    a = sub.add_parser('freeze'); a.add_argument('--out', required=True)
    a = sub.add_parser('run'); a.add_argument('--manifest', required=True); a.add_argument('--freeze', required=True); a.add_argument('--out', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'freeze': freeze(args.out)
        else: write_new(args.out, evaluate(args.manifest, args.freeze))
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(2, f'Validation failed: {exc}\n')
    print('Saved new artifact:', args.out)

if __name__ == '__main__': main()
