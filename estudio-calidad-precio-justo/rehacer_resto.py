# REHECHO 6 — el resto de lo que pesaba: valor neutral por sector con su t,
# el centinela 'desconocido' (A4), y los subtipos ciclicos (C20).
import collections, numpy as np
from base_lib import *
ev=carga(); rng=np.random.default_rng(53)
byY=collections.defaultdict(lambda: collections.defaultdict(list))
for e in ev:
    if e['sector']!='desconocido': byY[e['yr']][e['sector']].append(e)
yrs=sorted(byY)

print("="*100)
print("A) VALOR NEUTRAL POR SECTOR (el cuartil barato de TODOS los sectores) — sin elegir sectores")
print("="*100)
car=[];fam=[];q=[];ns=[];pools=[]
for y in yrs:
    sel=[];pool=[]
    for s,l in byY[y].items():
        if len(l)<8: continue
        o=sorted(l,key=lambda e:e['ps']); k=max(1,int(round(len(o)*0.25)))
        sel+=o[:k]; pool+=l
    car.append(np.mean([e['ret'] for e in sel])/100); fam.append(np.mean([e['ret'] for e in pool])/100)
    q.append(np.mean([e['qqq'] for e in sel])/100); ns.append(len(sel)); pools.append(pool)
car=np.array(car);fam=np.array(fam);q=np.array(q);T=len(yrs)
a=(cagr(car)-cagr(fam))*100
d=[]
for _ in range(3000):
    c=[]
    for i in range(T):
        r=np.array([e['ret'] for e in pools[i]])/100
        c.append(r[rng.choice(len(r),ns[i],replace=False)].mean())
    d.append((cagr(c)-cagr(fam))*100)
se=np.std(d,ddof=1)
P=[i for i,y in enumerate(yrs) if y%2==0]; I=[i for i,y in enumerate(yrs) if y%2==1]
cab(); stats(car,q,'barato 25% de cada sector',f"n/anho {np.mean(ns):.0f}")
stats(fam,q,'todos los sectores'); stats(q,q,'QQQ')
print(f"\n  ALFA INTERNO {a:+.2f} pp  SE {se:.2f}  t={a/se:.2f}  "
      f"({'SIGNIFICATIVO' if a/se>2 else 'no'})   pares {(cagr(car[P])-cagr(fam[P]))*100:+.2f}  "
      f"impares {(cagr(car[I])-cagr(fam[I]))*100:+.2f}")
print(f"  vs QQQ: CAGR {100*(cagr(car)-cagr(q)):+.2f} pp")

print()
print("="*100)
print("B) EL CENTINELA 'desconocido' (A4) — ¿sigue prediciendo el retorno con precios buenos?")
print("="*100)
byA=collections.defaultdict(list)
for e in ev: byA[e['yr']].append(e)
des=[];con=[];qq=[]
for y in sorted(byA):
    d_=[e['ret'] for e in byA[y] if e['sector']=='desconocido']
    c_=[e['ret'] for e in byA[y] if e['sector']!='desconocido']
    if not d_ or not c_: continue
    des.append(np.mean(d_)/100); con.append(np.mean(c_)/100)
    qq.append(np.mean([e['qqq'] for e in byA[y]])/100)
des=np.array(des);con=np.array(con);qq=np.array(qq)
cab(); stats(des,qq,"sector = 'desconocido'"); stats(con,qq,'sector conocido'); stats(qq,qq,'QQQ')
dif=(cagr(des)-cagr(con))*100
print(f"\n  Diferencia 'desconocido' menos conocido: {dif:+.2f} pp anuales")
print(f"  -> {'SIGUE contaminando: no se puede mezclar' if abs(dif)>2 else 'ya no distingue'}")

print()
print("="*100)
print("C) SUBTIPOS CICLICOS (C20) — CAGR y correlacion con precios buenos")
print("="*100)
CIC=['Basic Materials','Industrials','Consumer Cyclical','Energy']
print("  sector                 n/anho    CAGR    corr(QQQ)   beta   alfaJ")
print("  "+"-"*64)
for s in CIC:
    r=[];qz=[];nn=[]
    for y in yrs:
        l=byY[y].get(s,[])
        if len(l)<5: continue
        r.append(np.mean([e['ret'] for e in l])/100); qz.append(np.mean([e['qqq'] for e in l])/100); nn.append(len(l))
    r=np.array(r);qz=np.array(qz)
    X=np.column_stack([np.ones(len(r)),qz-RF]); b,_,_,_=np.linalg.lstsq(X,r-RF,rcond=None)
    print(f"  {s:<22} {np.mean(nn):>5.0f}  {100*cagr(r):>6.2f}%   {np.corrcoef(r,qz)[0,1]:>7.3f}  {b[1]:>6.2f}  {100*b[0]:>+6.2f}%")
