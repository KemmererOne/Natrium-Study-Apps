#!/usr/bin/env python3
"""Build work/manifest.json from work/objectives.json, work/word_outline.json and the mapping below."""
import json,re,os,datetime
O=json.load(open('work/objectives.json')); W=json.load(open('work/word_outline.json'))
src=open('SOURCES.md',encoding='utf8').read()
SID={m[1].strip():(m[0].strip(),m[2].strip(),m[3].strip()) for m in re.findall(r'^\| ([^|]+)\| ([^|]+)\| ([^|]+)\| [^|]+\| ([^|]+)\|',src,re.M) for m in [m]} if False else {}
for l in src.splitlines():
    c=[x.strip() for x in l.rstrip('\\').split('|')]
    if len(c)>=7 and c[2].endswith(('.pdf','.docx')): SID[c[2]]=dict(id=c[1],document=c[3],use=c[5])
HB={'1010':'Classical Physics','1011':'Electrical Science','1012':'Thermodynamics, Heat Transfer, and Fluid Flow','1013':'Instrumentation and Control','1015':'Chemistry','1016':'Engineering Symbology, Prints, and Drawings','1017':'Material Science','1018':'Mechanical Science','1019':'Nuclear Physics and Reactor Theory'}
P,S='primary','supporting'
MAP={
'ES-07':[('AC Generator Theory and Operation',S,'AC generation, cycle and frequency, peak and RMS values, phase angles')],
'ES-09':[('AC Generator Theory and Operation',S,'Real and reactive power, power factor')],
'ES-10':[('AC Generator Theory and Operation',P,'Generator construction, operation and paralleling')],
'ES-14':[('Electrical Test Equipment',P,'Voltmeter, ammeter, synchroscope, ground detectors')],
'ES-15':[('Breakers, Relays, and Disconnects Part 1',P,'Circuit protection and interrupting devices'),('Breakers, Relays, and Disconnects Part 2',P,'Circuit breakers, control power, paralleling')],
'HT-01':[('Thermodynamic Units and Properties',P,'Base copy of the duplicate pair'),('Thermo Units and Properties',P,'Duplicate of the base copy'),('Basic Energy Concepts 6-11',P,'First and second laws, enthalpy'),('Thermodynamics',P,'Processes and laws applied to systems')],
'HT-02':[('Heat Transfer',P,'Heat transfer mechanisms and terms'),('Thermal Hydraulics',P,'Core heat transfer, fuel temperature profile, decay heat'),('Core Thermal Limits word',S,'Core thermal limits; adds content beyond the handbook objectives'),('Heat Exchangers',S,'Heat transfer in heat exchangers')],
'HT-03':[('Fluid Statics and Dynamics - Part 1',P,'Fluid properties, closed systems, flow rate'),('Fluid Statics and Dynamics - Part 2',P,'Bernoulli, flow changes'),('Thermal Hydraulics',S,'Natural circulation')],
'IC-01':[('Temperature Detectors',P,'')],'IC-02':[('Pressure Detectors',P,'')],'IC-03':[('Level Detectors',P,'')],'IC-04':[('Flow Detectors',P,'')],'IC-05':[('Position Indicators',P,'')],
'IC-06':[('Sensors and Detectors Part 2',P,'Radiation and nuclear instruments'),('Failed Fuel Detectors',S,'Neutron and failed fuel detectors; adds content beyond the handbook objectives')],
'IC-07':[('Controllers and Positioners',P,'Controllers, control stations, actuators'),('DISTRIBUTED CONTROL SYSTEMS (DCS)',S,'Digital control; no IC-07 enabling objective covers it')],
'CH-04':[('Demineralizers and Ion Exchangers',P,'Ion exchange and demineralizers')],
'ES-12':[('Variable Frequency Drives',S,'Motor speed control; no ES-12 objective covers it')],
'ME-02':[('Heat Exchangers',P,'')],
'ME-03':[('Pumps',P,'Centrifugal and positive displacement pumps'),('ALIP Pumps',S,'Electromagnetic sodium pump; no ME-03 enabling objective covers it')],
'ME-04':[('Valve Fundamentals',P,'')],
'NP-01':[('Neutrons',P,'Atoms, binding energy, interactions, fission')],
'NP-02':[('Source Neutrons',P,'Intrinsic and installed sources'),('Delayed Neutron Importance',P,'Prompt and delayed neutrons'),('Neutrons',S,'Prompt and delayed neutrons, flux, cross sections')],
'NP-03':[('Reactor Neutrons',P,'keff, reactivity, core design in a fast reactor'),('Reactivity Coefficients Module 1',P,'Coolant and void coefficients'),('Reactivity Coefficients - Module 2',P,'Fuel temperature coefficient, Doppler'),('Reactivity Coefficients Module 3',P,'Core expansion, power coefficient'),('Control Rods',P,'Rod worth and effects'),('Fuel Depletion',P,'Depletion and burnable poison')],
'NP-04':[('Subcritical Multiplication',P,''),('Power Changes',P,'Reactor period and startup rate'),('Delayed Neutron Importance',S,'Period and reactor control'),('Source Neutrons',S,'Why a startup source is needed')],
}
UNMAPPED={'Cold Traps and Sodium Coolant Purification':'Sodium system content. No handbook module covers it.',
'Plugging Temperature Indicators':'Sodium system content. No handbook module covers it.',
'Sodium Leak Detectors':'Sodium system content. No handbook module covers it.'}
UNMAPPED={}
EXTRA=[('NA-01','Cold Traps and Sodium Coolant Purification'),('NA-02','Plugging Temperature Indicators'),('NA-03','Sodium Leak Detectors')]
DUP={'Thermo Units and Properties':'Thermodynamic Units and Properties'}
DRAFT={'Reactivity Coefficients Module 3':[r'draft storyboard',r'Script: TBD'],
'Reactivity Coefficients Module 1':[r'TBD . once factors',r'Need information on factors',r'Need to verify numbers'],
'Cold Traps and Sodium Coolant Purification':[r'TBD based on design'],
'Heat Transfer':[r'^# 3\. Storyboard'],
'AC Generator Theory and Operation':[r'Need to replace the graphic']}
CAND={'Reactivity Coefficients - Module 2','Plugging Temperature Indicators','Electrical Test Equipment'}
OVER=[('Cold Traps and Sodium Coolant Purification','Plugging Temperature Indicators',0.48),('Reactivity Coefficients - Module 2','Reactivity Coefficients Module 3',0.366),('Reactivity Coefficients Module 1','Reactivity Coefficients Module 3',0.224),('Power Changes','Source Neutrons',0.224)]
RULE11={'CP','PR','MS'}; RULE11M={'ME-01','ME-05'}
SCOPE={'CH-02':('Rule 10','Check how much of this module is specific to water systems.'),
'CH-03':('Approved decision','Build the module, tagged Water-system only.'),
'CH-04':('Approved decision','Build the module and its Word file, tagged Water-system only.'),
'HT-01':('Rule 10','Steam tables and steam cycle material need the Water-system only tag.'),
'HT-02':('Rule 10','Boiling material needs the Water-system only tag.'),
'HT-03':('Rule 10','Two-phase and water examples need checking; this topic is fluid flow, not water heat transfer.')}
THERM=r'moderat|thermal (neutron|utiliz|flux|non|reactor|absorber)|thermalization|resonance|six factor|boron|chemical shim|xenon|samarium'
slug=lambda s:re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',s.lower().replace('&','and'))).strip('-')
txt={b:open(f'work/text/{b}.txt',errors='replace').read() for b in W}
def locate(b,pat):
    ref=None
    for l in txt[b].splitlines():
        m=re.match(r'^# (\d+(?:\.\d+)?)\.?\s',l)
        if m: ref=m[1]
        h=re.search(pat,l)
        if h:
            a=max(0,h.start()-30); return dict(section=ref,text=l[a:h.end()+50].lstrip('# ').strip())
    raise SystemExit('draft evidence not found: '+b+' '+pat)
