import io
import sqlite3
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas
from nestproof.app import create_app
from nestproof.engine import normalize, parse_document
from nestproof.fixtures import pdf_bytes, scenarios

@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(tmp_path / 'test.db')) as c:
        login(c)
        yield c

def login(c, persona='ananya'):
    r = c.post('/api/session', json={'persona': persona})
    assert r.status_code == 200
    c.headers['X-NestProof-CSRF'] = r.json()['csrf']

def seed(c):
    assert c.post('/api/demo').status_code == 200
    return {d['scenario']: d for d in c.get('/api/documents').json()}

def compare(c, docs, scenario):
    r = c.post('/api/comparisons', json={'right_id': docs[scenario]['id']})
    assert r.status_code == 200, r.text
    return r.json()

def preview(c, review):
    if review.get('kind') == 'new':
        r = c.post('/api/documents/' + review['document']['id'] + '/preview')
        assert r.status_code == 200, r.text
        return r.json()
    r = c.post('/api/comparisons/' + review['id'] + '/preview')
    assert r.status_code == 200, r.text
    return r.json()

def commit(c, p):
    r = c.post('/api/commit', json={'preview_id':p['id']})
    assert r.status_code == 200, r.text
    return r.json()

def upload(c, lines, name='own.pdf', visibility='private'):
    return c.post('/api/documents', files={'file': (name, pdf_bytes(name, lines), 'application/pdf')}, data={'visibility': visibility})

def test_clarification_dedup_and_undo(client):
    c=client; docs=seed(c); r=compare(c,docs,'clarify')
    assert r['kind']=='comparison'
    assert r['left']['id']==docs['baseline']['id']
    assert r['result']['relation']=='review'
    assert r['question']['field']=='account_id'
    assert c.post('/api/comparisons/'+r['id']+'/preview').status_code==409
    r=c.post('/api/comparisons/'+r['id']+'/clarify',json={'value':'FD-1007','note':'Checked the original certificate','version':0}).json()
    assert r['result']['relation']=='same'
    assert r['answers'][0]['provenance']=='user-supplied'
    p=preview(c,r); assert p['effect']['delta']=='0.00'
    result=commit(c,p)
    ledger=c.get('/api/ledger').json()
    assert ledger['total']=='400000.00'
    assert len(ledger['positions'][0]['source_ids'])==2
    assert 'user-supplied' in ledger['positions'][0]['provenance']
    assert c.post('/api/commit',json={'preview_id':p['id']}).status_code==409
    assert c.post(f"/api/events/{result['event_id']}/undo").status_code==200
    assert len(c.get('/api/ledger').json()['positions'][0]['source_ids'])==1
    assert c.get('/api/ledger?revision=2').json()['positions'][0]['source_ids']==ledger['positions'][0]['source_ids']

def test_separate_historical_and_stale_preview(client):
    c=client; d=seed(c); p1=preview(c,compare(c,d,'new')); p2=preview(c,compare(c,d,'history'))
    assert p1['effect']['after']=='580000.00'
    event=commit(c,p1)
    assert c.post('/api/commit',json={'preview_id':p2['id']}).status_code==409
    p2=preview(c,compare(c,d,'history')); assert p2['effect']['delta']=='0.00'; commit(c,p2)
    assert c.get('/api/ledger?as_of=2026-07-01').json()['total']=='390000.00'
    assert c.get('/api/ledger?revision=1').json()['total']=='400000.00'
    assert c.post(f"/api/events/{event['event_id']}/undo").status_code==409

@pytest.mark.parametrize('choice,total',[('keep_existing','400000.00'),('use_incoming','410000.00')])
def test_conflict_requires_choice(client,choice,total):
    c=client; d=seed(c); r=compare(c,d,'conflict')
    assert r['result']['relation']=='conflict'
    assert c.post('/api/comparisons/'+r['id']+'/preview').status_code==409
    r=c.post('/api/comparisons/'+r['id']+'/clarify',json={'value':choice,'note':'Reviewed original evidence','version':0}).json()
    commit(c,preview(c,r)); assert c.get('/api/ledger').json()['total']==total

def test_private_routes_and_csrf(client):
    c=client; d=seed(c)
    assert 'private' not in d
    assert c.get('/api/ledger?scope=ravi').status_code==404
    login(c,'ravi'); private=next(d for d in c.get('/api/documents').json() if d['scope']=='ravi')
    assert c.get('/api/ledger?scope=ravi').json()['total']=='250000.00'
    login(c)
    for suffix in ('','/source'):
        assert c.get('/api/documents/'+private['id']+suffix).status_code==404
    assert c.post('/api/documents/'+private['id']+'/preview').status_code==404
    assert c.post('/api/comparisons',json={'right_id':private['id']}).status_code==404
    assert c.post('/api/demo',headers={'X-NestProof-CSRF':'forged'}).status_code==403
    assert c.post('/api/session',headers={'Origin':'https://hostile.invalid'},json={'persona':'ravi'}).status_code==403

