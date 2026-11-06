import json,re,os,glob,subprocess
d=json.load(open('work/manifest.json')); M=d['modules']; W=d['word_files']; err=[]
if len(M)!=58 or sum(m['terminal_count'] for m in M)!=74: err.append('counts')
sl=[m['topic']['slug'] for m in M]
if len(set(sl))!=len(sl): err.append('slug dup')
if any(not re.fullmatch(r'[a-z0-9-]+',s) for s in sl): err.append('slug form')
if any(m['topic']['status']!='Draft' for m in M): err.append('status')
if any(not m['title'] or not m['handbook'] for m in M): err.append('title')
disk={os.path.basename(f) for f in glob.glob('sources/*.docx')}
names={w['file'] for w in W}
if disk!=names: err.append(('word set',disk^names))
if any(not w['source_id'] for w in W): err.append(['no source id',[w['file'] for w in W if not w['source_id']]])
for m in M:
    for l in m['word_files']:
        if l['file'] not in names: err.append(('bad link',m['module_id'],l['file']))
    if (m['mapping']=='handbook only')!=(not m['word_files']): err.append(('map',m['module_id']))
    if m['gap_topic'] and m['word_files']: err.append(('rule 11',m['module_id']))
for w in W:
    if not w['modules'] and not w['unmapped_reason']: err.append(('orphan',w['file']))
    if not w['outline']: err.append(('no outline',w['file']))
# every objective verified on its cited PDF page
n=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
cache={};miss=0;tot=0
for m in M:
    for t in m['terminal_objectives']:
        for o in [t]+t['enabling']:
            k=(m['file'],o['page']['pdf'])
            if k not in cache:
                cache[k]=n(subprocess.run(['pdftotext','-f',str(k[1]),'-l',str(k[1]),'sources/'+k[0],'-'],capture_output=True,text=True,errors='replace').stdout)
            tot+=1
            if n(o['text'])[:60] not in cache[k]:
                pg=cache[k]
                nxt=n(subprocess.run(['pdftotext','-f',str(k[1]+1),'-l',str(k[1]+1),'sources/'+k[0],'-'],capture_output=True,text=True,errors='replace').stdout)
                if n(o['text'])[:40] not in pg: miss+=1; print('NOT ON PAGE',m['module_id'],o['number'],o['text'][:80])
print('objectives checked',tot,'not found on cited page',miss)
print('errors',err)
print('handbook sources',sorted({m['source_id'] for m in M}))
print('size',os.path.getsize('work/manifest.json'))
print('review',[ (m['module_id'],[r['rule'] for r in m['scope_review']]) for m in M if m['scope_review']])
print('NP hits',{m['module_id']:len(r['objectives']) for m in M for r in m['scope_review'] if r['rule']=='Rule 8'})
print('drafts',[(w['file'],w['draft']['evidence'][0]) for w in W if w['draft']['flag']])
print('no text share',sum(w['slides_with_no_text'] for w in W),sum(w['slides'] for w in W))
print('sample',M[0]['topic'],M[0]['terminal_objectives'][0]['text'],M[0]['terminal_objectives'][0]['page'])
