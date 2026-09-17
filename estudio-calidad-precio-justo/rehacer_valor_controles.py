# REHECHO 3 — controles completos sobre los sectores donde el efecto valor aparece.
import collections, numpy as np
from base_lib import *
ev=carga()
rng=np.random.default_rng(23)
def analiza(sec, frac=0.25):
    sub=[e for e in ev if e['sector']==sec]
    by=collections.defaultdict(list)
    for e in sub: by[e['yr']].append(e)
    yrs=[y for y in sorted(by) if len(by[y])>=8]
    car=[];fam=[];q=[];ns=[];cuart=[[] for _ in range(4)]
    for y in yrs:
        pool=sorted(by[y],key=lambda e:e['ps']); n=len(pool); k=max(1,int(round(n*frac)))
        car.append(np.mean([e['ret'] for e in pool[:k]])/100)
        fam.append(np.mean([e['ret'] for e in by[y]])/100)
        q.append(np.mean([e['qqq'] for e in pool[:k]])/100); ns.append(k)
        for j in range(4):
            seg=pool[int(n*j/4):int(n*(j+1)/4)]
            if seg: cuart[j].append(np.mean([e['ret'] for e in seg])/100)
    car=np.array(car);fam=np.array(fam);q=np.array(q);T=len(yrs)
    P=[i for i,y in enumerate(yrs) if y%2==0]; I=[i for i,y in enumerate(yrs) if y%2==1]
    a=(cagr(car)-cagr(fam))*100
    print(f"\n{'='*92}\n{sec.upper()} — cuartil mas barato por P/S ({np.mean(ns):.0f} nombres/anho, {len(sub)} obs, {T} anhos)\n{'='*92}")
    cab(); stats(car,q,'cartera barata'); stats(fam,q,'su propio sector'); stats(q,q,'NASDAQ-100 (QQQ)')
    # 1 alfa interno + ruido
    d=[]
    for _ in range(3000):
        c=[]
        for i,y in enumerate(yrs):
            r=np.array([e['ret'] for e in by[y]])/100
            c.append(r[rng.choice(len(r),ns[i],replace=False)].mean())
        d.append((cagr(c)-cagr(fam))*100)
    se=np.std(d,ddof=1)
    print(f"\n  1) ALFA INTERNO {a:+.2f} pp  SE {se:.2f}  t={a/se:.2f}  "
          f"({'SIGNIFICATIVO' if abs(a/se)>2 else 'no significativo'})")
    print(f"     pares {(cagr(car[P])-cagr(fam[P]))*100:+.2f}  impares {(cagr(car[I])-cagr(fam[I]))*100:+.2f}  "
          f"-> {'REPLICA' if (cagr(car[P])-cagr(fam[P]))>0 and (cagr(car[I])-cagr(fam[I]))>0 else 'NO replica'}")
    # 2 vs QQQ
    exc=car-q; t_e=exc.mean()/(exc.std(ddof=1)/np.sqrt(T))
    X=np.column_stack([np.ones(T),q-RF]); yv=car-RF
    b,_,_,_=np.linalg.lstsq(X,yv,rcond=None); resid=yv-X@b
    s2=(resid@resid)/(T-2); cov=s2*np.linalg.inv(X.T@X); t_a=b[0]/np.sqrt(cov[0,0])
    print(f"  2) vs QQQ: CAGR {100*(cagr(car)-cagr(q)):+.2f} pp | exceso medio {100*exc.mean():+.2f} pp t={t_e:.2f} | "
          f"alfa Jensen {100*b[0]:+.2f}% t={t_a:.2f}  ({'SIGNIFICATIVO' if abs(t_a)>2 else 'no'})")
    # 3 monotonia
    print(f"  3) Monotonia por cuartil de P/S (barato->caro): "
          + "  ".join(f"{100*cagr(c):.1f}%" for c in cuart))
    # 4 quitar un anho
    w=[(cagr(np.delete(car,i))-cagr(np.delete(fam,i)))*100 for i in range(T)]
    print(f"  4) Quitando un anho: min {min(w):+.2f} pp (sin {yrs[int(np.argmin(w))]})  max {max(w):+.2f} pp  "
          f"-> {'ESTABLE' if min(w)>0 else 'depende de un anho'}")
    # 5 descorrelacion real
    cc=[]
    for _ in range(1500):
        c_=[];q_=[]
        for i,y in enumerate(yrs):
            pool=by[y]; idx=rng.choice(len(pool),ns[i],replace=False)
            c_.append(np.mean([pool[j]['ret'] for j in idx])/100)
            q_.append(np.mean([pool[j]['qqq'] for j in idx])/100)
        cc.append(np.corrcoef(c_,q_)[0,1])
    cr=np.corrcoef(car,q)[0,1]
    print(f"  5) Correlacion {cr:.3f} vs aleatorias del mismo tamanho {np.mean(cc):.3f}  "
          f"-> descorrelacion real {cr-np.mean(cc):+.3f} "
          f"({'REAL' if cr-np.mean(cc)<-0.05 else 'ninguna'})")
    return a,a/se,cagr(car),cr
for s in ('Basic Materials','Financial Services','Industrials'):
    analiza(s)
