'use strict';
const $ = (s) => document.querySelector(s);
const escapeHTML = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const E = escapeHTML;
const money = value => new Intl.NumberFormat('en-IN', {style:'currency',currency:'INR',maximumFractionDigits:0}).format(Number(value || 0));
const fieldNames = {owner_id:'Holder reference',account_id:'Deposit reference',institution:'Institution',as_of:'Effective date',principal:'Principal',currency:'Currency',maturity_value:'Maturity proceeds',maturity_date:'Maturity date'};
const labels = {workspace:'Import review',history:'Ledger & history',evaluation:'Evidence lab',about:'How it works'};
const state = {csrf:'',persona:'ananya',view:'workspace',docs:[],ledger:null,selected:null,comparison:null,preview:null,highlight:null,single:null,matchIssue:null,scope:'family',request:0};

async function api(path, options={}) {
  const headers = {...options.headers};
  if (options.body && !(options.body instanceof FormData)) { headers['Content-Type']='application/json'; options.body=JSON.stringify(options.body); }
  if (options.method && options.method !== 'GET') headers['X-NestProof-CSRF']=state.csrf;
  const response = await fetch('/api'+path,{...options,headers,credentials:'same-origin'});
  let result;
  try { result=await response.json(); } catch { throw new Error('The server returned an unreadable response.'); }
  if (!response.ok) throw new Error(typeof result.detail==='string' ? result.detail : 'Please check the input and try again.');
  return result;
}
function notify(message,error=false) {const n=$('#notice'); n.textContent=message; n.className='notice'+(error?' error':'');n.hidden=false;}
function clearNotice() {$('#notice').hidden=true;}
async function action(button, work) {if(button)button.disabled=true;try {await work();}catch(e){notify(e.message,true);}finally{if(button)button.disabled=false;}}
function display(field,value) {if(value===undefined||value===null)return 'Not established';return ['principal','maturity_value'].includes(field)?money(value):value;}
function status(doc) {if(doc.flags.length)return ['Needs attention','red'];if(doc.missing.length)return ['Evidence needed','amber'];return ['Ready to review','green'];}

