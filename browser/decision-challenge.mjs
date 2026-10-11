// Run after resolving the masked source in the synthetic starting workspace.
// Uses the documented Codex browser Tab API, not a standalone Node driver.
export async function decisionChallenge(tab) {
  const p=tab.playwright;
  const before=await p.locator('#stats').innerText();
  await p.locator('.decision-challenge summary').click();
  await p.locator('#challenge-field').selectOption('principal');
  await p.locator('#challenge-value').fill('400000.01');
  await p.getByRole('button',{name:'Test decision boundary →',exact:true}).click();
  await p.getByRole('heading',{name:'Same deposit, already represented → Two values for the same date',exact:true}).waitFor({state:'visible'});
  if(!(await p.locator('#challenge-result').innerText()).includes('₹4,00,000.01'))throw Error('Paise were not visible');
  await p.locator('#challenge-field').selectOption('account_id');
  await p.locator('#challenge-remove').check();
  await p.getByRole('button',{name:'Test decision boundary →',exact:true}).click();
  await p.getByRole('heading',{name:'Same deposit, already represented → One piece of evidence at a time',exact:true}).waitFor({state:'visible'});
  if(await p.locator('#stats').innerText()!==before)throw Error('Workspace summary changed');
  return {passed:2,scope:'Hypothetical conflict and missing identity; displayed workspace summary unchanged. API tests verify no ledger persistence.'};
}
