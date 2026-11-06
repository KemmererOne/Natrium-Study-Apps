#!/usr/bin/env python3
"""Crop handbook figures. Finds each caption with pdftotext -bbox, and the figure from the
vector paths on the page (pdftocairo -svg). Writes work/figs/<module>-fig<N>.png and figs.json."""
import re,subprocess,json,os,sys,html
PICK={
 ('DOE-HDBK-1010-92','CP-02'):[2,3,10,12,13,18,21,24],
 ('DOE-HDBK-1010-92','CP-03'):[1],
 ('DOE-HDBK-1010-92','CP-04'):[1,3,5,7,9,10,12],
 ('DOE-HDBK-1011-92_VOL1','ES-01'):[7,10,13,22,27,28,29,30],
 ('DOE-HDBK-1011-92_VOL1','ES-02'):[6,8,9,10,11,12,13,14,15,16,17,31,35,53,56],
 ('DOE-HDBK-1011-92_VOL2','ES-03'):[7,10,11,18],
 ('DOE-HDBK-1011-92_VOL2','ES-04'):[1,2,4,5,6,7,8],
 ('DOE-HDBK-1011-92_VOL2','ES-05'):[2,3,4,5,6,8,9,10,11,12,13],
 ('DOE-HDBK-1011-92_VOL2','ES-06'):[2,4,5,6,7,8,9],
 ('DOE-HDBK-1011-92_VOL3','ES-07'):[1,2,3,4,5],
 ('DOE-HDBK-1011-92_VOL3','ES-08'):[1,2,3,4,5,8,10],
 ('DOE-HDBK-1011-92_VOL3','ES-09'):[1,2,3,10,11,13,16],
 ('DOE-HDBK-1011-92_VOL3','ES-10'):[1,2,4,5,6,8,9,10,11],
 ('DOE-HDBK-1011-92_VOL3','ES-11'):[1],
 ('DOE-HDBK-1011-92_VOL4','ES-12'):[1,2,3,4,6,8,9],
 ('DOE-HDBK-1011-92_VOL4','ES-13'):[1,3,4,5,8],
 ('DOE-HDBK-1011-92_VOL4','ES-14'):[1,2,3,4,6,8,9,11,16,17],
 ('DOE-HDBK-1011-92_VOL4','ES-15'):[1,2,5,7,12,13,15,16,19],
 ('DOE-HDBK-1012-92_VOL1','HT-01'):[1,2,4,5,7,9,13,14,15,19,20,21,24,31,35,40],
 ('DOE-HDBK-1012-92_VOL2','HT-02'):[2,5,6,7,8,9,10,13,14,15,17],
 ('DOE-HDBK-1012-92_VOL3','HT-03'):[1,2,5,6,7,8,9,10,11,12,13,14],
 ('DOE-HDBK-1013-92-VOL1','IC-01'):[1,2,3,5,6,8,9,10,11,12],
 ('DOE-HDBK-1013-92-VOL1','IC-02'):[1,2,3,4,5,6,7,8,9,10],
 ('DOE-HDBK-1013-92-VOL1','IC-03'):[1,5,6,7,8,9,10,11,15],
 ('DOE-HDBK-1013-92-VOL1','IC-04'):[1,2,3,4,5,6,7,8,9,11],
 ('DOE-HDBK-1013-92-VOL1','IC-05'):[1,2,3,4,5,6,7],
 ('DOE-HDBK-1013-92-VOL2','IC-06'):[1,2,3,4,5,6,7,9,14,16,19,20,21,24,25,26,27,29,35,36,37],
 ('DOE-HDBK-1013-92-VOL2','IC-07'):[2,3,4,8,9,10,12,13,14,17,19,22,27,30,32,34,35,36,37,38,39],
 ('DOE-HDBK-1015-93_VOL1','CH-01'):[1,4,5,6,7,8],
 ('DOE-HDBK-1015-93_VOL1','CH-02'):[1,2,3,5,7,10,11,12,14],
 ('DOE-HDBK-1015-93_VOL2','CH-03'):[2],
 ('DOE-HDBK-1015-93_VOL2','CH-04'):[3,4],
 ('DOE-HDBK-1015-93_VOL2','CH-05'):[5,6,7,8,9],
 ('DOE-HDBK-1016-93_VOL1','PR-01'):[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],
 ('DOE-HDBK-1016-93_VOL1','PR-02'):list(range(1,33)),
 ('DOE-HDBK-1016-93_VOL1','PR-03'):[1,2,3,4,5,6,7,8,9,10,14,15,16,17,18],
 ('DOE-HDBK-1016-93_VOL2','PR-04'):[1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17],
 ('DOE-HDBK-1016-93_VOL2','PR-05'):list(range(1,15)),
 ('DOE-HDBK-1016-93_VOL2','PR-06'):[1,2,4,5,6,7,8,9,10,11],
 ('DOE-HDBK-1017-93_VOL1','MS-01'):list(range(1,10)),
 ('DOE-HDBK-1017-93_VOL1','MS-02'):[1,2,3,4,6,7,9,10],
 ('DOE-HDBK-1017-93_VOL2','MS-03'):[2,3],
 ('DOE-HDBK-1017-93_VOL2','MS-04'):[1,2,3],
 ('DOE-HDBK-1017-93_VOL2','MS-05'):[1,2,3,4],
 ('DOE-HDBK-1018-93_VOL1','ME-01'):[2,3,6,7,10,15,16,17,18,19,20,21,22,23,24,25,26,28],
 ('DOE-HDBK-1018-93_VOL1','ME-02'):[1,2,3,4,5,6,7,8,9],
 ('DOE-HDBK-1018-93_VOL1','ME-03'):[1,3,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21],
 ('DOE-HDBK-1019-93_VOL1','NP-01'):[1,2,6,7,9,10,11,12,14,15,16,17,18,19,20,21,22],
 ('DOE-HDBK-1019-93_VOL1','NP-02'):[1,2,3],
 ('DOE-HDBK-1019-93_VOL2','NP-03'):[3,8,9,10,11],
 ('DOE-HDBK-1019-93_VOL2','NP-04'):[1,2,3,5],
 ('DOE-HDBK-1018-93_VOL2','ME-05'):[1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23,24],
 ('DOE-HDBK-1018-93_VOL2','ME-04'):[1,2,3,4,9,12,13,14,15,16,18,19,20,22,24,27,28,29,30,31,32,33,34,35],
}
BOX={'np-01-fig2':[400,72,560,236],'me-05-fig4':[298,82,568,305],'me-05-fig6':[262,82,532,323],'me-05-fig17':[262,82,532,287],'me-05-fig18':[116,462,460,690],'me-04-fig27':[44,82,360,449],'me-04-fig9':[304,82,568,421],'me-04-fig31':[90,82,384,341],'me-04-fig34':[246,82,568,575],'me-03-fig17':[80,82,330,359],'me-03-fig19':[145,245,431,525],'me-01-fig21':[116,151,296,369],'me-01-fig22':[298,151,460,369],'pr-06-fig6':[98,94,564,510],'pr-06-fig7':[62,94,528,704],'pr-06-fig8':[179,302,487,705],'pr-06-fig9':[172,296,562,708],'pr-06-fig10':[112,338,485,512],'pr-06-fig11':[98,130,564,412],'ms-02-fig10':[330,74,550,208],'ms-03-fig2':[320,76,550,298],'ms-04-fig1':[26,76,228,255],'pr-02-fig7':[286,88,562,350],'pr-02-fig8':[232,84,532,407],'pr-02-fig11':[246,84,532,443],'pr-02-fig15':[44,88,532,623],'pr-02-fig27':[250,84,532,377],'pr-05-fig5':[338,74,524,264],'pr-03-fig10':[44,178,532,370],'pr-01-fig13':[104,92,478,282],'pr-01-fig14':[50,425,530,675],'pr-01-fig16':[60,285,538,655],'pr-04-fig1':[118,104,702,560],'pr-04-fig2':[116,85,700,540],'pr-04-fig16':[70,85,510,490],'pr-05-fig1':[132,108,680,478],'pr-05-fig10':[168,76,500,584],'ch-02-fig2':[288,76,568,240],'ch-02-fig7':[326,76,576,262],'ic-06-fig7':[240,230,586,483],'ic-02-fig2':[232,293,514,533],'ht-03-fig13':[212,366,514,674],'ht-03-fig1':[152,374,532,675],'es-13-fig1':[26, 69, 514, 379],'es-13-fig4':[98, 69, 586, 271],'es-12-fig9':[74, 255, 538, 547],'es-06-fig8':[278,323,586,541],'es-04-fig7':[186,342,514,658],'cp-04-fig12':[234,397,527,633]}
TITLES={'np-02-fig2':'Prompt Fission Neutron Energy Spectrum for Thermal Fission of Uranium-235','np-02-fig3':'Comparison of Neutron Flux Spectra for Thermal and Fast Breeder Reactor','np-01-fig2':'Nomenclature for Identifying Nuclides','np-01-fig21':'Uranium-235 Fission Yield vs. Mass Number','ms-05-fig1':'Nominal Stress-Strain Curve vs True Stress-Strain Curve','ms-05-fig4':'Qualitative Representation of Neutron Irradiation Effect on Many Metals','me-02-fig4':'Counter Flow Heat Exchanger','ms-04-fig1':'Basic Fracture Types','ms-02-fig3':'Typical Ductile Material Stress-Strain Curve','pr-02-fig19':'Fluid Power Pump and Compressor Symbols','pr-03-fig9':'Comparison of an Electrical Schematic and a Pictorial Diagram','pr-04-fig15':'Example Combination Diagram of Electrical Single Line, and Block Diagram','ch-02-fig1':'Formation of Ferrous (Fe++) Ions in the Corrosion of Iron','ch-02-fig7':'Effect of pH on the Corrosion Rate of Iron in Water','ch-05-fig9':'Storage Container With Spring-loaded Cover','ch-01-fig7':'Covalent Bond, Methane CH4','ic-03-fig15':'Block Diagram of a Differential Pressure Level Detection Circuit','ic-07-fig22':'Response of Proportional Plus Reset Control','ic-07-fig14':'Relation Between Valve Position and Controlled Variable Under Proportional Mode','ic-07-fig4':'Relationships of Functions and Elements in an Automatic Control System','ht-02-fig17':'Radial Temperature Profile Across a Fuel Rod and Coolant Channel','ic-01-fig5':'Internal Construction of a Typical Thermocouple','ic-01-fig12':'Resistance Thermometer Circuit with Precision Resistor in Place of Resistance Bulb','ht-03-fig7':'Typical Centrifugal Pump Characteristic Curve','ht-03-fig11':'Pump Characteristic Curve for Two Identical Centrifugal Pumps Used in Parallel','ht-03-fig13':'Pump Characteristic Curve for Two Identical Centrifugal Pumps Used in Series','ht-01-fig24':'Expansion and Compression Processes on T-s Diagram','es-15-fig7':'Simple Circuit Breaker Control Circuit - Breaker Open','es-08-fig3':'Voltage, Charge, and Current in a Capacitor','es-10-fig6':'Simple AC Generator - Rotating Field, Stationary Armature','es-01-fig22':'Left-hand Rule for Current Carrying Conductors'}
ROT=('pr-01-fig11','pr-02-fig18','pr-04-fig15')  # drawings printed sideways on the page
FOOT=re.compile(r'(?:Page\s+(\S+)\s+([A-Z]{2}-\d\d)|([A-Z]{2}-\d\d)\s+Page\s+(\S+))')
def words(pdf,p):
    t=subprocess.run(['pdftotext','-bbox','-f',str(p),'-l',str(p),pdf,'-'],capture_output=True,text=True,errors='replace').stdout
    return [(float(a),float(b),float(c),float(d),html.unescape(w)) for a,b,c,d,w in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',t)]
def paths(pdf,p):
    svg=subprocess.run(['pdftocairo','-svg','-f',str(p),'-l',str(p),pdf,'-'],capture_output=True,text=True,errors='replace').stdout
    svg=re.sub(r'<defs>.*?</defs>','',svg,flags=re.S)
    out=[]
    for m in re.finditer(r'<(?:path|rect)\b[^>]*>',svg):
        tag=m[0]; d=re.search(r'\bd="([^"]*)"',tag)
        tr=re.search(r'transform="matrix\(([^)]*)\)"',tag)
        a,b,c,dd,e,f=(1,0,0,1,0,0)
        if tr: a,b,c,dd,e,f=[float(x) for x in re.split(r'[ ,]+',tr[1].strip())]
        if not d: continue
        n=[float(x) for x in re.findall(r'-?\d+\.?\d*',d[1])]
        pts=[(a*n[i]+c*n[i+1]+e,b*n[i]+dd*n[i+1]+f) for i in range(0,len(n)-1,2)]
        if not pts: continue
        xs,ys=zip(*pts); out.append((min(xs),min(ys),max(xs),max(ys)))
    return [q for q in out if not (q[2]-q[0]>=600 and q[3]-q[1]>=780)]
def cluster(boxes,gap=14):
    cl=[]
    for b in sorted(boxes,key=lambda q:(q[1],q[0])):
        hit=[c for c in cl if b[0]-gap<=c[2] and c[0]-gap<=b[2] and b[1]-gap<=c[3] and c[1]-gap<=b[3]]
        n=list(b)
        for c in hit:
            n=[min(n[0],c[0]),min(n[1],c[1]),max(n[2],c[2]),max(n[3],c[3])]; cl.remove(c)
        cl.append(n)
    ch=True
    while ch:
        ch=False
        for i in range(len(cl)):
            for j in range(i+1,len(cl)):
                a,b=cl[i],cl[j]
                if b[0]-gap<=a[2] and a[0]-gap<=b[2] and b[1]-gap<=a[3] and a[1]-gap<=b[3]:
                    cl[i]=[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])]; del cl[j]; ch=True; break
            if ch: break
    return cl
