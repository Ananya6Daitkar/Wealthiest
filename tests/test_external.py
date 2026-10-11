import json
import pytest
from evaluation import external

@pytest.fixture
def pack(tmp_path):
    text='Owner reference: PERSON-FICTIONAL\nDeposit reference: FD-TEST\nBank identifier: FICTIONALBANK\nAs of: 2026-09-30\nPrincipal: 100000\nCurrency: INR\n'
    (tmp_path/'a.txt').write_text(text)
    (tmp_path/'b.txt').write_text(text+'\nSynthetic duplicate\n')
    manifest={'authorship':'Developer-authored unit test, not independent evidence','cases':[{'id':'t1','relation':'same','left':{'file':'a.txt','facts':{'principal':'100000.00','maturity_value':None}},'right':{'file':'b.txt','facts':{'principal':'100000.00','maturity_value':None}}}]}
    m=tmp_path/'manifest.json';m.write_text(json.dumps(manifest))
    f=tmp_path/'freeze.json';external.freeze(f)
    return m,f,manifest

def test_assessor_runner_records_methods_hashes_and_denominators(pack):
    m,f,_=pack;r=external.evaluate(m,f)
    assert r['n']==1
    assert [x['method'] for x in r['methods']]==['exact','fuzzy','ml']
    for method in r['methods']:
        assert method['correct_relations']==1
        assert method['annotated_fields']==4
        assert method['annotated_field_accuracy']==1
        assert method['same_decisions']==1
        assert len(method['rows'][0]['source_sha256']['left'])==64
    assert 'not verified' in r['status']

def test_freeze_drift_is_rejected(pack,monkeypatch):
    m,f,_=pack;monkeypatch.setattr(external,'fingerprint',lambda:{'changed':'yes'})
    with pytest.raises(ValueError,match='Build changed'):external.evaluate(m,f)

def test_existing_results_cannot_be_overwritten(tmp_path):
    p=tmp_path/'report.json';external.write_new(p,{'original':True})
    with pytest.raises(FileExistsError):external.write_new(p,{'original':False})
    assert json.loads(p.read_text())=={'original':True}

@pytest.mark.parametrize('mutation',['path','duplicate','empty','gold'])
def test_invalid_manifest_rejected(pack,mutation):
    m,f,v=pack
    if mutation=='path':v['cases'][0]['left']['file']='../outside.txt'
    elif mutation=='duplicate':v['cases']*=2
    elif mutation=='empty':v['cases']=[]
    else:v['cases'][0]['relation']='approved'
    m.write_text(json.dumps(v))
    with pytest.raises(ValueError):external.evaluate(m,f)

def test_parser_failure_stays_in_denominator(pack):
    m,f,v=pack;(m.parent/'b.txt').write_bytes(b'\xff\xfeinvalid')
    r=external.evaluate(m,f)
    for method in r['methods']:
        assert method['parser_failures']==1
        assert method['correct_relations']==0
        assert method['annotated_fields']==4
        assert method['annotated_field_accuracy']==0.5
        assert method['same_precision'] is None
        assert method['rows'][0]['parser_errors']
