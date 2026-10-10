"""Run from repository root: python -m evaluation.run."""
import hashlib
import json
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from nestproof.engine import classify, clean_label, model, fuzzy_threshold, parse_document, reconcile
from nestproof.fixtures import pdf_bytes, scenarios
from nestproof.labels import TRAIN, CALIBRATION
from .cases import LABELS, pairs

ROOT=Path(__file__).resolve().parents[1]

def main():
    train={clean_label(v) for values in TRAIN.values() for v in values}
    calibration={clean_label(v) for values in CALIBRATION.values() for v in values}
    test={clean_label(v) for values in LABELS.values() for v in values}
    assert not train & test, 'Test labels overlap training labels'
    assert not calibration & test, 'Test labels overlap calibration labels'
    _,manifest=model() # exclude cold training from per-label inference latency
    report={'generated_at':datetime.now(timezone.utc).isoformat(),'model':manifest,'platform':platform.platform(),'python':platform.python_version(),
      'evaluation_status':'Development regression: cases were inspected before adding shared role guards. Not an untouched final test.',
      'fuzzy_threshold':fuzzy_threshold(),
      'test_sha256':hashlib.sha256((ROOT/'evaluation/cases.py').read_bytes()).hexdigest(),
      'label_cases':sum(map(len,LABELS.values())),'labels':[],'pairs':[],
      'limitations':'Development regression set used to diagnose role errors; shared exclusion rules were added after inspection. Small developer-authored synthetic set; same author as training data. No real-user or real-bank validation. Test labels were not used to select the model threshold. PDF layouts share a generator. Latency is local warm inference, not a service SLA.'}
    generated=[(case,pdf_bytes('Held-out source A',case['left']),pdf_bytes('Held-out source B',case['right'])) for case in pairs()]
    names={'exact':'Exact dictionary + role guard','fuzzy':f'Calibrated fuzzy + role guard ({fuzzy_threshold():.3f})','ml':'NestProof ML + role guard'}
    for method in names:
        rows=[];elapsed=[]
        for truth,labels in LABELS.items():
            for label in labels:
                start=time.perf_counter(); pred,score=classify(label,method);elapsed.append((time.perf_counter()-start)*1000)
                rows.append({'label':label,'gold':truth,'prediction':pred,'score':round(score,5)})
        accepted=[r for r in rows if r['prediction']!='ignore']
        metric={'method':method,'name':names[method],'n':len(rows),'correct':sum(r['gold']==r['prediction'] for r in rows),
          'accepted':len(accepted),'precision':sum(r['gold']==r['prediction'] for r in accepted)/len(accepted) if accepted else None,
          'coverage':sum(r['prediction']!='ignore' and r['gold']!='ignore' for r in rows)/sum(r['gold']!='ignore' for r in rows),
          'p95_ms':float(np.percentile(elapsed,95)),'failures':[r for r in rows if r['gold']!=r['prediction']]}
        report['labels'].append(metric)
        rows=[];elapsed=[]
        for case,ab,bb in generated:
            start=time.perf_counter();a=parse_document(ab,'left.pdf',method);b=parse_document(bb,'right.pdf',method);pred=reconcile(a,b)['relation'];elapsed.append((time.perf_counter()-start)*1000)
            rows.append({'id':case['id'],'gold':case['gold'],'prediction':pred,'missing':a['missing']+b['missing']})
        report['pairs'].append({'method':method,'name':names[method],'n':len(rows),'correct':sum(r['gold']==r['prediction'] for r in rows),
          'false_merges':sum(r['prediction']=='same' and r['gold']!='same' for r in rows),'same_decisions':sum(r['prediction']=='same' for r in rows),
          'review':sum(r['prediction'] in ('review','blocked') for r in rows),'p95_ms':float(np.percentile(elapsed,95)),
          'failures':[r for r in rows if r['gold']!=r['prediction']]})
    (ROOT/'evaluation/results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('label_cases','model')},indent=2))
    for group in ('labels','pairs'):
        for row in report[group]:print(group,json.dumps({k:v for k,v in row.items() if k!='failures'}))

if __name__=='__main__':main()