out={}
for (name,mod),nums in PICK.items():
    pdf=f'sources/{name}.pdf'; raw=open(f'work/text/{name}.txt',errors='replace').read().split('\f')
    for n in nums:
        page=None
        for i,p in enumerate(raw):
            ft=FOOT.findall(p)
            if not ft or not any((x[1] or x[2])==mod for x in ft): continue
            label=(ft[-1][0] or ft[-1][3])
            if not label.isdigit(): continue
            if (mod,n)==('NP-01',9) and label!='28': continue
            if (mod,n)==('NP-04',1) and label=='8': page=(i+1,label,'1/M Plot vs. Rod Withdrawal'); break
            if (mod,n)==('ME-03',21) and label=='27': page=(i+1,label,'Positive Displacement Pump Characteristic Curve'); break
            if re.search(rf'^\s*.*\bFigure {n}\s{{1,8}}[-A-Z234]',p,re.M) and not re.search(r'\. \. \. \.',p):
                # a caption line: Figure N followed by a title, not a text reference
                m=re.search(rf'Figure {n}\s{{1,8}}([-A-Z234][^\n]*?)(?:\s{{3,}}|$)',p,re.M)
                if m and not re.search(r'^(shows|is|and)\b|\(',m[1][:5]): page=(i+1,label,m[1].strip(' -')); break
        if not page: print('NO CAPTION',mod,n); continue
        pg,label,title=page
        stem=f'{mod.lower()}-fig{n}'
        if stem in BOX:
            x0,y0,x1,y1=BOX[stem]; s=150/72
            subprocess.run(['pdftoppm','-f',str(pg),'-l',str(pg),'-r','150','-gray','-png','-singlefile','-x',str(int(x0*s)),'-y',str(int(y0*s)),'-W',str(int((x1-x0)*s)),'-H',str(int((y1-y0)*s)),pdf,f'work/figs/{stem}'],check=True)
            out[stem]=dict(module=mod,num=n,title=TITLES.get(stem,title),pdf=pg,page=label,box=[round(v) for v in (x0,y0,x1,y1)],bytes=os.path.getsize(f'work/figs/{stem}.png'))
            continue
        w=words(pdf,pg)
        cap=[x for k,x in enumerate(w) if x[4]=='Figure' and k+1<len(w) and w[k+1][4]==str(n) and abs(w[k+1][1]-x[1])<3]
        if not cap: print('NO BBOX',mod,n,pg); continue
        c=cap[-1]
        ps=[q for q in paths(pdf,pg) if q[3]<745 and q[1]>45 and (q[2]-q[0]>0.5 or q[3]-q[1]>0.5)]
        cl=cluster(ps)
        best=None
        for b in cl:
            area=(b[2]-b[0])*(b[3]-b[1])
            if area<400: continue
            dx=max(b[0]-c[2],c[0]-b[2],0); dy=max(b[1]-c[3],c[1]-b[3],0)
            sc=dx+dy*1.0+(30 if b[1]>c[3] else 0)
            if best is None or sc<best[0]: best=(sc,b)
        if not best: print('NO PATHS',mod,n,pg,len(ps)); continue
        b=best[1]
        x0,y0,x1,y1=b[0]-10,b[1]-10,b[2]+10,b[3]+10
        # take in labels that sit just outside the drawn lines: short words in the margin
        R=150; s=R/72
        stem=f'{mod.lower()}-fig{n}'
        x0=max(x0,20);y0=max(y0,40);x1=min(x1,595);y1=min(y1,750)
        if stem[:2]=='ch': y0=max(y0,76)
        if stem[:2] in ('pr','ms','me'): y0=max(y0,82)
        if stem[:2]=='np': y0=max(y0,72)
        if stem in BOX: x0,y0,x1,y1=BOX[stem]
        subprocess.run(['pdftoppm','-f',str(pg),'-l',str(pg),'-r',str(R),'-gray','-png','-singlefile','-x',str(int(x0*s)),'-y',str(int(y0*s)),'-W',str(int((x1-x0)*s)),'-H',str(int((y1-y0)*s)),pdf,f'work/figs/{stem}'],check=True)
        out[stem]=dict(module=mod,num=n,title=TITLES.get(stem,title),pdf=pg,page=label,box=[round(v) for v in (x0,y0,x1,y1)],bytes=os.path.getsize(f'work/figs/{stem}.png'))
for k in ROT: subprocess.run(['sips','-r','90',f'work/figs/{k}.png'],capture_output=True,check=True)
json.dump(out,open('work/figs/figs.json','w'),indent=0)
print(len(out),'figures',sum(v['bytes'] for v in out.values())//1024,'KB')
rows=''.join(f'<figure><img src="{k}.png"><figcaption>{k} p.{v["page"]}: {v["title"]}</figcaption></figure>' for k,v in out.items() if k[:5] in ('np-01','np-02','np-03','np-04'))
open('work/figs/sheet.html','w').write('<!doctype html><meta charset=utf-8><style>body{margin:6px;background:#fff;font:11px sans-serif;columns:3;column-gap:6px}figure{margin:0 0 6px;break-inside:avoid;border:1px solid #c33;padding:2px}img{width:100%}</style>'+rows)
