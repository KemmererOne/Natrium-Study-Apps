import json,re,subprocess,collections
d=json.load(open('work/objectives.json'))
tot=0
for m in d['modules']:
    e=sum(len(t['enabling']) for t in m['terminal'])
    print(f"{str(m['code']):7} {m['source_id']:12} T{len(m['terminal']):2} E{e:3} {m['title']} | {[p['printed'] for p in m['objective_pages']]}")
    nums=[o['number'] for t in m['terminal'] for o in t['enabling']]
    seq=[tuple(map(int,n.split('.'))) for n in nums]
    for a,b in zip(seq,seq[1:]):
        if not(b>a) or (b[0]==a[0] and b[1]!=a[1]+1): print('   SEQ',a,b)
    if len(set(nums))!=len(nums): print('   DUPNUM')
    for t in m['terminal']:
        if not t['enabling']: print('   NO ENABLING',t['number'])
        for o in t['enabling']:
            if o['number'].split('.')[0]!=t['number'].split('.')[0]: print('   MISFILED',t['number'],o['number'])
    for o in m['orphans']: print('   ORPHAN',str(o)[:120])
# completeness: every word on each objectives page must be in the parsed output
W=lambda s:re.findall(r'[A-Za-z0-9]+',s)
miss=0
for m in d['modules']:
    parsed=collections.Counter()
    for t in m['terminal']:
        for o in [t]+t['enabling']:
            parsed.update(W(o['number']+' '+o['raw'])); 
            for i in o['items']: parsed.update(W(i))
    page=collections.Counter()
    for pr in m['objective_pages']:
        tx=subprocess.run(['pdftotext','-layout','-f',str(pr['pdf']),'-l',str(pr['pdf']),'sources/'+m['file'],'-'],capture_output=True,text=True,errors='replace').stdout
        for l in tx.splitlines():
            if re.search(r'DOE-HDBK-10|Page \S+\s|TERMINAL OBJECTIVE|ENABLING OBJECTIVE',l): continue
            page.update(W(l))
    diff=page-parsed
    if diff:
        miss+=sum(diff.values()); print('MISSING',m['code'],dict(list(diff.items())[:25]))
print('missing tokens',miss)
