"""Local supervised label interpretation; source-bound values; deterministic decisions."""
from __future__ import annotations

import hashlib
import io
import json
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from difflib import SequenceMatcher
from functools import lru_cache

import numpy as np
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from .labels import TRAIN, CALIBRATION

CRITICAL = ('owner_id', 'account_id', 'institution', 'as_of', 'principal', 'currency')
IDENTITY = ('owner_id', 'account_id', 'institution')
FIELD_NAMES = {'owner_id': 'holder reference', 'account_id': 'deposit reference',
               'institution': 'issuing institution', 'as_of': 'statement date',
               'principal': 'principal amount', 'currency': 'currency',
               'maturity_value': 'maturity proceeds', 'maturity_date': 'maturity date'}
INJECTION = re.compile(r'ignore\s+(?:all\s+)?(?:previous|prior|system)|(?:send|upload|post|export).{0,50}https?://|override.{0,20}(?:rules|instructions)', re.I)


def clean_label(value):
    return ' '.join(re.sub(r'[^a-z0-9 ]', ' ', value.lower()).split())


@lru_cache(maxsize=1)
def model():
    x, y = [], []
    for kind, labels in TRAIN.items():
        for label in labels:
            x.append(clean_label(label)); y.append(kind)
    pipeline = Pipeline([
        ('features', FeatureUnion([
            ('word', TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
            ('char', TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 5), sublinear_tf=True)),
        ])),
        ('classifier', LogisticRegression(C=12, max_iter=1000, random_state=42)),
    ])
    pipeline.fit(x, y)
    cx = [clean_label(s) for values in CALIBRATION.values() for s in values]
    cy = [k for k, values in CALIBRATION.items() for _ in values]
    p = pipeline.predict_proba(cx)
    classes = pipeline.classes_
    # Choose threshold on calibration only. Financial field errors cost much more
    # than review; correct rejection of irrelevant labels has zero cost.
    trials = []
    for threshold in np.arange(.30, .86, .025):
        cost = accepted = wrong = 0
        for truth, probs in zip(cy, p):
            best = int(np.argmax(probs)); pred = classes[best]
            emit = pred != 'ignore' and float(probs[best]) >= threshold
            if emit:
                accepted += 1
                wrong += int(pred != truth)
                cost += 12 * int(pred != truth)
            elif truth != 'ignore':
                cost += 1
        trials.append((cost, -accepted, float(threshold), wrong))
    selected = min(trials)
    manifest = {'name': 'TF-IDF word/character + logistic regression',
        'training_labels': len(x), 'calibration_labels': len(cx),
        'threshold': round(selected[2], 3), 'calibration_wrong_accepted': selected[3],
        'training_sha256': hashlib.sha256(json.dumps(TRAIN, sort_keys=True).encode()).hexdigest(),
        'calibration_sha256': hashlib.sha256(json.dumps(CALIBRATION, sort_keys=True).encode()).hexdigest(),
        'confidence_note': 'Classifier score is not financial correctness probability.'}
    return pipeline, manifest


# Conservative FD-only domain exclusions, shared by every method. These are
# development-set fixes, not new evidence of model generalization.
EXCLUDED_ROLE = re.compile(r'\b(?:loan|credit|tax|interest|nominee|aggregate|total)\b', re.I)


@lru_cache(maxsize=1)
def fuzzy_threshold():
    dictionary = {clean_label(s): k for k, labels in TRAIN.items() for s in labels}
    trials = []
    examples = []
    for truth, labels in CALIBRATION.items():
        for label in labels:
            value = clean_label(label)
            candidate = max(dictionary, key=lambda s: SequenceMatcher(None, value, s).ratio())
            examples.append((truth, dictionary[candidate], SequenceMatcher(None, value, candidate).ratio(), bool(EXCLUDED_ROLE.search(value))))
    for threshold in np.arange(.30, .96, .025):
        cost = accepted = 0
        for truth, pred, score, excluded in examples:
            emit = not excluded and pred != 'ignore' and score >= threshold
            if emit:
                accepted += 1
                cost += 12 * int(pred != truth)
            elif truth != 'ignore':
                cost += 1
        trials.append((cost, -accepted, float(threshold)))
    return round(min(trials)[2], 3)


