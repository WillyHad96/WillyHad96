# REHECHO 5 — PROTOCOLO HONESTO. La eleccion de sectores se hace SOLO con anhos pares
# (descubrimiento) y se mide SOLO en impares (confirmacion). Sin mirar el resultado antes.
import collections, numpy as np
from base_lib import *
ev=carga()
by=collections.defaultdict(lambda: collections.defaultdict(list))
for e in ev:
    if e['sector']!='desconocido': by[e['yr']][e['sector']].append(e)
yrs=sorted(by)
PAR=[y for y in yrs if y%2==0]; IMP=[y for y in yrs if y%2==1]
SECT=sorted({s for y in yrs for s in by[y]})

def alfa_int(sec,anos,frac=0.25,minn=8):
    car=[];fam=[]
    for y in anos:
        l=by[y].get(sec,[])
        if len(l)<minn: continue
        o=sorted(l,key=lambda e:e['ps']); k=max(1,int(round(len(o)*frac)))
        car.append(np.mean([e['ret'] for e in o[:k]])/100); fam.append(np.mean([e['ret'] for e in l])/100)
    if len(car)<5: return None
    return (cagr(car)-cagr(fam))*100

print("PASO 1 — ranking de sectores usando SOLO los anhos PARES (descubrimiento):")
rank=[]
for s in SECT:
    a=alfa_int(s,PAR)
    if a is not None: rank.append((a,s))
rank.sort(reverse=True)
for a,s in rank: print(f"    {s:<24}{a:>+8.2f} pp")
elegidos={s for a,s in rank[:3]}
print(f"\n  -> sectores elegidos (top 3 en pares): {sorted(elegidos)}")

print("\nPASO 2 — medir esa eleccion SOLO en anhos IMPARES (confirmacion):")
def cartera(anos,sectores,frac=0.25,minn=8):
    car=[];fam=[];q=[];ns=[]
    for y in anos:
        sel=[];pool=[]
        for s in sectores:
            l=by[y].get(s,[])
            if len(l)<minn: continue
            o=sorted(l,key=lambda e:e['ps']); k=max(1,int(round(len(o)*frac)))
            sel+=o[:k]; pool+=l
        if not sel: continue
        car.append(np.mean([e['ret'] for e in sel])/100); fam.append(np.mean([e['ret'] for e in pool])/100)
        q.append(np.mean([e['qqq'] for e in sel])/100); ns.append(len(sel))
    return np.array(car),np.array(fam),np.array(q),ns
c,f,q,n=cartera(IMP,elegidos)
a=(cagr(c)-cagr(f))*100
rng=np.random.default_rng(41); d=[]
for _ in range(3000):
    cc=[]
    for i,y in enumerate(IMP):
        pool=[e for s in elegidos for e in by[y].get(s,[]) if len(by[y].get(s,[]))>=8]
        if not pool: continue
        r=np.array([e['ret'] for e in pool])/100
        cc.append(r[rng.choice(len(r),min(n[i],len(r)),replace=False)].mean())
    d.append((cagr(cc)-cagr(f))*100)
se=np.std(d,ddof=1)
cab(); stats(c,q,'cartera (solo impares)',f"n/anho {np.mean(n):.0f}"); stats(q,q,'QQQ (solo impares)')
print(f"\n  ALFA INTERNO en confirmacion: {a:+.2f} pp   SE {se:.2f}   t={a/se:.2f}   "
      f"({'CONFIRMA' if a/se>2 else 'no confirma'})")
print(f"  vs QQQ: CAGR {100*(cagr(c)-cagr(q)):+.2f} pp")

print("\nPASO 3 — y al reves (elegir en impares, medir en pares), para ver si es casualidad:")
rank2=sorted(((alfa_int(s,IMP),s) for s in SECT if alfa_int(s,IMP) is not None),reverse=True)
eleg2={s for a2,s in rank2[:3]}
print(f"  sectores elegidos en impares: {sorted(eleg2)}")
c2,f2,q2,n2=cartera(PAR,eleg2)
a2=(cagr(c2)-cagr(f2))*100
print(f"  ALFA INTERNO medido en pares: {a2:+.2f} pp   vs QQQ: {100*(cagr(c2)-cagr(q2)):+.2f} pp")
print(f"\n  Coincidencia de la eleccion entre mitades: {sorted(elegidos & eleg2)} "
      f"({len(elegidos&eleg2)} de 3)")
