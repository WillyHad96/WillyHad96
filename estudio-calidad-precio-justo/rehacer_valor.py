# REHECHO 2 — el efecto valor por sector (C21, C23, C24) con retornos verificados
# y el indice en las fechas exactas de cada posicion.
import collections, numpy as np
from base_lib import *
ev=carga()
print(f"decisiones: {len(ev)}")
SEC=collections.Counter(e['sector'] for e in ev)
print()
print("="*104)
print("CUARTIL BARATO POR P/S DENTRO DE CADA SECTOR — alfa INTERNO (contra su propio sector)")
print("="*104)
print("  sector                 obs  n/anho    CAGR   sector   alfa int     t   pares impar  corr(QQQ)")
print("  " + "-"*100)
rng=np.random.default_rng(17)
res={}
for sec,_ in SEC.most_common():
    sub=[e for e in ev if e['sector']==sec]
    by=collections.defaultdict(list)
    for e in sub: by[e['yr']].append(e)
    yrs=[y for y in sorted(by) if len(by[y])>=8]
    if len(yrs)<14: continue
    car=[];fam=[];q=[];ns=[]
    for y in yrs:
        pool=sorted(by[y],key=lambda e:e['ps']); k=max(1,int(round(len(pool)*0.25)))
        car.append(np.mean([e['ret'] for e in pool[:k]])/100)
        fam.append(np.mean([e['ret'] for e in by[y]])/100)
        q.append(np.mean([e['qqq'] for e in pool[:k]])/100); ns.append(k)
    car=np.array(car);fam=np.array(fam);q=np.array(q)
    a=(cagr(car)-cagr(fam))*100
    d=[]
    for _ in range(1500):
        c=[]
        for i,y in enumerate(yrs):
            r=np.array([e['ret'] for e in by[y]])/100
            c.append(r[rng.choice(len(r),ns[i],replace=False)].mean())
        d.append((cagr(c)-cagr(fam))*100)
    se=np.std(d,ddof=1)
    P=[i for i,y in enumerate(yrs) if y%2==0]; I=[i for i,y in enumerate(yrs) if y%2==1]
    ap=(cagr(car[P])-cagr(fam[P]))*100; ai=(cagr(car[I])-cagr(fam[I]))*100
    cr=np.corrcoef(car,q)[0,1]
    res[sec]=dict(a=a,t=a/se,ap=ap,ai=ai,cagr=cagr(car),corr=cr,n=np.mean(ns),q=cagr(q))
    marca='  <<<' if abs(a/se)>2 and ap>0 and ai>0 else ''
    print(f"  {sec:<20} {len(sub):>5}  {np.mean(ns):>5.0f}  {100*cagr(car):>6.2f}% {100*cagr(fam):>6.2f}%  "
          f"{a:>+7.2f} pp {a/se:>5.2f}  {ap:>5.1f} {ai:>5.1f}   {cr:>6.3f}{marca}")
import json; json.dump({k:{kk:float(vv) for kk,vv in v.items()} for k,v in res.items()},open('/tmp/valor_sec.json','w'))