def classify(label, method='ml'):
    value = clean_label(label)
    if EXCLUDED_ROLE.search(value):
        return 'ignore', 0.0
    # A compositional role constraint shared by all methods: invested/deposited
    # capital is principal, except when qualified as future/maturity/redemption.
    words = set(value.split())
    if words & {'currency', 'denomination'}:
        return 'currency', 1.0
    if words & {'maturity', 'expiry'} and words & {'value', 'amount', 'proceeds', 'payout', 'sum'} and not words & {'date', 'day'}:
        return 'maturity_value', 1.0
    if 'capital' in words and words & {'invested', 'deposited', 'initial', 'original'} and not words & {'future', 'maturity', 'redemption', 'projected', 'expiry'}:
        return 'principal', 1.0
    dictionary = {clean_label(s): k for k, labels in TRAIN.items() for s in labels}
    if method == 'exact':
        return dictionary.get(value, 'ignore'), 1.0 if value in dictionary else 0.0
    if method == 'fuzzy':
        candidate = max(dictionary, key=lambda s: SequenceMatcher(None, value, s).ratio())
        score = SequenceMatcher(None, value, candidate).ratio()
        return (dictionary[candidate] if score >= fuzzy_threshold() else 'ignore'), score
    pipeline, info = model()
    probs = pipeline.predict_proba([value])[0]
    best = int(np.argmax(probs))
    return (str(pipeline.classes_[best]) if probs[best] >= info['threshold'] else 'ignore'), float(probs[best])


def normalize(field, value):
    value = str(value).strip()
    if not value or value.lower() in ('unknown', 'not supplied', 'n/a', 'missing', '-'):
        raise ValueError('Not supplied')
    if field in IDENTITY:
        if '*' in value or '•' in value or re.search(r'\bxx', value, re.I):
            raise ValueError('Masked identity cannot establish a match')
        if len(value) < 3 or len(value) > 80 or not re.fullmatch(r'[A-Za-z0-9 _./-]+', value):
            raise ValueError('Invalid reference')
        return re.sub(r'\s+', ' ', value).upper()
    if field in ('as_of', 'maturity_date'):
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d %b %Y', '%d %B %Y'):
            try:
                return datetime.strptime(value, fmt).date().isoformat()
            except ValueError:
                pass
        raise ValueError('Use an unambiguous supported date')
    if field in ('principal', 'maturity_value'):
        value = re.sub(r'^(?:INR|Rs\.?|₹)\s*', '', value, flags=re.I).strip()
        if not re.fullmatch(r'(?:\d+|\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})*,\d{3})(?:\.\d{1,2})?', value):
            raise ValueError('Invalid INR amount')
        try:
            number = Decimal(value.replace(',', ''))
        except InvalidOperation as exc:
            raise ValueError('Invalid amount') from exc
        if not number.is_finite() or not Decimal('0') <= number <= Decimal('100000000000'):
            raise ValueError('Amount outside supported range')
        return format(number.quantize(Decimal('.01')), 'f')
    if field == 'currency':
        if value.upper() not in ('INR', 'RUPEES', 'INDIAN RUPEES', '₹'):
            raise ValueError('Only INR is supported')
        return 'INR'
    raise ValueError('Unsupported field')


def parse_document(content: bytes, filename: str, method='ml'):
    if len(content) > 3 * 1024 * 1024:
        raise ValueError('Maximum document size is 3 MB')
    if filename.lower().endswith('.pdf'):
        if not content.startswith(b'%PDF'):
            raise ValueError('The file is not a PDF')
        try:
            reader = PdfReader(io.BytesIO(content), strict=False)
            if reader.is_encrypted:
                raise ValueError('Encrypted PDFs are not supported; provide a synthetic unlocked file')
            if len(reader.pages) > 10:
                raise ValueError('Maximum 10 pages per document')
            pages = [p.extract_text() or '' for p in reader.pages]
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError('Unable to read PDF') from exc
    elif filename.lower().endswith('.txt'):
        try:
            pages = [content.decode('utf-8')]
        except UnicodeDecodeError as exc:
            raise ValueError('Text files must be UTF-8') from exc
    else:
        raise ValueError('Upload a digital PDF or UTF-8 .txt file')
    if sum(len(p.strip()) for p in pages) < 15:
        raise ValueError('No readable text. Scanned PDFs require OCR, which this prototype does not support.')
    if sum(len(p) for p in pages) > 100000:
        raise ValueError('Too much extracted text')
    evidence, candidates, flags = [], {}, []
    for page_no, page in enumerate(pages, 1):
        for line_no, raw in enumerate(page.splitlines(), 1):
            raw = raw.strip()
            if not raw:
                continue
            eid = f'p{page_no}:l{line_no}'
            item = {'id': eid, 'page': page_no, 'line': line_no, 'text': raw,
                    'field': None, 'value': None, 'status': 'context'}
            if INJECTION.search(raw):
                flags.append({'code': 'untrusted_instruction', 'evidence_id': eid,
                              'message': 'Document contains instruction-like text; import quarantined.'})
                item['status'] = 'quarantined'
            label, sep, val = raw.partition(':')
            if sep and len(label) <= 90 and item['status'] != 'quarantined':
                field, score = classify(label, method)
                item.update(label=label, model_score=round(score, 4))
                if field != 'ignore':
                    item['field'] = field
                    try:
                        item['value'] = normalize(field, val)
                        item['status'] = 'extracted'
                        candidates.setdefault(field, []).append(item)
                    except ValueError as exc:
                        item['status'] = 'unresolved'
                        item['reason'] = str(exc)
            evidence.append(item)
    facts, sources = {}, {}
    for field, items in candidates.items():
        values = {i['value'] for i in items}
        if len(values) == 1:
            facts[field] = items[0]['value']
            sources[field] = [i['id'] for i in items]
        else:
            flags.append({'code': 'conflicting_field', 'field': field,
                          'message': f'Multiple incompatible values for {FIELD_NAMES[field]}.'})
    if 'principal' in facts and 'maturity_value' in facts and Decimal(facts['maturity_value']) < Decimal(facts['principal']):
        flags.append({'code': 'amount_inconsistency', 'message': 'Maturity proceeds below principal require review.'})
    return {'facts': facts, 'sources': sources, 'evidence': evidence, 'flags': flags,
            'pages': len(pages), 'missing': [f for f in CRITICAL if f not in facts],
            'method': method, 'hash': hashlib.sha256(content).hexdigest()}