def test_actor_cannot_use_others_preview(client):
    c=client; d=seed(c); r=compare(c,d,'history'); p=preview(c,r)
    login(c,'ravi')
    assert c.get('/api/comparisons/'+r['id']).status_code==404
    assert c.post('/api/commit',json={'preview_id':p['id']}).status_code==404

def test_revocation_applies_to_past_and_pending(client):
    c=client; d=seed(c); p=preview(c,compare(c,d,'new'))
    assert c.post('/api/documents/'+d['baseline']['id']+'/revoke').status_code==200
    assert c.get('/api/documents/'+d['baseline']['id']+'/source').status_code==404
    assert c.get('/api/ledger?revision=1').json()['positions']==[]
    assert c.post('/api/commit',json={'preview_id':p['id']}).status_code in (404,409)
    ledger=c.get('/api/ledger').json()
    assert ledger['events'][0]['action']=='revoke'

def test_injection_and_maturity_only(client):
    c=client; d=seed(c)
    attack=compare(c,d,'attack'); assert attack['result']['relation']=='blocked'
    assert attack['question'] is None
    assert c.post('/api/comparisons/'+attack['id']+'/preview').status_code==409
    maturity=compare(c,d,'maturity'); assert maturity['result']['relation']=='review'
    assert maturity['question']['field']=='principal'
    assert 'principal' not in maturity['right']['facts']

def test_first_upload_then_same_upload(client):
    c=client; _,lines,*_=scenarios()[0]
    content=pdf_bytes('User file',lines)
    r=c.post('/api/documents',files={'file':('user.pdf',content)},data={'visibility':'private'}); assert r.status_code==200
    did=r.json()['document']['id']
    again=c.post('/api/documents',files={'file':('user.pdf',content)},data={'visibility':'private'}).json()
    assert not again['created']; assert again['document']['id']==did
    p=c.post('/api/documents/'+did+'/preview'); assert p.status_code==200,p.text
    commit(c,p.json()); assert c.get('/api/ledger?scope=ananya').json()['total']=='400000.00'
    assert c.post('/api/documents/'+did+'/preview').status_code==409

def test_cross_scope_comparison_denied(client):
    c=client; d=seed(c); own=upload(c,scenarios()[0][1]).json()['document']
    result=c.post('/api/comparisons',json={'right_id':own['id']}).json()
    assert result['kind']=='new'
    assert result['document']['scope']==own['scope']=='ananya'

def test_no_silent_overwrite_from_older_anchor(client):
    c=client; d=seed(c)
    # The matcher anchors to the current accepted observation, not the older uploaded statement.
    commit(c,preview(c,compare(c,d,'history')))
    r=compare(c,d,'conflict')
    assert r['result']['relation']=='conflict'
    assert c.post('/api/comparisons/'+r['id']+'/preview').status_code==409
    assert c.get('/api/ledger').json()['total']=='400000.00'

def test_question_limit_and_stale_answer(client):
    c=client; d=seed(c)
    # Construct omissions independently of fixture spelling.
    lines=['As of: 2026-09-30','Principal: 400000','Currency: INR']
    doc=upload(c,lines,visibility='family').json()['document']
    r=c.post('/api/comparisons',json={'right_id':doc['id']}).json()
    for version,value in enumerate(('FD-1007','PERSON-ANANYA')):
        response=c.post('/api/comparisons/'+r['id']+'/clarify',json={'value':value,'note':'Synthetic source confirmation','version':version}); assert response.status_code==200,response.text
    r=response.json(); assert r['question'] is None; assert not r['can_preview']
    assert c.post('/api/comparisons/'+r['id']+'/clarify',json={'value':'NORTHSTAR','note':'Synthetic source confirmation','version':2}).status_code==409

def test_bad_uploads_and_headers(client):
    c=client
    for name,content in [('bad.pdf',b'not a PDF'),('bad.exe',b'long arbitrary content'),('bad.txt',b'\xff'*20),('huge.txt',b'x'*(3*1024*1024+1))]:
        assert c.post('/api/documents',files={'file':(name,content)}).status_code==422
    out=io.BytesIO(); pdf=canvas.Canvas(out);pdf.showPage();pdf.save()
    assert c.post('/api/documents',files={'file':('scan.pdf',out.getvalue())}).status_code==422
    assert "script-src 'self'" in c.get('/').headers['content-security-policy']
    assert c.get('/api/documents').headers['cache-control']=='no-store'

