// Run through the documented Codex browser Tab API against a fresh synthetic DB.
// This is a reusable browser test, not a dependency on a paid model API.
export async function regression(tab, samplePath) {
  const p=tab.playwright, checks=[];
  const check=async(text,work)=>{await work();checks.push(text);};
  await p.getByRole('button',{name:'＋ Import a document',exact:true}).waitFor({state:'visible',timeoutMs:10000});
  await check('PDF upload opens a first-observation review',async()=>{
    await p.getByRole('button',{name:'＋ Import a document',exact:true}).click();
    await p.domSnapshot();
    const pending=p.waitForEvent('filechooser',{timeoutMs:10000});
    await p.locator('input[type="file"]').click();
    await (await pending).setFiles([samplePath]);
    await p.getByRole('button',{name:'Extract & inspect evidence →',exact:true}).click();
    await p.getByRole('heading',{name:'new.pdf',exact:true}).waitFor({state:'visible',timeoutMs:10000});
    await p.domSnapshot();
  });
  await check('Preview requires explicit confirmation before commit',async()=>{
    await p.getByRole('button',{name:'Preview first observation →',exact:true}).click();
    const commit=p.getByRole('button',{name:'Confirm & record decision →',exact:true});
    await commit.waitFor({state:'visible',timeoutMs:10000});
    if(await commit.isEnabled())throw Error('Commit was enabled before confirmation');
    await p.getByRole('checkbox',{name:'I reviewed the source and proposed change.',exact:true}).check();
    await commit.click();
    await p.getByText('First observation recorded at revision 1.',{exact:true}).waitFor({state:'visible',timeoutMs:10000});
    await p.domSnapshot();
  });
  await check('Ledger exposes a decision receipt and undo',async()=>{
    await p.getByRole('button',{name:'↶ Ledger & history',exact:true}).click();
    await p.getByRole('link',{name:'Download decision receipt ↓',exact:true}).waitFor({state:'visible',timeoutMs:10000});
    await p.domSnapshot();
    await p.getByRole('button',{name:'Undo this decision ↶',exact:true}).click();
    await p.getByText('Decision reversed in a new revision. The earlier history is preserved.',{exact:true}).waitFor({state:'visible',timeoutMs:10000});
    await p.domSnapshot();
  });
  return {checks,passed:checks.length,scope:'Real browser upload, preview, commit and undo. API tests cover receipt authorization and other edge cases.'};
}
