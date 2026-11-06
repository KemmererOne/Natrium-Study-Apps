import re,glob,os,json,zipfile
out={}
for f in sorted(glob.glob('sources/*.docx')):
    b=os.path.basename(f)[:-5]; lines=open(f'work/text/{b}.txt',errors='replace').read().splitlines()
    secs=[];cur=None
    for l in lines[1:]:
        m=re.match(r'^# (\d+)\.\s+(.*)$',l)
        s=re.match(r'^# (\d+\.\d+)\s+(.*)$',l)
        y=re.match(r'^# (.*) \(Slide Layer\)$',l)
        if y:
            if cur: cur['layers']+=1
        elif s or m:
            cur=dict(ref=(s or m)[1],title=(s or m)[2].strip(),kind='slide' if s else 'scene',layers=0,chars=0,notes=False,question=False); secs.append(cur)
        elif cur:
            cur['chars']+=len(l)
            if l.startswith('Notes:'): cur['notes']=True
            if re.match(r'^\((Text Entry|Drag and Drop|Multiple|True|Matching|Sequence|Hot|Pick|Numeric|Fill)',l): cur['question']=True
    z=zipfile.ZipFile(f)
    imgs=[n for n in z.namelist() if re.search(r'\.(png|jpe?g|gif|emf|wmf|bin)$',n,re.I) and 'media' in n]
    out[b]=dict(file=b+'.docx',sections=secs,images=len(imgs),chunks=len([n for n in z.namelist() if 'afchunk' in n]))
json.dump(out,open('work/word_outline.json','w'),indent=0,ensure_ascii=False)
for b,v in out.items():
    sl=[s for s in v['sections'] if s['kind']=='slide']; sc=[s for s in v['sections'] if s['kind']=='scene']
    bare=sum(1 for s in sl if s['chars']==0)
    print(f"\n## {b} | scenes {len(sc)} slides {len(sl)} notes {sum(s['notes'] for s in sl)} bare {bare} checks {sum(s['question'] for s in sl)} images {v['images']} chunks {v['chunks']}")
    print('  scenes:',' / '.join(s['title'][:40] for s in sc)[:220])
    print('  slides:',' / '.join(s['title'][:32] for s in sl[:16])[:430])