@pytest.mark.parametrize('value',['1,2,3','4,,000','1e5','-20','NaN','400000.999'])
def test_invalid_amounts(value):
    with pytest.raises(ValueError): normalize('principal',value)

@pytest.mark.parametrize('value',['400000','400,000','4,00,000','INR 400000.00'])
def test_supported_amounts(value):
    assert normalize('principal',value)=='400000.00'

def test_conflicting_fields_are_quarantined():
    doc=parse_document(b'Principal: 400000\nPrincipal amount: 500000\nCurrency: INR','conflict.txt')
    assert any(f['code']=='conflicting_field' for f in doc['flags'])
    assert 'principal' not in doc['facts']

def test_new_deposit_uses_ledger_first_observation_flow(client):
    c=client; docs=seed(c); review=compare(c,docs,'new')
    assert review['kind']=='new'
    assert c.get('/api/ledger').json()['total']=='400000.00'
    p=preview(c,review)
    assert p['effect']['delta']=='180000.00'
    commit(c,p)
    assert c.get('/api/ledger').json()['total']=='580000.00'

def test_multiple_uploads_do_not_become_ledger_matches(client):
    c=client; docs=seed(c)
    unrelated=upload(c,scenarios()[2][1],name='uncommitted-new.pdf',visibility='family').json()['document']
    incoming=upload(c,scenarios()[1][1],name='masked-incoming.pdf',visibility='family').json()['document']
    review=c.post('/api/comparisons',json={'right_id':incoming['id']}).json()
    assert review['kind']=='comparison'
    assert review['left']['id']==docs['baseline']['id']
    assert review['left']['id']!=unrelated['id']

    new_review=compare(c,docs,'new')
    commit(c,preview(c,new_review))
    another=upload(c,scenarios()[1][1],name='masked-after-second-deposit.pdf',visibility='family').json()['document']
    unresolved=c.post('/api/comparisons',json={'right_id':another['id']}).json()
    assert unresolved['kind']=='unresolved'
    assert len(unresolved['candidates'])==2

def test_review_cannot_continue_after_ledger_revision_changes(client):
    c=client; docs=seed(c); review=compare(c,docs,'clarify')
    commit(c,preview(c,compare(c,docs,'new')))
    response=c.post('/api/comparisons/'+review['id']+'/clarify',
                    json={'value':'FD-1007','note':'Checked the original certificate','version':0})
    assert response.status_code==409

def test_fresh_workspace_initializes_synthetic_records(tmp_path):
    with TestClient(create_app(tmp_path/'fresh.db')) as c:
        login(c)
        family=c.get('/api/ledger').json()
        assert family['total']=='400000.00'
        assert family['current_revision']==1
        docs=c.get('/api/documents').json()
        assert any(doc['scenario']=='baseline' for doc in docs)
        login(c,'ravi')
        assert c.get('/api/ledger?scope=ravi').json()['total']=='250000.00'

def test_clean_new_fd_is_previewable_and_committable(client):
    c=client
    content=(Path(__file__).resolve().parents[1]/'samples'/'new.pdf').read_bytes()
    uploaded=c.post('/api/documents',files={'file':('new.pdf',content,'application/pdf')},data={'visibility':'private'})
    assert uploaded.status_code==200, uploaded.text
    document=uploaded.json()['document']
    assert document['missing']==[]
    assert document['flags']==[]
    review=c.post('/api/comparisons',json={'right_id':document['id']}).json()
    assert review['kind']=='new'
    assert c.get('/api/ledger?scope=ananya').json()['total']=='0.00'
    p=preview(c,review)
    assert p['effect']['after']=='180000.00'
    assert c.get('/api/ledger?scope=ananya').json()['total']=='0.00'
    commit(c,p)
    assert c.get('/api/ledger?scope=ananya').json()['total']=='180000.00'

def test_existing_comparison_schema_migrates(tmp_path):
    path=tmp_path/'legacy.db'
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE comparisons(id TEXT PRIMARY KEY, actor TEXT, left_id TEXT, right_id TEXT, scope TEXT, answers TEXT, version INTEGER, created TEXT)')
    create_app(path)
    with sqlite3.connect(path) as db:
        columns={row[1] for row in db.execute('PRAGMA table_info(comparisons)')}
    assert {'left_facts','ledger_revision'} <= columns
