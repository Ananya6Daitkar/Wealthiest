import io
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
    r = c.post('/api/comparisons', json={'left_id': docs['baseline']['id'], 'right_id': docs[scenario]['id']})
    assert r.status_code == 200, r.text
    return r.json()

def preview(c, review):
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
    assert c.post('/api/comparisons',json={'left_id':d['baseline']['id'],'right_id':private['id']}).status_code==404
    assert c.post('/api/demo',headers={'X-NestProof-CSRF':'forged'}).status_code==403
    assert c.post('/api/session',headers={'Origin':'https://hostile.invalid'},json={'persona':'ravi'}).status_code==403

def test_actor_cannot_use_others_preview(client):
    c=client; d=seed(c); r=compare(c,d,'new'); p=preview(c,r)
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
    assert c.post('/api/comparisons',json={'left_id':d['baseline']['id'],'right_id':own['id']}).status_code==409

def test_no_silent_overwrite_from_older_anchor(client):
    c=client; d=seed(c)
    # Accept the earlier date; comparing it with a different September value
    # must not bypass the existing September conflict via an 'update' result.
    commit(c,preview(c,compare(c,d,'history')))
    r=c.post('/api/comparisons',json={'left_id':d['history']['id'],'right_id':d['conflict']['id']}).json()
    assert r['result']['relation']=='update'
    assert c.post('/api/comparisons/'+r['id']+'/preview').status_code==409
    assert c.get('/api/ledger').json()['total']=='400000.00'

def test_question_limit_and_stale_answer(client):
    c=client; d=seed(c)
    # Construct omissions independently of fixture spelling.
    lines=['As of: 2026-09-30','Principal: 400000','Currency: INR']
    doc=upload(c,lines,visibility='family').json()['document']
    r=c.post('/api/comparisons',json={'left_id':d['baseline']['id'],'right_id':doc['id']}).json()
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