def reconcile(left, right):
    """Inputs are extracted records with provenance; values are never generated."""
    a, b = left['facts'], right['facts']
    if left.get('flags') or right.get('flags'):
        return {'relation': 'blocked', 'title': 'Source needs attention',
                'reason': 'A document has conflicting or instruction-like content. No correction can be committed.', 'missing': []}
    missing = [{'side': side, 'field': f} for side, obj in [('left', a), ('right', b)] for f in CRITICAL if not obj.get(f)]
    if missing:
        return {'relation': 'review', 'title': 'One piece of evidence at a time',
                'reason': 'Identity, valuation basis and date must be established before a supported decision.', 'missing': missing}
    different = [f for f in IDENTITY if a[f] != b[f]]
    if different:
        return {'relation': 'separate', 'title': 'A separate deposit',
                'reason': 'Different ' + ', '.join(FIELD_NAMES[f] for f in different) + '. Similar amounts do not establish identity.', 'missing': []}
    if a['as_of'] != b['as_of']:
        newer = b['as_of'] > a['as_of']
        return {'relation': 'update' if newer else 'historical',
                'title': 'A newer observation' if newer else 'An earlier observation',
                'reason': 'Same deposit, different effective dates. Preserve both observations without adding the deposit twice.', 'missing': []}
    maturity_conflicts = [f for f in ('maturity_value', 'maturity_date')
                          if a.get(f) is not None and b.get(f) is not None and a[f] != b[f]]
    if maturity_conflicts:
        return {'relation': 'conflict', 'title': 'Maturity evidence disagrees',
                'reason': 'Same deposit and statement date, but different ' + ', '.join(FIELD_NAMES[f] for f in maturity_conflicts) + '. Review the complete observation explicitly.',
                'missing': []}
    if Decimal(a['principal']) != Decimal(b['principal']):
        return {'relation': 'conflict', 'title': 'Two values for the same date',
                'reason': 'The deposit identity and effective date agree, but principal amounts disagree. A user decision is required.', 'missing': []}
    return {'relation': 'same', 'title': 'Same deposit, already represented',
            'reason': 'Holder, deposit, institution, date and principal agree. Link the evidence without adding its value again.', 'missing': []}


def question(result, answers=0):
    if answers >= 2:
        return None
    if result['relation'] == 'conflict':
        return {'field': 'value_choice', 'side': 'right', 'label': 'Which dated observation should the ledger represent?',
                'reason': 'This is a user-reviewed choice, not independent proof of financial correctness.',
                'type': 'choice', 'choices': ['keep_existing', 'use_incoming']}
    if not result.get('missing'):
        return None
    priority = {'account_id': 0, 'owner_id': 1, 'institution': 2, 'as_of': 3, 'principal': 4, 'currency': 5}
    pick = min(result['missing'], key=lambda m: (priority[m['field']], m['side'] != 'right'))
    f = pick['field']
    return {**pick, 'label': f'Confirm the {FIELD_NAMES[f]} on the {"incoming" if pick["side"] == "right" else "existing"} document',
            'reason': 'Supply only this missing field from your source. It will be labeled user-supplied, not institution-verified.',
            'type': 'text', 'placeholder': {'as_of': 'YYYY-MM-DD', 'principal': 'Amount in INR', 'currency': 'INR'}.get(f, 'Full reference from your document')}


def position_key(facts):
    return '|'.join(facts[f] for f in IDENTITY)


def select_match_field(facts, missing):
    """Deterministic candidate discrimination, not a learned question policy."""
    if not facts or not missing:
        return None
    return max(missing, key=lambda f: len({o.get(f) for o in facts}))
