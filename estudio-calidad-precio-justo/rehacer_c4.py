# REHECHO 1 — la estrategia C4 original, con retornos verificados (A9) y con el indice
# calculado en las FECHAS EXACTAS de cada posicion (ni la columna qqq del panel, que esta
# corrupta, ni un feb-feb aproximado).
import collections, numpy as np
from base_lib import *
ev=carga()
by=collections.defaultdict(list)
for e in ev: by[e['yr']].append(e)
yrs=sorted(by)
print(f"universo elegible: {len(ev)} decisiones, {len(yrs)} anhos ({yrs[0]}-{yrs[-1]})")
print("Indices: precio, sin dividendos — igual que las acciones (precio_post). Comparable.")
print()

def c4_pool(pool):
    a=pr([e['sdmb'] for e in pool]); b=pr([e['sdcr'] for e in pool])
    c=pr([e['r40'] for e in pool]);  d=pr([e['mcap'] for e in pool])
    return [e for i,e in enumerate(pool) if a[i]<0.5 and b[i]<0.5 and c[i]>0.25 and d[i]>0.25]

cart=[];pasa=[];nopasa=[];univ=[];bq=[];bi=[];ns=[]
for y in yrs:
    pool=by[y]; c4=c4_pool(pool)
    univ.append(np.mean([e['ret'] for e in pool])/100)
    ids={id(e) for e in c4}; resto=[e for e in pool if id(e) not in ids]
    pasa.append(np.mean([e['ret'] for e in c4])/100)
    nopasa.append(np.mean([e['ret'] for e in resto])/100)
    o=sorted(c4,key=lambda e:-e['mom']); k=max(1,int(len(c4)*0.20)); sel=o[:k]; n=len(sel)
    w=np.array([(n-i)**2 for i in range(n)],float)
    cart.append(float(np.dot([e['ret'] for e in sel],w)/w.sum())/100); ns.append(n)
    bq.append(np.mean([e['qqq'] for e in sel])/100)   # indice en las mismas fechas
    bi.append(np.mean([e['ixic'] for e in sel])/100)
bq=np.array(bq); bi=np.array(bi)
cab()
stats(cart,bq,'C4 (top 20% momento, rank^2)',f"n/anho {np.mean(ns):.0f}")
stats(pasa,bq,'pasa el filtro C4 (equipond.)')
stats(nopasa,bq,'NO pasa el filtro')
stats(univ,bq,'universo elegible entero')
stats(bq,bq,'NASDAQ-100 (QQQ)')
stats(bi,bq,'NASDAQ Composite (^IXIC)')
print()
P=[i for i,y in enumerate(yrs) if y%2==0]; I=[i for i,y in enumerate(yrs) if y%2==1]
ai=(cagr(pasa)-cagr(nopasa))*100
print(f"  ALFA INTERNO (pasa menos no-pasa): {ai:+.2f} pp   "
      f"pares {(cagr(np.array(pasa)[P])-cagr(np.array(nopasa)[P]))*100:+.2f}   "
      f"impares {(cagr(np.array(pasa)[I])-cagr(np.array(nopasa)[I]))*100:+.2f}")
print(f"  C4 vs QQQ en CAGR: {100*(cagr(cart)-cagr(bq)):+.2f} pp     "
      f"C4 vs ^IXIC: {100*(cagr(cart)-cagr(bi)):+.2f} pp")
print(f"  correlacion C4-QQQ: {np.corrcoef(cart,bq)[0,1]:.3f}    C4-^IXIC: {np.corrcoef(cart,bi)[0,1]:.3f}")
print()
print("  AÑO A AÑO (C4 vs QQQ):")
print("   anho     C4      QQQ    dif")
for i,y in enumerate(yrs):
    print(f"   {y}  {100*cart[i]:>6.1f}%  {100*bq[i]:>6.1f}%  {100*(cart[i]-bq[i]):>+6.1f}")

print()
print("="*84)
print("CONTROLES — ¿sobrevive?")
print("="*84)
import numpy as np
exc=np.array(cart)-bq
T=len(exc)
t_exc=exc.mean()/(exc.std(ddof=1)/np.sqrt(T))
print(f"  1) Exceso anual medio sobre QQQ: {100*exc.mean():+.2f} pp, t={t_exc:.2f}  "
      f"({'significativo' if abs(t_exc)>2 else 'NO significativo'})")
print(f"     pares {100*exc[P].mean():+.2f} pp   impares {100*exc[I].mean():+.2f} pp"
      f"   -> {'replica' if exc[P].mean()>0 and exc[I].mean()>0 else 'NO replica'}")
# t del alfa de Jensen por regresion
X=np.column_stack([np.ones(T),bq-RF]); y=np.array(cart)-RF
b,res,_,_=np.linalg.lstsq(X,y,rcond=None)
resid=y-X@b; s2=(resid@resid)/(T-2); cov=s2*np.linalg.inv(X.T@X)
t_alfa=b[0]/np.sqrt(cov[0,0])
print(f"  2) Alfa de Jensen: {100*b[0]:+.2f}% anual, t={t_alfa:.2f}  "
      f"({'significativo' if abs(t_alfa)>2 else 'NO significativo'})")
# alfa interno: ruido por bootstrap con carteras aleatorias del mismo tamanho
rng=np.random.default_rng(5); d=[]
for _ in range(4000):
    a_=[];b_=[]
    for i,y_ in enumerate(yrs):
        pool=by[y_]; n=len(pool); k=sum(1 for e in c4_pool(pool))
        idx=rng.permutation(n); s1=idx[:k]; s2_=idx[k:]
        r=np.array([e['ret'] for e in pool])/100
        a_.append(r[s1].mean()); b_.append(r[s2_].mean())
    d.append((cagr(a_)-cagr(b_))*100)
se=np.std(d,ddof=1)
print(f"  3) Alfa interno {ai:+.2f} pp contra ruido de particiones aleatorias del mismo "
      f"tamanho: SE={se:.2f} pp, t={ai/se:.2f}  ({'significativo' if abs(ai/se)>2 else 'NO significativo'})")
# contrafactual de correlacion: carteras aleatorias de 35 nombres
cc=[]
for _ in range(2000):
    c_=[];q_=[]
    for y_ in yrs:
        pool=by[y_]; idx=rng.choice(len(pool),min(35,len(pool)),replace=False)
        c_.append(np.mean([pool[i]['ret'] for i in idx])/100)
        q_.append(np.mean([pool[i]['qqq'] for i in idx])/100)
    cc.append(np.corrcoef(c_,q_)[0,1])
cr_obs=np.corrcoef(cart,bq)[0,1]
print(f"  4) Correlacion observada {cr_obs:.3f} vs carteras ALEATORIAS de 35 nombres "
      f"{np.mean(cc):.3f} (p10-p90 {np.percentile(cc,10):.3f}-{np.percentile(cc,90):.3f})")
print(f"     descorrelacion real: {cr_obs-np.mean(cc):+.3f}  -> "
      f"{'nada' if abs(cr_obs-np.mean(cc))<0.05 else 'algo'}")
# quitar un anho cada vez
print("  5) Robustez quitando un anho (exceso sobre QQQ):")
w=[]
for i in range(T):
    m=[j for j in range(T) if j!=i]
    w.append((cagr(np.array(cart)[m])-cagr(bq[m]))*100)
print(f"     min {min(w):+.2f} pp (sin {yrs[int(np.argmin(w))]})   max {max(w):+.2f} pp   "
      f"-> {'estable' if min(w)>0 else 'DEPENDE DE UN ANHO'}")