async function refresh() {
  const [docs,ledger]=await Promise.all([api('/documents'),api('/ledger?scope='+encodeURIComponent(state.scope))]);
  state.docs=docs; state.ledger=ledger;
  renderStats();
}
function renderStats() {
  $('#stats').innerHTML=`<div class="stat"><div class="stat-label">Recorded deposit principal</div><div class="stat-value">${money(state.ledger?.total)}</div><div class="stat-foot">${state.scope==='family'?'Shared family':'Private'} scope · dated principal, not current net worth</div><span class="stat-icon">↗</span></div>
  <div class="stat"><div class="stat-label">Documents in your view</div><div class="stat-value">${state.docs.length.toString().padStart(2,'0')}</div><div class="stat-foot">Only sources this persona can access</div><span class="stat-icon">▤</span></div>
  <div class="stat"><div class="stat-label">Ledger revision</div><div class="stat-value">${String(state.ledger?.current_revision||0).padStart(2,'0')}</div><div class="stat-foot">Changes recorded. Earlier versions preserved.</div><span class="stat-icon">↶</span></div>`;
}
function render() {
  document.querySelectorAll('.nav').forEach(b=>b.classList.toggle('active',b.dataset.view===state.view));
  $('#page-crumb').textContent=labels[state.view];
  if(state.view==='workspace')renderWorkspace();
  else if(state.view==='history')renderHistory();
  else if(state.view==='evaluation')renderLab();
  else renderAbout();
}
function emptyWorkspace() {
  return `<div class="empty-state"><div class="empty-illustration">n·</div><div class="eyebrow">A WORKSPACE YOU CAN PUT TO THE TEST</div><h2>Start with the evidence.</h2><p>Open a synthetic family workspace with an existing deposit, a masked reference, a conflicting statement and a document-borne instruction attack. Every file passes through the real parser.</p><button class="button primary" id="seed">Open synthetic workspace <span>→</span></button><p class="hint">No real bank accounts. No model API key. No preassigned outcomes.</p></div>`;
}
function renderWorkspace() {
  if(!state.docs.length){$('#view').innerHTML=emptyWorkspace();$('#seed').onclick=e=>action(e.currentTarget,async()=>{await api('/demo',{method:'POST'});await refresh();render();});return;}
  $('#view').innerHTML=`<div class="section-title"><div><h2>Import workspace <span class="count">${state.docs.length} sources</span></h2><p>Choose an incoming document. Inspect the evidence before changing the ledger.</p></div><select class="scope-select" id="scope" aria-label="Ledger scope"><option value="family">Shared family ledger</option><option value="${E(state.persona)}">My private ledger</option></select></div>
  <div class="workbench"><aside class="panel"><div class="panel-heading"><h3>Source documents</h3><small>PDF / TXT</small></div><div class="document-list">${state.docs.map(d=>{
    const [text,color]=status(d);return `<button class="document-card ${state.selected===d.id?'active':''}" data-doc="${E(d.id)}"><span class="doc-top"><span class="pdf-icon">${d.name.endsWith('.pdf')?'PDF':'TXT'}</span><span><span class="doc-name">${E(d.name.replace(/\.(pdf|txt)$/i,''))}</span><span class="doc-meta">${E(d.facts.as_of||'Date unresolved')} · ${d.scope==='family'?'Shared':'Private'}</span></span></span><span class="doc-bottom"><span class="pill ${d.scenario==='baseline'?'':color}">${d.scenario==='baseline'?'Starting ledger source':text}</span></span></button>`;
  }).join('')}</div><div class="queue-footer">Original sources stay intact.<br>Review decisions are stored separately.</div></aside><div id="review-panel">${state.comparison?reviewHTML():state.single?singleHTML():state.matchIssue?matchIssueHTML():`<div class="empty-state"><div class="empty-illustration">↗</div><h2>A closer look, before a change.</h2><p>Start with <strong>Masked deposit summary</strong> to see how a single missing reference becomes a precise clarification.</p><button class="button secondary" id="start-review">Review the masked statement →</button></div>`}</div></div>`;
  $('#scope').value=state.scope;$('#scope').onchange=async e=>{state.scope=e.target.value;await action(e.target,async()=>{await refresh();renderStats();});};
  document.querySelectorAll('[data-doc]').forEach(b=>b.onclick=()=>selectDoc(b.dataset.doc));
  if($('#start-review'))$('#start-review').onclick=()=>selectDoc(state.docs.find(d=>d.scenario==='clarify')?.id||state.docs[0].id);
  bindReview();
  bindSingle();
  if($('#match-form'))$('#match-form').onsubmit=e=>{e.preventDefault();action(e.submitter,async()=>{
    const issue=state.matchIssue;
    const review=await api('/comparisons',{method:'POST',body:{right_id:issue.right_id,clarification:{field:issue.question.field,value:$('#match-value').value,note:$('#match-note').value,revision:issue.ledger_revision}}});
    state.matchIssue=null;state.comparison=review;state.preview=null;renderWorkspace();
    notify('Deposit identified. Your clarification is attributed and the evidence has been checked again.');
  });};
}
async function selectDoc(id) {
  if(!id)return;
  clearNotice();state.selected=id;state.preview=null;state.highlight=null;state.single=null;state.matchIssue=null;state.comparison=null;
  const doc=state.docs.find(d=>d.id===id);
  if(doc?.scope && doc.scope!==state.scope){state.scope=doc.scope;await refresh();}
  const request=++state.request;
  $('#review-panel').innerHTML='<div class="panel loading"><span class="busy-indicator">Matching evidence against accepted ledger records…</span></div>';
  try {
    const match=await api('/comparisons',{method:'POST',body:{right_id:id}});
    if(request!==state.request)return;
    if(match.kind==='new')state.single=match.document;
    else if(match.kind==='unresolved'||match.kind==='represented')state.matchIssue=match;
    else state.comparison=match;
    renderWorkspace();
  }
  catch(e){if(request===state.request){state.comparison=null;renderWorkspace();notify(e.message,true);}}
}
function matchIssueHTML() {
  const issue=state.matchIssue;
  const represented=issue.kind==='represented';
  const clarification=issue.question?`<form class="clarification" id="match-form"><div class="eyebrow">IDENTIFY THE DEPOSIT · QUESTION 1 OF AT MOST 2</div><h3>${E(issue.question.label)}</h3><p>${E(issue.question.reason)}</p><label class="form-label" for="match-value">Reference from your original source</label><input id="match-value" maxlength="100" required autocomplete="off"><label class="form-label" for="match-note">Where did you verify this reference?</label><input id="match-note" minlength="5" maxlength="500" required><button class="button secondary" type="submit">Identify deposit & recheck →</button></form>`:'';
  return `<section class="panel"><div class="review-heading"><div class="eyebrow">LEDGER MATCH</div><span class="pill ${represented?'green':'amber'}">${represented?'Already represented':'Unresolved'}</span><h2>${E(issue.title)}</h2><p>${E(issue.reason)}</p></div><div class="review-body">${issue.candidates.length?`<p>Possible accepted records:</p><ul>${issue.candidates.map(c=>`<li>${E(c.account_id||'Deposit reference not established')} · ${E(c.owner_id||'Holder not established')} · ${E(c.institution||'Institution not established')}</li>`).join('')}</ul>`:''}<p class="block-warning">${represented?'No new observation is needed.': 'No ledger change is available until the incoming identity can be matched unambiguously. Upload clearer evidence or leave this review unresolved.'}</p>${clarification}</div></section>`;
}
function singleHTML() {
  const d=state.single,p=state.preview;
  return `<section class="panel"><div class="review-heading"><div class="eyebrow">FIRST OBSERVATION</div><h2>${E(d.name)}</h2><p>Review the extracted source before adding its principal to this ledger.</p></div><div class="review-body">${d.missing.length||d.flags.length?'<div class="block-warning">This source has unresolved fields or flags. Upload a complete, clearer source before creating the first observation.</div>':`<p>Deposit <strong>${E(d.facts.account_id)}</strong> · Principal <strong>${money(d.facts.principal)}</strong> · ${E(d.facts.as_of)}</p><button class="button primary" id="first-preview">Preview first observation →</button>`}${p?`<div class="preview"><h3>${E(p.effect.title)}</h3><p>${money(p.effect.before)} → ${money(p.effect.after)}</p><p>${E(p.effect.notice)}</p><label class="confirmation-line"><input type="checkbox" id="first-confirm">I reviewed the source and proposed change.</label><button class="button primary" id="first-commit" disabled>Confirm & record decision →</button></div>`:''}${sourceHTML(d,'right')}</div></section>`;
}
function bindSingle() {
  if(!state.single)return;
  if($('#first-preview'))$('#first-preview').onclick=e=>action(e.currentTarget,async()=>{state.preview=await api('/documents/'+state.single.id+'/preview',{method:'POST'});renderWorkspace();});
  if($('#first-confirm'))$('#first-confirm').onchange=e=>{$('#first-commit').disabled=!e.target.checked;};
  if($('#first-commit'))$('#first-commit').onclick=e=>action(e.currentTarget,async()=>{const r=await api('/commit',{method:'POST',body:{preview_id:state.preview.id}});state.preview=null;await refresh();renderWorkspace();notify('First observation recorded at revision '+r.revision+'.');});
}
function sourceHTML(doc,side) {
  return `<div class="source"><div class="source-head"><span>${side==='left'?'LEDGER SUPPORTING SOURCE':'INCOMING SOURCE'}</span><a href="/api/documents/${E(doc.id)}/source" target="_blank" rel="noopener">Download original ↗</a></div><div class="source-lines">${doc.evidence.map(line=>`<div class="source-line ${state.highlight && line.field===state.highlight?'highlight':''} ${line.status==='quarantined'?'quarantined':''}" data-line="${E(line.id)}"><small>${line.page}.${line.line}</small><span>${E(line.text)}</span></div>`).join('')}</div></div>`;
}
function reviewHTML() {
  const c=state.comparison,r=c.result;
  const color=r.relation==='blocked'?'red':['review','conflict'].includes(r.relation)?'amber':'green';
  const fields=['owner_id','account_id','institution','as_of','principal','maturity_value','currency'];
  const questionHTML=c.question?`<form class="clarification" id="clarification-form"><div class="clarify-top"><span class="clarify-mark">?</span><div><div class="eyebrow">CLARIFICATION ${c.answers.length+1} OF AT MOST 2</div><h3>${E(c.question.label)}</h3><p>${E(c.question.reason)}</p></div></div><label class="form-label" for="answer-value">${c.question.type==='choice'?'Your reviewed choice':'Value from your source'}</label>${c.question.type==='choice'?`<select id="answer-value" required><option value="">Choose deliberately…</option><option value="keep_existing">Keep the existing observation</option><option value="use_incoming">Use the incoming observation</option></select>`:`<input id="answer-value" maxlength="100" placeholder="${E(c.question.placeholder)}" required autocomplete="off">`}<label class="form-label" for="answer-note">Where did you verify it?</label><input id="answer-note" placeholder="For example: original certificate, reference field" minlength="5" maxlength="500" required><div class="form-row"><span class="hint">Recorded as user-supplied evidence. You can leave this unresolved.</span><button class="button secondary" type="submit">Apply evidence & recheck →</button></div></form>`:'';
  const preview=state.preview;
  return `<section class="panel"><div class="review-heading"><div class="review-overline">EVIDENCE REVIEW / ${E(c.right.name.replace(/\.(pdf|txt)$/,''))}</div><span class="pill ${color}">${r.relation==='review'?'Evidence needed':r.relation==='blocked'?'Import quarantined':r.relation==='conflict'?'Conflicting evidence':'Supported proposal'}</span><h2>${E(r.title)}</h2><p>${E(r.reason)}</p></div><div class="review-body">
    <table class="comparison-table"><thead><tr><th>FIELD</th><th>LEDGER RECORD</th><th>INCOMING SOURCE</th></tr></thead><tbody>${fields.map(f=>{
      const a=c.interpreted_left[f],b=c.interpreted_right[f],diff=a!==b||a==null||b==null;
      return `<tr class="${diff?'disputed':''}"><td>${fieldNames[f]}</td><td class="${a==null?'missing':''}"><button class="cell-button" data-field="${f}">${E(display(f,a))}</button></td><td class="${b==null?'missing':''}"><button class="cell-button" data-field="${f}">${E(display(f,b))}</button></td></tr>`;
    }).join('')}</tbody></table>
    <p class="hint">Select a value to highlight its original source lines. Principal and maturity proceeds are different fields.</p>
    ${c.answers.map(a=>`<div class="answer-log">✓ ${E(a.field==='value_choice'?'Observation choice':fieldNames[a.field])}: <strong>${E(a.value)}</strong> · User-supplied<br><span>${E(a.note)}</span></div>`).join('')}
    ${questionHTML}
    ${r.relation==='review'&&!c.question?'<div class="block-warning">The two-question limit is reached. Keep this unresolved and supply a clearer source; no ledger change is permitted.</div>':''}
    ${r.relation==='blocked'?`<div class="block-warning">No document can instruct NestProof to change a record or send data elsewhere. This source has been quarantined. It remains available for inspection.</div>`:''}
    ${preview?`<div class="preview"><div class="eyebrow">PREVIEW · LEDGER REVISION ${preview.revision}</div><div class="preview-title">${E(preview.effect.title)}</div><div class="preview-grid"><div><small>REPRESENTED PRINCIPAL BEFORE</small><strong>${money(preview.effect.before)}</strong></div><span>→</span><div><small>AFTER THIS DECISION</small><strong>${money(preview.effect.after)}</strong></div></div><div class="preview-note">Change ${money(preview.effect.delta)} · Effective ${E(preview.effect.effective_date)}<br>${E(preview.effect.notice)}${preview.effect.user_supplied?'<br>Includes explicitly attributed user-supplied clarification.':''}</div><label class="confirmation-line"><input type="checkbox" id="confirm-evidence">I reviewed the source evidence and the proposed change.</label><button class="button primary wide" id="commit" disabled>Confirm & record decision →</button></div>`:''}
    <div class="section-title"><h2>Follow the evidence</h2><span class="subtle">Original extracted text</span></div><div class="source-pair">${sourceHTML(c.left,'left')}${sourceHTML(c.right,'right')}</div><p class="source-caption">Page.line references point to extracted PDF text; this prototype does not perform OCR or certify document authenticity.</p>
    </div><div class="review-actions"><small>Nothing changes until you confirm.<br>Every committed decision has a history.</small>${c.can_preview?'<button class="button primary" id="preview">Preview ledger change →</button>':'<span class="pill amber">Ledger unchanged</span>'}</div></section>`;
}
function bindReview() {
  if(!state.comparison)return;
  document.querySelectorAll('[data-field]').forEach(b=>b.onclick=()=>{state.highlight=b.dataset.field;const scroll=window.scrollY;$('#review-panel').innerHTML=reviewHTML();bindReview();window.scrollTo(0,scroll);});
  if($('#clarification-form'))$('#clarification-form').onsubmit=e=>{e.preventDefault();action(e.submitter,async()=>{const c=state.comparison;const value=$('#answer-value').value,note=$('#answer-note').value;state.comparison=await api(`/comparisons/${c.id}/clarify`,{method:'POST',body:{value,note,version:c.version}});state.preview=null;renderWorkspace();notify('Evidence recorded with its source. Constraints have been checked again.');});};
  if($('#preview'))$('#preview').onclick=e=>action(e.currentTarget,async()=>{state.preview=await api(`/comparisons/${state.comparison.id}/preview`,{method:'POST'});renderWorkspace();$('.preview').scrollIntoView({behavior:'smooth',block:'center'});});
  if($('#confirm-evidence'))$('#confirm-evidence').onchange=e=>{$('#commit').disabled=!e.target.checked;};
  if($('#commit'))$('#commit').onclick=e=>action(e.currentTarget,async()=>{const result=await api('/commit',{method:'POST',body:{preview_id:state.preview.id}});state.preview=null;await refresh();renderWorkspace();notify(`Decision recorded at revision ${result.revision}. You can inspect or undo it in Ledger & history.`);});
}
function renderHistory() {
  const l=state.ledger;
  $('#view').innerHTML=`<div class="section-title"><div><h2>The record, and how it changed</h2><p>Effective date tells you when a figure applies. A revision tells you what was known.</p></div><select id="history-scope" class="scope-select" aria-label="Ledger scope"><option value="family">Shared family</option><option value="${E(state.persona)}">My private ledger</option></select></div><div class="panel"><div class="history-tools"><div><label for="effective-date">Financial position as of</label><input id="effective-date" type="date" value="${E(l.as_of||'')}"></div><div><label for="revision">Known at ledger revision</label><select id="revision"><option value="">Latest knowledge</option>${l.events.map(ev=>`<option value="${ev.revision}" ${l.revision===ev.revision&&l.revision!==l.current_revision?'selected':''}>Revision ${ev.revision} · ${E(ev.action)}</option>`).join('')}</select></div><button class="button secondary" id="history-query">Reconstruct view</button><span class="subtle">Viewing revision ${l.revision} · ${money(l.total)} represented principal</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>DEPOSIT / HOLDER</th><th>PRINCIPAL</th><th>EFFECTIVE DATE</th><th>EVIDENCE</th></tr></thead><tbody>${l.positions.length?l.positions.map(p=>`<tr><td>${E(p.account_id)}<small>${E(p.owner_id)} · ${E(p.institution)}</small></td><td>${money(p.principal)}<small>${E(p.currency)} · principal basis</small></td><td>${E(p.as_of)}<small>Recorded ${E(new Date(p.recorded_at).toLocaleString())}</small></td><td>${p.source_ids.length} source${p.source_ids.length===1?'':'s'}<small>${E(p.provenance)}</small></td></tr>`).join(''):'<tr><td colspan="4">No visible accepted observations for this scope and date.</td></tr>'}</tbody></table></div></div><div class="section-title" ><h2>Decision history</h2><span class="subtle">Append-only revisions</span></div><div class="panel history-list">${l.events.map(ev=>`<div class="history-event"><span class="timeline-dot"></span><div><p>${E(ev.detail)}</p><small>Revision ${ev.revision} · ${E(ev.actor)} · ${E(new Date(ev.created).toLocaleString())}</small>${ev.can_undo?`<br><button class="button small" data-undo="${ev.id}">Undo this decision ↶</button>`:''}</div></div>`).join('')||'<p class="lab-note">No decisions yet.</p>'}</div>`;
  $('#history-scope').value=state.scope;$('#history-scope').onchange=e=>action(e.target,async()=>{state.scope=e.target.value;await refresh();renderHistory();});
  $('#history-query').onclick=e=>action(e.currentTarget,async()=>{const params=new URLSearchParams({scope:state.scope});if($('#effective-date').value)params.set('as_of',$('#effective-date').value);if($('#revision').value)params.set('revision',$('#revision').value);state.ledger=await api('/ledger?'+params);renderHistory();});
  document.querySelectorAll('[data-undo]').forEach(b=>b.onclick=()=>action(b,async()=>{await api(`/events/${b.dataset.undo}/undo`,{method:'POST'});await refresh();renderHistory();notify('Decision reversed in a new revision. The earlier history is preserved.');}));
}
async function renderLab() {
  $('#view').innerHTML='<div class="panel loading">Loading actual evaluation results…</div>';
  try {
    const r=await api('/evaluation');if(state.view!=='evaluation')return;
    if(r.status==='not_run'){$('#view').innerHTML='<div class="empty-state"><h2>Results, when measured.</h2><p>No evaluation report has been generated. Run the evaluation command in the README. We never substitute a target score for a result.</p></div>';return;}
    $('#view').innerHTML=`<div class="section-title"><div><h2>Evidence, not a victory score</h2><p>Development regression set. Shared safeguards. Actual local execution.</p></div><span class="pill green">MEASURED ${E(r.generated_at.slice(0,10))}</span></div><div class="panel"><div class="panel-heading"><h3>Field interpretation regression</h3><small>${r.label_cases} authored labels</small></div><div class="table-scroll"><table class="data-table"><thead><tr><th>METHOD</th><th>CORRECT / ALL</th><th>ACCEPTED FIELD PRECISION</th><th>FIELD COVERAGE</th><th>p95 / LABEL</th></tr></thead><tbody>${r.labels.map(m=>`<tr><td>${E(m.name)}</td><td>${m.correct} / ${m.n}</td><td>${m.precision==null?'N/A':(m.precision*100).toFixed(1)+'%'}</td><td>${(m.coverage*100).toFixed(1)}%</td><td>${m.p95_ms.toFixed(2)} ms</td></tr>`).join('')}</tbody></table></div><div class="lab-note"><p>${E(r.limitations)}</p><p>Scores are observed on this small authored set. They are not financial correctness probabilities.</p></div></div><div class="section-title" ><h2>End-to-end document pairs</h2><span class="subtle">Actual PDF parsing and reconciliation</span></div><div class="panel table-scroll"><table class="data-table"><thead><tr><th>METHOD</th><th>CORRECT RELATIONS</th><th>FALSE SAME DECISIONS</th><th>REVIEW / BLOCKED</th><th>p95 / PAIR</th></tr></thead><tbody>${r.pairs.map(m=>`<tr><td>${E(m.name)}</td><td>${m.correct} / ${m.n}</td><td>${m.false_merges} / ${m.same_decisions} same decisions</td><td>${m.review}</td><td>${m.p95_ms.toFixed(1)} ms</td></tr>`).join('')}</tbody></table></div><div class="scope-note"><strong>What this does not establish</strong><p>No real-user time savings, bank authenticity, scan/OCR quality or production safety has been measured. Exact and fuzzy baselines share the same deterministic reconciliation rules. Failures are published alongside the report.</p><p>Model: ${E(r.model.name)} · ${r.model.training_labels} training labels · threshold ${r.model.threshold} selected using calibration labels.</p></div>`;
  }catch(e){notify(e.message,true);}
}
function renderAbout() {
  $('#view').innerHTML=`<div class="section-title"><div><h2>A small system with explicit boundaries</h2><p>AI interprets field labels. Evidence supplies the values. Code governs changes.</p></div></div><div class="about-grid">${[
    ['01','Interpret the source','A local word/character model classifies financial field labels. Values are copied and validated from actual PDF or text lines; no generative model invents amounts.'],
    ['02','Resolve what matters','Exact holder, account, institution and date constraints identify missing evidence. A bounded policy asks one relevant question, with at most two per review.'],
    ['03','Preview, confirm, reverse','A supported proposal becomes a revision-bound preview. Explicit confirmation writes one transaction. Undo creates a new revision and preserves history.']
  ].map(x=>`<div class="about-card"><span class="step">${x[0]}</span><h3>${x[1]}</h3><p>${x[2]}</p></div>`).join('')}</div><div class="scope-note"><strong>Designed to be challenged</strong><p>Try two different holders with the same amount. Remove the deposit reference. Upload a maturity-only notice. Introduce instruction-like text. Switch demo personas and inspect private sources. A useful system must know when not to change the ledger.</p><strong>Honest scope</strong><p>English labeled digital FD documents, INR principal, synthetic demo personas. No OCR, investment advice, AA integration, production authentication or guarantee of complete wealth. Unknown formats should remain unresolved. Model scores are not probabilities of financial correctness.</p></div>`;
}

