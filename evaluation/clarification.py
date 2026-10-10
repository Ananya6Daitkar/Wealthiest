"""Policy simulation with truthful oracle answers, not a human user study."""
import json
from pathlib import Path
from nestproof.engine import select_match_field

def run():
    fields=['account_id','owner_id','institution'];rows=[]
    # Each case has one distinguishing field. Vary its position and target.
    # These model the production one-answer disambiguation path.
    for distinct in fields:
        for count in (2,3,5):
            candidates=[{f:(f'{f}-{i}' if f==distinct else f'{f}-shared') for f in fields} for i in range(count)]
            for target in candidates:
                counts={}
                for policy in ('adaptive','fixed','all_fields'):
                    remaining=candidates[:];missing=fields[:];questions=0
                    while len(remaining)>1 and missing:
                        f=select_match_field(remaining,missing) if policy=='adaptive' else missing[0]
                        remaining=[c for c in remaining if c[f]==target[f]];missing.remove(f);questions+=1
                    counts[policy]=len(fields) if policy=='all_fields' else questions
                rows.append({'distinguishing_field':distinct,'candidates':count,'questions':counts})
    result={'status':'Synthetic oracle-answer policy simulation. Not user effort or independently validated impact.',
            'n':len(rows),'mean_questions':{p:sum(r['questions'][p] for r in rows)/len(rows) for p in ('adaptive','fixed','all_fields')},
            'limitations':'Cases deliberately have one fully distinguishing field. No typo, incorrect answer, partial distinction, abandonment or human timing is modeled.', 'rows':rows}
    Path('evaluation/clarification-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
if __name__=='__main__':run()