mods=[]
for m in O['modules']:
    c=m['code']; hb=m['file'][9:13]; links=MAP.get(c,[])
    t=[dict(number=x['number'],text=x['text'],items=x['items'],page=x['page'],
        enabling=[dict(number=e['number'],text=e['text'],items=e['items'],page=e['page']) for e in x['enabling']]) for x in m['terminal']]
    review=[]
    if c in SCOPE: review.append(dict(rule=SCOPE[c][0],note=SCOPE[c][1]))
    if c.startswith('NP'):
        hits=[o['number'] for x in m['terminal'] for o in [x]+x['enabling'] if re.search(THERM,o['text']+' '+' '.join(o['items']),re.I)]
        if hits: review.append(dict(rule='Rule 8',note='Objectives that name thermal-spectrum or moderator content.',objectives=hits))
    drafts=[l[0] for l in links if l[0] in DRAFT]
    if drafts: review.append(dict(rule='Rule 5',note='Uses a draft Word file, so the topic takes the Draft source tag.',files=[d+'.docx' for d in drafts]))
    mods.append(dict(module_id=c,handbook=m['designation'],handbook_title=HB[hb],source_id=m['source_id'],file=m['file'],volume=m['volume'],module_number=int(c[3:]),title=m['title'],
        objective_pages=m['objective_pages'],terminal_count=len(t),enabling_count=sum(len(x['enabling']) for x in t),terminal_objectives=t,
        mapping='word files' if links else 'handbook only',word_files=[dict(file=f+'.docx',role=r,note=n) for f,r,n in links],
        gap_topic=(c[:2] in RULE11 or c in RULE11M),topic=dict(slug=slug(c+' '+m['title']),status='Draft'),scope_tags=[],scope_review=review))