document.querySelectorAll('[data-view]').forEach(b=>b.onclick=async()=>{state.view=b.dataset.view;clearNotice();await action(b,async()=>{if(state.view==='history'){await refresh();}render();});});
$('#upload-open').onclick=()=>{$('#upload-error').textContent='';$('#upload-dialog').showModal();};
$('#upload-close').onclick=()=>$('#upload-dialog').close();
$('#file').onchange=()=>{$('#file-label').textContent=$('#file').files[0]?.name||'Choose a file or drop it here';};
$('#dropzone').ondragover=e=>{e.preventDefault();$('#dropzone').classList.add('drag');};
$('#dropzone').ondragleave=()=>$('#dropzone').classList.remove('drag');
$('#dropzone').ondrop=e=>{e.preventDefault();$('#dropzone').classList.remove('drag');if(e.dataTransfer.files.length){$('#file').files=e.dataTransfer.files;$('#file').dispatchEvent(new Event('change'));}};
$('#upload-form').onsubmit=async e=>{e.preventDefault();const form=e.currentTarget;const button=e.submitter;button.disabled=true;$('#upload-error').textContent='';try {const data=new FormData(form);const result=await api('/documents',{method:'POST',body:data});$('#upload-dialog').close();form.reset();$('#file-label').textContent='Choose a file or drop it here';state.view='workspace';await refresh();render();notify(result.created?'Document extracted. Inspect its fields and original evidence.':'This exact source already exists. No duplicate was created.');await selectDoc(result.document.id);}catch(err){$('#upload-error').textContent=err.message;}finally{button.disabled=false;}};
$('#persona').onchange=e=>action(e.target,async()=>{state.request++;const result=await api('/session',{method:'POST',body:{persona:e.target.value}});state.persona=result.persona;state.csrf=result.csrf;state.scope='family';state.comparison=null;state.single=null;state.matchIssue=null;state.preview=null;state.selected=null;$('.avatar').textContent=state.persona[0].toUpperCase();await refresh();render();notify('Synthetic persona changed. Server-side permissions determine which sources are visible.');});

(async()=>{
  try {let s;try{s=await api('/session');}catch{s=await api('/session',{method:'POST',body:{persona:'ananya'}});}state.persona=s.persona;state.csrf=s.csrf;$('#persona').value=s.persona;$('.avatar').textContent=s.persona[0].toUpperCase();await refresh();render();}
  catch(e){notify('Could not connect to the local service: '+e.message,true);$('#view').innerHTML='<div class="empty-state"><h2>The workspace is offline.</h2><p>Start the local server using the README, then reload this page.</p></div>';}
})();
