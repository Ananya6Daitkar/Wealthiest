from __future__ import annotations

import hashlib
import json
import os
import secrets
import sqlite3
import time
from contextlib import contextmanager
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

from fastapi import FastAPI, Depends, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from .engine import CRITICAL, FIELD_NAMES, model, normalize, parse_document, position_key, question, reconcile
from .fixtures import pdf_bytes, scenarios

ROOT = Path(__file__).resolve().parents[1]
MATURITY_STATUSES = {'maturing_soon', 'upcoming', 'matured', 'date_unavailable'}


def maturity_details(maturity_date, today=None):
    today = today or date.today()
    try:
        due = date.fromisoformat(maturity_date)
    except (TypeError, ValueError):
        return {'days_remaining': None, 'maturity_status': 'date_unavailable'}
    days_remaining = (due - today).days
    if days_remaining < 0:
        status = 'matured'
    elif days_remaining <= 30:
        status = 'maturing_soon'
    else:
        status = 'upcoming'
    return {'days_remaining': days_remaining, 'maturity_status': status}


def encode(value):
    return json.dumps(value, sort_keys=True)


def now():
    return datetime.now(timezone.utc).isoformat()


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Login(StrictModel):
    persona: str


class MatchAnswer(StrictModel):
    field: str
    value: str = Field(min_length=1, max_length=100)
    note: str = Field(min_length=5, max_length=500)
    revision: int


class Compare(StrictModel):
    right_id: str
    clarification: MatchAnswer | None = None


class Clarify(StrictModel):
    value: str = Field(min_length=1, max_length=100)
    note: str = Field(min_length=5, max_length=500)
    version: int


class Commit(StrictModel):
    preview_id: str


