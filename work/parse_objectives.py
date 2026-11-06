#!/usr/bin/env python3
"""Parse terminal and enabling objectives from the DOE handbooks into work/objectives.json.
Reads pdftotext -layout output page by page, so every objective keeps its PDF and printed page."""
import re,glob,os,subprocess,json,sys
SRC={'1010':'DOE-1010','1011':'DOE-1011','1012':'DOE-1012','1013':'DOE-1013','1015':'DOE-1015','1016':'DOE-1016','1017':'DOE-1017','1018':'DOE-1018','1019':'DOE-1019'}
def pages(pdf):
    t=subprocess.run(['pdftotext','-layout',pdf,'-'],capture_output=True,text=True,errors='replace').stdout
    return t.split('\f')
FOOT=re.compile(r'^[\s.]*(?:Rev\.\s*\d+\s+Page\s+(\S+)\s+([A-Z]{2,3}-\d+)|([A-Z]{2,3}-\d+)\s+Page\s+(\S+)\s+Rev\.\s*\d+)\s*$')
HEAD=re.compile(r'DOE-HDBK-10\d\d(?:/\d)?-9\d')
def footer(pg):
    for l in reversed(pg.splitlines()):
        m=FOOT.match(l)
        if m: return (m[2] or m[3]),(m[1] or m[4])
    return None,None
def header_title(pg):
    for l in pg.splitlines():
        if not l.strip(): continue
        m=re.match(r'^\s*(.+?)\s+OBJECTIVES\s*$',l) or re.match(r'^\s*OBJECTIVES\s+(.+?)\s*$',l)
        if m and not HEAD.search(l): return re.sub(r'\s+',' ',m[1])
        break
    for l in pg.splitlines():
        m=HEAD.search(l)
        if m:
            for side in (l[:m.start()],l[m.end():]):
                t=re.sub(r'\s+',' ',side).strip()
                if t and t.replace(' ','').upper()!='OBJECTIVES' and not t.replace(' ','').upper().startswith('OBJECTIVES'): return t
    return None
def clean_lines(pg):
    out=[]
    for l in pg.splitlines():
        if not l.strip() or FOOT.match(l) or HEAD.search(l): continue
        if not re.match(r'^\s*(TERMINAL|ENABLING)\s+OBJECTIVE',l) and not NUM.match(l) and (re.search(r'\sOBJECTIVES\s*$',l) or re.match(r'^\s*OBJECTIVES\s+\S',l)): continue
        out.append(l.rstrip())
    return out
NUM=re.compile(r'^\s*(\d{1,2}\.\d{1,2})\s+(\S.*)$')
SUB=re.compile(r'(?:^|\s{2,})([a-z]{1,2}|1)\.\s+(\S.*?)(?=\s{3,}(?:[a-z]{1,2}|1)\.\s|$)')
def fix(s):
    "Repair kerning breaks from PDF text only; wording is unchanged."
    s=re.sub(r'\s+',' ',s).strip()
    s=re.sub(r'\b([A-Z]{3,}) ([A-Z])\b(?= |,|$)',lambda m:m[1]+m[2] if m[2] not in('A','I') else m[0],s)
    s=re.sub(r'\b([A-Z]) ([A-Z]{3,})\b',lambda m:m[1]+m[2] if m[1] not in('A','I') else m[0],s)
    return s
mods=[];vols=[]
for pdf in sorted(glob.glob('sources/DOE-HDBK-10*.pdf')):
    fn=os.path.basename(pdf); hb=fn[9:13]; v=re.search(r'VOL(\d)',fn); vol=int(v[1]) if v else 1
    sid=SRC[hb]+(f'-V{vol}' if v else '')
    P=pages(pdf); desig=None
    for pg in P[:4]:
        m=re.search(r'DOE-HDBK-10\d\d(?:/\d)?-9\d',pg)
        if m: desig=m[0]; break
    vols.append(dict(source_id=sid,file=fn,designation=desig,pdf_pages=len([p for p in P if p.strip()])))
    cur=None; state=None; last=None
    for i,pg in enumerate(P):
        if not re.search(r'OBJECTIVES',pg.split('\n\n\n')[0]) and not re.search(r'(TERMINAL|ENABLING)\s+OBJECTIVE',pg): continue
        if not re.search(r'^\s*(TERMINAL OBJECTIVE|ENABLING OBJECTIVE ?S)',pg,re.M) : continue
        code,pl=footer(pg); title=header_title(pg)
        ref=dict(pdf=i+1,printed=pl)
        if code is None: print('NOFOOT',fn,i+1,file=sys.stderr)
        if cur and cur['code']==code and not cur['title']: cur['title']=title
        if not cur or cur['code']!=code:
            cur=dict(code=code,title=title,source_id=sid,designation=desig,file=fn,volume=vol,terminal=[],orphans=[],objective_pages=[])
            mods.append(cur); state=None; last=None
        cur['objective_pages'].append(ref)
        for l in clean_lines(pg):
            s=l.strip()
            if re.match(r'^TERMINAL OBJECTIVES?(\s*\(.*\))?$',s): state='T'; last=None; continue
            if re.match(r'^ENABLING OBJECTIVE ?S?(\s*\(.*\))?$',s): state='E'; last=None if state!='E' else last; continue
            if re.match(r'^(Page\s+\S+|Intentionally Left Blank|OBJECTIVES)$',s,re.I): continue
            n=NUM.match(l)
            if n and state:
                it=dict(number=n[1],raw=n[2],page=dict(ref),items=[])
                if state=='T': it['enabling']=[]; cur['terminal'].append(it)
                else:
                    if cur['terminal']: cur['terminal'][-1]['enabling'].append(it)
                    else: cur['orphans'].append(it)
                last=it; continue
            if last is None:
                if state and s: cur['orphans'].append(dict(raw=s,page=dict(ref)))
                continue
            subs=SUB.findall(l) if re.match(r'^\s+(?:[a-z]{1,2}|1)\.\s',l) else []
            if subs:
                for a,b in subs:
                    # columns set closer than the usual gap
                    for j,part in enumerate(re.split(r'\s+(?=[a-z]\.\s+[A-Z])',b.strip())):
                        if j==0: last['items'].append([a,part])
                        else: last['items'].append([part[0],part[2:].strip()])
            elif last['items'] and len(l)-len(l.lstrip())>=12:
                # wrapped sub-item, or a second column continuing
                last['items'][-1][1]+=' '+s
            else:
                last['raw']+=' '+s
    
for m in mods:
    for t in m['terminal']:
        for o in [t]+t['enabling']:
            o['text']=fix(o['raw'])
            exp=[]
            for a,b in o['items']:
                ps=re.split(r'\s+(?=[a-z]\.\s+[A-Z])',b)
                exp.append([a,ps[0]])
                exp+= [[q[0],q[2:].strip()] for q in ps[1:]]
            o['items']=exp
            o['items']=[f"{'l' if a=='1' else a}. {fix(b)}" for a,b in sorted(o['items'],key=lambda x:(len(x[0]),'l' if x[0]=='1' else x[0]))]
for m in mods:
    if m['code']=='PR-06': m['title']='Engineering Fabrication, Construction, and Architectural Drawings'  # title wraps in the running head; wording from the handbook overview
json.dump(dict(volumes=vols,modules=mods),open('work/objectives.json','w'),indent=1,ensure_ascii=False)
print('modules',len(mods),'terminal',sum(len(m['terminal']) for m in mods),'enabling',sum(len(t['enabling']) for m in mods for t in m['terminal']))