for c,t in EXTRA:
    drafts=[t] if t in DRAFT else []
    mods.append(dict(module_id=c,handbook=None,handbook_title='Sodium Systems',source_id=None,file=None,volume=None,module_number=int(c[3:]),title=t,objective_pages=[],terminal_count=0,enabling_count=0,terminal_objectives=[],
        objectives_note='No handbook objectives. Objectives come from the Word file when this topic is built.',mapping='word only',word_files=[dict(file=t+'.docx',role=P,note='Added sodium topic')],gap_topic=False,topic=dict(slug=slug(c+' '+t),status='Draft'),scope_tags=[],
        scope_review=[dict(rule='Rule 5',note='Uses a draft Word file, so the topic takes the Draft source tag.',files=[d+'.docx' for d in drafts])] if drafts else []))
    MAP[c]=[(t,P,'Added sodium topic')]
mapped={}
for c,l in MAP.items():
    for f,r,n in l: mapped.setdefault(f,[]).append(dict(module_id=c,role=r))
words=[]
for b,v in W.items():
    sl=[s for s in v['sections'] if s['kind']=='slide']
    ev=[locate(b,p) for p in DRAFT.get(b,[])]
    ov=[dict(file=(y if x==b else x)+'.docx',shared_text=k) for x,y,k in OVER if b in(x,y)]
    dup=None
    if b in DUP: dup=dict(flag=True,role='duplicate',base=DUP[b]+'.docx',evidence='Identical extracted text, 158 of 158 embedded files, and metadata. The two files differ only in zip packaging.')
    elif b in DUP.values(): dup=dict(flag=True,role='base',duplicate=[k+'.docx' for k,x in DUP.items() if x==b],evidence='Identical extracted text, 158 of 158 embedded files, and metadata. The two files differ only in zip packaging.')
    else: dup=dict(flag=False)
    s=SID.get(v['file'],{})
    words.append(dict(file=v['file'],source_id=s.get('id'),title=txt[b].splitlines()[0].lstrip('# ').strip(),sources_md_use=s.get('use'),
        slides=len(sl),slides_with_notes=sum(x['notes'] for x in sl),slides_with_no_text=sum(1 for x in sl if x['chars']==0),knowledge_checks=sum(x['question'] for x in sl),images=v['images'],
        duplicate=dup,draft=dict(flag=bool(ev),evidence=ev,scope='Scene 3 only' if b=='Heat Transfer' else ('whole file' if ev else None)),
        possible_draft=b in CAND,partial_overlaps=ov,modules=mapped.get(b,[]),unmapped_reason=UNMAPPED.get(b),
        outline=[dict(ref=x['ref'],title=x['title'],kind=x['kind'],notes=x['notes'],knowledge_check=x['question'],layers=x['layers'],no_text=(x['kind']=='slide' and x['chars']==0)) for x in v['sections']]))
hb=[]
for v in O['volumes']:
    hb.append(dict(v,modules=[m['module_id'] for m in mods if m['source_id']==v['source_id']]))
out=dict(generated=datetime.date.today().isoformat(),status='Approved at Step 1 review, Nov 5, 2026',
 summary=dict(handbook_volumes=len(hb),modules=sum(1 for m in mods if m['handbook']),topics=len(mods),terminal_objectives=sum(m['terminal_count'] for m in mods),enabling_objectives=sum(m['enabling_count'] for m in mods),
  modules_with_word_files=sum(m['mapping']=='word files' for m in mods),modules_handbook_only=sum(m['mapping']=='handbook only' for m in mods),gap_topics=sum(m['gap_topic'] for m in mods),
  word_files=len(words),word_duplicates=sum(1 for w in words if w['duplicate'].get('role')=='duplicate'),word_drafts=sum(w['draft']['flag'] for w in words),word_possible_drafts=sum(w['possible_draft'] for w in words),word_unmapped=sum(1 for w in words if not w['modules'])),
 extraction_notes=['Objective text comes from pdftotext -layout. 15 objectives had kerning breaks repaired (DESCRIB E to DESCRIBE, W RITE to WRITE); no wording changed.',
  'In PR-04 objective 1.1, item l prints as 1 in the PDF text and is labeled l here.',
  'NP-01 objective 1.4 shows the stacked A, Z, X notation as AZX in PDF text. Exponents and stacked notation can flatten in both PDF and Word text.',
  'PR-06 title comes from the handbook overview because its running head wraps.'],
 handbooks=hb,modules=mods,word_files=words)
json.dump(out,open('work/manifest.json','w'),indent=1,ensure_ascii=False)
print(json.dumps(out['summary'],indent=0))