def create_app(db_path=None):
    path = Path(db_path or os.environ.get('NESTPROOF_DB', ROOT / '.runtime/nestproof.db'))
    path.parent.mkdir(parents=True, exist_ok=True)
    app = FastAPI(title='NestProof', version='0.1.0', docs_url='/api/docs')

    @contextmanager
    def db(write=False):
        connection = sqlite3.connect(path, timeout=15)
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys = ON')
        try:
            if write:
                connection.execute('BEGIN IMMEDIATE')
            yield connection
            connection.commit()
        except Exception:
            connection.rollback(); raise
        finally:
            connection.close()

    with db() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS sessions(token_hash TEXT PRIMARY KEY, persona TEXT, csrf TEXT, expires REAL);
        CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY, name TEXT, owner TEXT, scope TEXT, extracted TEXT, content BLOB, hash TEXT, created TEXT, scenario TEXT, revoked INTEGER DEFAULT 0, UNIQUE(scope,hash));
        CREATE TABLE IF NOT EXISTS ledger(scope TEXT PRIMARY KEY, revision INTEGER, state TEXT);
        CREATE TABLE IF NOT EXISTS comparisons(id TEXT PRIMARY KEY, actor TEXT, left_id TEXT REFERENCES documents(id), right_id TEXT REFERENCES documents(id), scope TEXT, answers TEXT, version INTEGER, created TEXT, left_facts TEXT, ledger_revision INTEGER);
        CREATE TABLE IF NOT EXISTS previews(id TEXT PRIMARY KEY, comparison_id TEXT, actor TEXT, scope TEXT, revision INTEGER, comparison_version INTEGER, before_state TEXT, after_state TEXT, effect TEXT, used INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT, scope TEXT, revision INTEGER, action TEXT, actor TEXT, comparison_id TEXT, before_state TEXT, after_state TEXT, detail TEXT, created TEXT);
        ''')
        for scope in ('family', 'ananya', 'ravi'):
            c.execute('INSERT OR IGNORE INTO ledger VALUES(?,0,?)', (scope, '{}'))
        comparison_columns = {row['name'] for row in c.execute('PRAGMA table_info(comparisons)')}
        if 'left_facts' not in comparison_columns:
            c.execute('ALTER TABLE comparisons ADD COLUMN left_facts TEXT')
        if 'ledger_revision' not in comparison_columns:
            c.execute('ALTER TABLE comparisons ADD COLUMN ledger_revision INTEGER')

    @app.middleware('http')
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'"
        if request.url.path.startswith('/api'):
            response.headers['Cache-Control'] = 'no-store'
        return response

    def session(request: Request):
        token = request.cookies.get('nestproof_session', '')
        with db() as c:
            row = c.execute('SELECT * FROM sessions WHERE token_hash=? AND expires>?', (hashlib.sha256(token.encode()).hexdigest(), time.time())).fetchone()
        if not row:
            raise HTTPException(401, 'Choose a synthetic demo persona to begin')
        if request.method not in ('GET', 'HEAD'):
            if not secrets.compare_digest(request.headers.get('X-NestProof-CSRF', ''), row['csrf']):
                raise HTTPException(403, 'Invalid session request token')
        return dict(row)

    def document(c, doc_id, actor):
        row = c.execute('SELECT * FROM documents WHERE id=? AND revoked=0 AND scope IN (?,?)', (doc_id, 'family', actor)).fetchone()
        if not row:
            raise HTTPException(404, 'Document not available')
        return dict(row)

    def public_doc(row, full=False):
        ext = json.loads(row['extracted'])
        result = {k: row[k] for k in ('id', 'name', 'scope', 'owner', 'created', 'scenario')}
        result.update(facts=ext['facts'], missing=ext['missing'], flags=ext['flags'], pages=ext['pages'])
        if full:
            result.update(evidence=ext['evidence'], sources=ext['sources'], hash=ext['hash'])
        return result

    def store_doc(c, content, name, actor, scope, scenario='upload'):
        ext = parse_document(content, name)
        existing = c.execute('SELECT * FROM documents WHERE scope=? AND hash=?', (scope, ext['hash'])).fetchone()
        if existing:
            if existing['revoked']:
                raise HTTPException(409, 'This document was revoked; it cannot be silently restored by re-upload')
            return dict(existing), False
        did = secrets.token_hex(12)
        c.execute('INSERT INTO documents(id,name,owner,scope,extracted,content,hash,created,scenario) VALUES(?,?,?,?,?,?,?,?,?)',
                  (did, name, actor, scope, encode(ext), content, ext['hash'], now(), scenario))
        return dict(c.execute('SELECT * FROM documents WHERE id=?', (did,)).fetchone()), True

    def seed_workspace(c, only_if_empty=False):
        exists = c.execute("SELECT 1 FROM documents WHERE scenario='baseline'").fetchone()
        if exists:
            return False
        if only_if_empty:
            has_documents = c.execute('SELECT 1 FROM documents LIMIT 1').fetchone()
            has_events = c.execute('SELECT 1 FROM events LIMIT 1').fetchone()
            has_ledger_state = c.execute("SELECT 1 FROM ledger WHERE revision != 0 OR state != '{}' LIMIT 1").fetchone()
            if has_documents or has_events or has_ledger_state:
                return False
        for title, lines, scope, owner, scenario in scenarios():
            row, _ = store_doc(c, pdf_bytes(title, lines), title + '.pdf', owner, scope, scenario)
            if scenario in ('baseline', 'private'):
                parsed = json.loads(row['extracted'])
                if parsed['missing'] or parsed['flags']:
                    raise HTTPException(500, 'Synthetic fixture did not parse; do not seed a fabricated result')
                key = position_key(parsed['facts'])
                state = {key: {'observations': [{'facts': parsed['facts'], 'source_ids': [row['id']],
                        'recorded_at': now(), 'provenance': 'Synthetic starting ledger'}]}}
                c.execute('UPDATE ledger SET state=?,revision=1 WHERE scope=?', (encode(state), scope))
                c.execute('INSERT INTO events(scope,revision,action,actor,before_state,after_state,detail,created) VALUES(?,?,?,?,?,?,?,?)',
                          (scope, 1, 'seed', owner, '{}', encode(state), 'Loaded synthetic starting position', now()))
        return True

    def comparison(c, cid, actor):
        row = c.execute('SELECT * FROM comparisons WHERE id=? AND actor=?', (cid, actor)).fetchone()
        if not row:
            raise HTTPException(404, 'Review not available')
        left = document(c, row['left_id'], actor)
        right = document(c, row['right_id'], actor)
        a, b = json.loads(left['extracted']), json.loads(right['extracted'])
        if row['left_facts']:
            a['facts'] = json.loads(row['left_facts'])
        answers = json.loads(row['answers'])
        for answer in answers:
            if answer['field'] != 'value_choice':
                target = a if answer['side'] == 'left' else b
                target['facts'][answer['field']] = answer['value']
        result = reconcile(a, b)
        choice = next((i['value'] for i in answers if i['field'] == 'value_choice'), None)
        if result['relation'] == 'conflict' and choice:
            result.update(relation='keep' if choice == 'keep_existing' else 'correction',
                          title='Keep the existing observation' if choice == 'keep_existing' else 'A user-reviewed correction',
                          reason='Explicit user choice recorded. This is not independent verification of the institution record.')
        return dict(row), left, right, a, b, result, answers

    def view_comparison(c, cid, actor):
        row, left, right, a, b, result, answers = comparison(c, cid, actor)
        return {'id': cid, 'version': row['version'], 'left': public_doc(left, True), 'right': public_doc(right, True),
                'interpreted_left': a['facts'], 'interpreted_right': b['facts'], 'result': result,
                'question': question(result, len(answers)), 'answers': answers,
                'can_preview': result['relation'] not in ('review', 'blocked', 'conflict')}

    def allowed_state(c, state, actor):
        filtered = {}
        for key, value in state.items():
            observations = []
            for obs in value['observations']:
                try:
                    for did in obs['source_ids']:
                        document(c, did, actor)
                    observations.append(obs)
                except HTTPException:
                    pass
            if observations:
                filtered[key] = {'observations': observations}
        return filtered

    def ledger_candidates(c, doc, actor, overrides=None):
        incoming = json.loads(doc['extracted'])['facts'] | (overrides or {})
        known = {field: incoming[field] for field in ('owner_id', 'account_id', 'institution') if incoming.get(field)}
        ledger = c.execute('SELECT revision,state FROM ledger WHERE scope=?', (doc['scope'],)).fetchone()
        state = allowed_state(c, json.loads(ledger['state']), actor)
        candidates = []
        for key, value in state.items():
            observations = value['observations']
            current = max(enumerate(observations), key=lambda item: (item[1]['facts']['as_of'], item[0]))[1]
            facts = current['facts']
            if all(facts.get(field) == value for field, value in known.items()):
                candidates.append((key, current))

        if len(candidates) == 1:
            return 'matched', candidates[0], ledger['revision']
        if len(candidates) > 1:
            return 'unresolved', candidates, ledger['revision']
        if len(known) == len(('owner_id', 'account_id', 'institution')) or not state:
            return 'new', None, ledger['revision']
        return 'unresolved', [], ledger['revision']

    def match_question(doc, candidates):
        ext = json.loads(doc['extracted'])
        if ext['flags']:
            return None
        missing = [f for f in ('account_id', 'owner_id', 'institution') if not ext['facts'].get(f)]
        if not missing or len(candidates) < 2:
            return None
        # Ask for the missing identity field that best separates the candidates.
        field = max(missing, key=lambda f: len({o['facts'][f] for _, o in candidates}))
        return {'field': field, 'label': 'Confirm the ' + FIELD_NAMES[field] + ' from the original source',
                'reason': 'This missing field best distinguishes the accepted deposits. Your answer is recorded as user-supplied evidence.'}

    def summarize(state, effective=None):
        rows, total = [], Decimal('0')
        for key, value in state.items():
            eligible = [o for o in value['observations'] if not effective or o['facts']['as_of'] <= effective]
            if not eligible:
                continue
            latest = max(enumerate(eligible), key=lambda t: (t[1]['facts']['as_of'], t[0]))[1]
            total += Decimal(latest['facts']['principal'])
            rows.append({'key': key, **latest['facts'], 'source_ids': latest['source_ids'],
                         'recorded_at': latest['recorded_at'], 'provenance': latest['provenance']})
        return {'total': format(total, '.2f'), 'positions': rows, 'basis': 'Recorded INR deposit principal; not current net worth'}

    @app.get('/api/health')
    def health():
        return {'status': 'ok', 'model': model()[1], 'mode': 'local synthetic prototype'}

    @app.post('/api/session')
    def login(body: Login, request: Request, response: Response):
        if body.persona not in ('ananya', 'ravi'):
            raise HTTPException(400, 'Unknown demo persona')
        origin = request.headers.get('origin')
        if origin and origin != str(request.base_url).rstrip('/'):
            raise HTTPException(403, 'Cross-origin session creation denied')
        token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(24)
        with db(True) as c:
            c.execute('DELETE FROM sessions WHERE expires<?', (time.time(),))
            c.execute('INSERT INTO sessions VALUES(?,?,?,?)', (hashlib.sha256(token.encode()).hexdigest(), body.persona, csrf, time.time() + 28800))
        response.set_cookie('nestproof_session', token, httponly=True, samesite='strict', max_age=28800)
        return {'persona': body.persona, 'csrf': csrf, 'notice': 'Synthetic persona switch, not production authentication'}

    @app.get('/api/session')
    def get_session(user=Depends(session)):
        return {'persona': user['persona'], 'csrf': user['csrf']}

    @app.post('/api/demo')
    def seed(user=Depends(session)):
        with db(True) as c:
            # Explicit seeding remains idempotent and never resets existing work.
            created = seed_workspace(c, only_if_empty=True)
        return {'created': created}

    @app.get('/api/documents')
    def documents(user=Depends(session)):
        with db() as c:
            rows = c.execute('SELECT * FROM documents WHERE revoked=0 AND scope IN (?,?) ORDER BY created', ('family', user['persona'])).fetchall()
            return [public_doc(dict(row)) for row in rows]

    @app.post('/api/documents')
    async def upload(file: UploadFile = File(...), visibility: str = Form('private'), user=Depends(session)):
        if visibility not in ('private', 'family'):
            raise HTTPException(400, 'Choose private or family visibility')
        content = await file.read(3 * 1024 * 1024 + 1)
        name = Path(file.filename or 'document.txt').name[:160]
        try:
            with db(True) as c:
                row, created = store_doc(c, content, name, user['persona'], 'family' if visibility == 'family' else user['persona'])
                return {'document': public_doc(row, True), 'created': created}
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.get('/api/documents/{did}')
    def get_document(did: str, user=Depends(session)):
        with db() as c:
            return public_doc(document(c, did, user['persona']), True)

    @app.get('/api/documents/{did}/source')
    def get_source(did: str, user=Depends(session)):
        with db() as c:
            row = document(c, did, user['persona'])
            mime = 'application/pdf' if row['content'].startswith(b'%PDF') else 'text/plain; charset=utf-8'
            return Response(row['content'], media_type=mime, headers={'Content-Disposition': 'attachment; filename="synthetic-source' + ('.pdf"' if mime == 'application/pdf' else '.txt"')})

    @app.post('/api/documents/{did}/revoke')
    def revoke(did: str, user=Depends(session)):
        with db(True) as c:
            row = document(c, did, user['persona'])
            if row['owner'] != user['persona']:
                raise HTTPException(403, 'Only the document owner can revoke it')
            c.execute('UPDATE documents SET revoked=1 WHERE id=?', (did,))
            ledger = c.execute('SELECT * FROM ledger WHERE scope=?', (row['scope'],)).fetchone()
            revision = ledger['revision'] + 1
            c.execute('UPDATE ledger SET revision=? WHERE scope=?', (revision, row['scope']))
            c.execute('INSERT INTO events(scope,revision,action,actor,before_state,after_state,detail,created) VALUES(?,?,?,?,?,?,?,?)',
                      (row['scope'], revision, 'revoke', user['persona'], ledger['state'], ledger['state'], 'Owner revoked a source; current permissions also apply to historical views', now()))
        return {'revoked': True}

    @app.post('/api/documents/{did}/preview')
    def preview_first(did: str, user=Depends(session)):
        with db(True) as c:
            doc = document(c, did, user['persona'])
            ext = json.loads(doc['extracted'])
            if ext['missing'] or ext['flags']:
                raise HTTPException(409, 'A first observation needs complete, unflagged source evidence')
            ledger = c.execute('SELECT * FROM ledger WHERE scope=?', (doc['scope'],)).fetchone()
            before = json.loads(ledger['state']); after = json.loads(ledger['state'])
            key = position_key(ext['facts'])
            if key in after:
                raise HTTPException(409, 'This deposit already has observations. Compare with an accepted source.')
            after[key] = {'observations': [{'facts': ext['facts'], 'source_ids': [did], 'recorded_at': now(), 'provenance': 'document evidence'}]}
            old, new = summarize(before), summarize(after)
            effect = {'relation': 'initial', 'title': 'Add a first observation', 'before': old['total'], 'after': new['total'],
                      'delta': format(Decimal(new['total']) - Decimal(old['total']), '.2f'), 'basis': new['basis'],
                      'effective_date': ext['facts']['as_of'], 'user_supplied': False,
                      'notice': 'Recorded principal from the source, not money recovered or investment advice.'}
            pid = secrets.token_hex(16)
            c.execute('INSERT INTO previews(id,comparison_id,actor,scope,revision,comparison_version,before_state,after_state,effect) VALUES(?,?,?,?,?,?,?,?,?)',
                      (pid, 'document:' + did, user['persona'], doc['scope'], ledger['revision'], 0, encode(before), encode(after), encode(effect)))
            return {'id': pid, 'revision': ledger['revision'], 'effect': effect}

    @app.post('/api/comparisons')
    def compare(body: Compare, user=Depends(session)):
        with db(True) as c:
            incoming = document(c, body.right_id, user['persona'])
            match_type, match, revision = ledger_candidates(c, incoming, user['persona'])
            answers = []
            if body.clarification:
                answer = body.clarification
                if answer.revision != revision:
                    raise HTTPException(409, 'The ledger changed. Start a new review before answering.')
                q = match_question(incoming, match) if match_type == 'unresolved' else None
                if not q or answer.field != q['field']:
                    raise HTTPException(409, 'Only the currently requested missing identity field can be supplied')
                try:
                    value = normalize(answer.field, answer.value)
                except ValueError as exc:
                    raise HTTPException(422, str(exc)) from exc
                match_type, match, revision = ledger_candidates(c, incoming, user['persona'], {answer.field: value})
                if match_type != 'matched':
                    raise HTTPException(422, 'This answer does not identify one accepted deposit. Check the original reference or upload clearer evidence; nothing changed.')
                answers = [{'field': answer.field, 'side': 'right', 'value': value, 'note': answer.note,
                            'provenance': 'user-supplied', 'actor': user['persona'], 'recorded_at': now()}]
            if match_type == 'new':
                return {'kind': 'new', 'document': public_doc(incoming, True), 'ledger_revision': revision}
            if match_type == 'unresolved':
                candidates = []
                for _, observation in match:
                    candidates.append({'account_id': observation['facts'].get('account_id'),
                                       'owner_id': observation['facts'].get('owner_id'),
                                       'institution': observation['facts'].get('institution')})
                return {'kind': 'unresolved',
                        'title': 'No unique ledger match',
                        'reason': ('More than one accepted deposit matches the established identity fields.' if candidates
                                   else 'The incoming identity is incomplete and no unique accepted ledger record can be identified.'),
                        'candidates': candidates, 'ledger_revision': revision, 'right_id': incoming['id'],
                        'question': match_question(incoming, match)}
            _, observation = match
            anchor_ids = observation['source_ids']
            anchor_id = next((did for did in anchor_ids if did != incoming['id']), None)
            if not anchor_id:
                return {'kind': 'represented', 'title': 'Already represented in the ledger',
                        'reason': 'This source is already attached to the accepted ledger observation.',
                        'candidates': [], 'ledger_revision': revision}
            cid = secrets.token_hex(12)
            c.execute('''INSERT INTO comparisons
                (id,actor,left_id,right_id,scope,answers,version,created,left_facts,ledger_revision)
                VALUES(?,?,?,?,?,?,?,?,?,?)''',
                (cid, user['persona'], anchor_id, incoming['id'], incoming['scope'], encode(answers), len(answers), now(),
                 encode(observation['facts']), revision))
            result = view_comparison(c, cid, user['persona'])
            result['kind'] = 'comparison'
            return result

    @app.get('/api/comparisons/{cid}')
    def get_compare(cid: str, user=Depends(session)):
        with db() as c:
            return view_comparison(c, cid, user['persona'])

    @app.post('/api/comparisons/{cid}/clarify')
    def clarify(cid: str, body: Clarify, user=Depends(session)):
        with db(True) as c:
            row, a, b, ea, eb, result, answers = comparison(c, cid, user['persona'])
            current = c.execute('SELECT revision FROM ledger WHERE scope=?', (row['scope'],)).fetchone()
            if row['ledger_revision'] is not None and current['revision'] != row['ledger_revision']:
                raise HTTPException(409, 'The ledger changed. Start a new review against its current records.')
            if row['version'] != body.version:
                raise HTTPException(409, 'Review changed. Refresh before answering.')
            q = question(result, len(answers))
            if not q:
                raise HTTPException(409, 'No permitted clarification remains; leave unresolved or supply a new source')
            try:
                value = body.value if q['field'] == 'value_choice' else normalize(q['field'], body.value)
            except ValueError as exc:
                raise HTTPException(422, str(exc)) from exc
            if q['field'] == 'value_choice' and value not in q['choices']:
                raise HTTPException(422, 'Choose an available observation')
            answers.append({'field': q['field'], 'side': q['side'], 'value': value, 'note': body.note,
                            'provenance': 'user-supplied', 'actor': user['persona'], 'recorded_at': now()})
            c.execute('UPDATE comparisons SET answers=?,version=version+1 WHERE id=?', (encode(answers), cid))
            return view_comparison(c, cid, user['persona'])

    @app.post('/api/comparisons/{cid}/preview')
    def preview(cid: str, user=Depends(session)):
        with db(True) as c:
            row, left, right, a, b, result, answers = comparison(c, cid, user['persona'])
            if row['ledger_revision'] is not None and row['ledger_revision'] != c.execute(
                    'SELECT revision FROM ledger WHERE scope=?', (row['scope'],)).fetchone()['revision']:
                raise HTTPException(409, 'The ledger changed. Start a new review against its current records.')
            if result['relation'] in ('review', 'blocked', 'conflict'):
                raise HTTPException(409, 'Evidence is unresolved; no correction preview is available')
            ledger = c.execute('SELECT * FROM ledger WHERE scope=?', (row['scope'],)).fetchone()
            before = json.loads(ledger['state']); after = json.loads(ledger['state'])
            # Anchor must be represented with the same critical facts. Otherwise a
            # stale source could authorize replacement of a later accepted correction.
            key_a = position_key(a['facts'])
            anchor = after.get(key_a)
            if not anchor or not any(all(o['facts'].get(f) == a['facts'].get(f) for f in CRITICAL) for o in anchor['observations']):
                raise HTTPException(409, 'Existing source is not an accepted observation. Choose a current ledger source.')
            for obs in anchor['observations']:
                for did in obs['source_ids']:
                    document(c, did, user['persona'])
            key = position_key(b['facts'])
            observation = {'facts': b['facts'], 'source_ids': [right['id']], 'recorded_at': now(),
                           'provenance': 'user-supplied clarification' if answers else 'document evidence', 'clarifications': answers}
            relation_name = result['relation']
            if relation_name == 'same':
                target = next((o for o in after[key]['observations'] if all(o['facts'].get(f) == b['facts'].get(f) for f in CRITICAL)), None)
                if target is None:
                    raise HTTPException(409, 'The canonical observation changed; review again')
                target['source_ids'] = list(dict.fromkeys(target['source_ids'] + [right['id']]))
                if answers:
                    target['clarifications'] = answers
                    target['provenance'] = 'document evidence with user-supplied clarification'
            elif relation_name == 'separate':
                if key in after:
                    raise HTTPException(409, 'This deposit is already in the ledger. Compare with its accepted source.')
                after[key] = {'observations': [observation]}
            elif relation_name != 'keep':
                existing_date = [o for o in after.get(key, {}).get('observations', []) if o['facts']['as_of'] == b['facts']['as_of']]
                if existing_date and existing_date[-1]['facts']['principal'] != b['facts']['principal']:
                    if relation_name != 'correction' or existing_date[-1]['facts']['principal'] != a['facts']['principal']:
                        raise HTTPException(409, 'An accepted value already exists for this date. Compare with that source to resolve the conflict explicitly.')
                after.setdefault(key, {'observations': []})['observations'].append(observation)
            old, new = summarize(before), summarize(after)
            effect = {'relation': relation_name, 'title': result['title'], 'before': old['total'], 'after': new['total'],
                      'delta': format(Decimal(new['total']) - Decimal(old['total']), '.2f'), 'basis': new['basis'],
                      'effective_date': b['facts']['as_of'], 'user_supplied': bool(answers),
                      'notice': 'A represented principal correction, not money recovered or investment advice.'}
            pid = secrets.token_hex(16)
            c.execute('INSERT INTO previews(id,comparison_id,actor,scope,revision,comparison_version,before_state,after_state,effect) VALUES(?,?,?,?,?,?,?,?,?)',
                      (pid, cid, user['persona'], row['scope'], ledger['revision'], row['version'], encode(before), encode(after), encode(effect)))
            return {'id': pid, 'revision': ledger['revision'], 'effect': effect}

    @app.post('/api/commit')
    def commit(body: Commit, user=Depends(session)):
        with db(True) as c:
            p = c.execute('SELECT * FROM previews WHERE id=? AND actor=?', (body.preview_id, user['persona'])).fetchone()
            if not p:
                raise HTTPException(404, 'Preview not available')
            if p['used']:
                raise HTTPException(409, 'This preview was already committed')
            if p['comparison_id'].startswith('document:'):
                document(c, p['comparison_id'].split(':', 1)[1], user['persona'])
                comparison_version = 0
            else:
                row, *_ = comparison(c, p['comparison_id'], user['persona'])
                comparison_version = row['version']
            ledger = c.execute('SELECT * FROM ledger WHERE scope=?', (p['scope'],)).fetchone()
            if ledger['revision'] != p['revision'] or comparison_version != p['comparison_version']:
                raise HTTPException(409, 'The ledger or evidence changed. Generate a new preview.')
            # Recheck every source used by the resulting state at commit time.
            for v in json.loads(p['after_state']).values():
                for o in v['observations']:
                    for did in o['source_ids']:
                        document(c, did, user['persona'])
            revision = ledger['revision'] + 1
            c.execute('UPDATE ledger SET revision=?,state=? WHERE scope=?', (revision, p['after_state'], p['scope']))
            c.execute('UPDATE previews SET used=1 WHERE id=?', (p['id'],))
            cursor = c.execute('INSERT INTO events(scope,revision,action,actor,comparison_id,before_state,after_state,detail,created) VALUES(?,?,?,?,?,?,?,?,?)',
                (p['scope'], revision, 'commit', user['persona'], p['comparison_id'], p['before_state'], p['after_state'], json.loads(p['effect'])['title'], now()))
            return {'revision': revision, 'event_id': cursor.lastrowid}

    @app.post('/api/events/{eid}/undo')
    def undo(eid: int, user=Depends(session)):
        with db(True) as c:
            event = c.execute('SELECT * FROM events WHERE id=? AND scope IN (?,?)', (eid, 'family', user['persona'])).fetchone()
            if not event or event['actor'] != user['persona']:
                raise HTTPException(404, 'Decision not available for reversal')
            ledger = c.execute('SELECT * FROM ledger WHERE scope=?', (event['scope'],)).fetchone()
            if event['action'] != 'commit' or ledger['revision'] != event['revision']:
                raise HTTPException(409, 'Only your latest unchanged committed decision can be reversed')
            for value in json.loads(event['before_state']).values():
                for obs in value['observations']:
                    for did in obs['source_ids']:
                        document(c, did, user['persona'])
            rev = ledger['revision'] + 1
            c.execute('UPDATE ledger SET revision=?,state=? WHERE scope=?', (rev, event['before_state'], event['scope']))
            c.execute('INSERT INTO events(scope,revision,action,actor,before_state,after_state,detail,created) VALUES(?,?,?,?,?,?,?,?)',
                      (event['scope'], rev, 'undo', user['persona'], ledger['state'], event['before_state'], f'Reversed decision {eid}; original history preserved', now()))
            return {'revision': rev}

    @app.get('/api/ledger')
    def get_ledger(scope: str = 'family', revision: int | None = None, as_of: str | None = None, user=Depends(session)):
        if scope not in ('family', user['persona']):
            raise HTTPException(404, 'Ledger not available')
        if as_of:
            try:
                date.fromisoformat(as_of)
            except ValueError as exc:
                raise HTTPException(422, 'Use YYYY-MM-DD') from exc
        with db() as c:
            current = c.execute('SELECT * FROM ledger WHERE scope=?', (scope,)).fetchone()
            state = json.loads(current['state'])
            actual_rev = current['revision']
            if revision is not None and revision != actual_rev:
                event = c.execute('SELECT * FROM events WHERE scope=? AND revision=?', (scope, revision)).fetchone()
                if not event:
                    raise HTTPException(404, 'Historical revision not available')
                state = json.loads(event['after_state']); actual_rev = revision
            visible = allowed_state(c, state, user['persona'])
            result = summarize(visible, as_of)
            result.update(revision=actual_rev, current_revision=current['revision'], scope=scope, as_of=as_of)
            events = c.execute('SELECT * FROM events WHERE scope=? ORDER BY id DESC', (scope,)).fetchall()
            result['events'] = [{k: e[k] for k in ('id', 'revision', 'action', 'actor', 'detail', 'created')} | {
                'can_undo': e['action'] == 'commit' and e['revision'] == current['revision'] and e['actor'] == user['persona']} for e in events]
            return result

    @app.get('/api/maturities')
    def get_maturities(scope: str = 'family', holder: str | None = None,
                       status: str | None = None, sort: str = 'asc', user=Depends(session)):
        if scope not in ('family', user['persona']):
            raise HTTPException(404, 'Ledger not available')
        if status is not None and status not in MATURITY_STATUSES:
            raise HTTPException(422, 'Choose a valid maturity status')
        if sort not in ('asc', 'desc'):
            raise HTTPException(422, 'Choose ascending or descending maturity-date order')
        with db() as c:
            ledger = c.execute('SELECT * FROM ledger WHERE scope=?', (scope,)).fetchone()
            visible = allowed_state(c, json.loads(ledger['state']), user['persona'])
            rows = []
            for position in summarize(visible)['positions']:
                maturity_date = position.get('maturity_date')
                row = {**position, 'maturity_date': maturity_date,
                       **maturity_details(maturity_date)}
                row['projected_proceeds'] = position.get('maturity_value')
                rows.append(row)

            holders = sorted({row['owner_id'] for row in rows if row.get('owner_id')})
            counts = {key: 0 for key in MATURITY_STATUSES}
            proceeds = Decimal('0')
            proceeds_count = 0
            for row in rows:
                counts[row['maturity_status']] += 1
                if row['projected_proceeds'] is not None:
                    proceeds += Decimal(row['projected_proceeds'])
                    proceeds_count += 1

            filtered = [row for row in rows
                        if (holder is None or row.get('owner_id') == holder)
                        and (status is None or row['maturity_status'] == status)]
            dated = [row for row in filtered if row['maturity_date']]
            undated = [row for row in filtered if not row['maturity_date']]
            dated.sort(key=lambda row: (row['maturity_date'], row['account_id']), reverse=sort == 'desc')
            undated.sort(key=lambda row: row['account_id'])
            return {
                'scope': scope,
                'revision': ledger['revision'],
                'as_of': date.today().isoformat(),
                'holders': holders,
                'summary': {
                    'accepted_fds': len(rows),
                    **counts,
                    'projected_proceeds': format(proceeds, '.2f'),
                    'projected_proceeds_count': proceeds_count,
                },
                'positions': dated + undated,
            }

    @app.get('/api/evaluation')
    def evaluation(user=Depends(session)):
        report = ROOT / 'evaluation/results.json'
        return json.loads(report.read_text()) if report.exists() else {'status': 'not_run'}

    app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')

    @app.get('/')
    def home():
        return FileResponse(ROOT / 'static/index.html')

    # New, otherwise-empty databases start with the synthetic workspace. Do not
    # seed over a database that already contains user documents or ledger history.
    with db(True) as c:
        seed_workspace(c, only_if_empty=True)
    return app


app = create_app()
