# REHECHO 4 — cartera VALOR NEUTRAL POR SECTOR: el cuartil barato de cada sector, combinado.
# Es la unica configuracion que suma nombres (baja el suelo de ruido) sin diluir la senhal.
import collections, numpy as np
from base_lib import *
ev=carga()
rng=np.random.default_rng(31)
SECT=[s for s in {e['sector'] for e in ev} if s!='desconocido']
by=collections.defaultdict(lambda: collections.defaultdict(list))
for e in ev:
    if e['sector']!='desconocido': by[e['yr']][e['sector']].append(e)
yrs=sorted(by); T=len(yrs)
print(f"anhos {yrs[0]}-{yrs[-1]}  (se EXCLUYE el cubo 'desconocido': es el centinela de A4/A7)")

def cartera(frac, sectores=None, minn=8):
    car=[];fam=[];q=[];ns=[]
    for y in yrs:
        sel=[];pool=[]
        for s,lst in by[y].items():
            if sectores and s not in sectores: continue
            if len(lst)<minn: continue
            o=sorted(lst,key=lambda e:e['ps']); k=max(1,int(round(len(o)*frac)))
            sel+=o[:k]; pool+=lst
        if not sel: continue
        car.append(np.mean([e['ret'] for e in sel])/100)
        fam.append(np.mean([e['ret'] for e in pool])/100)
        q.append(np.mean([e['qqq'] for e in sel])/100); ns.append(len(sel))
    return np.array(car),np.array(fam),np.array(q),ns

def informe(etq,car,fam,q,ns,by_pool=None):
    T=len(car); P=[i for i,y in enumerate(yrs) if y%2==0]; I=[i for i,y in enumerate(yrs) if y%2==1]
    a=(cagr(car)-cagr(fam))*100
    exc=car-q; t_e=exc.mean()/(exc.std(ddof=1)/np.sqrt(T))
    X=np.column_stack([np.ones(T),q-RF]); yv=car-RF
    b,_,_,_=np.linalg.lstsq(X,yv,rcond=None); resid=yv-X@b
    s2=(resid@resid)/(T-2); cov=s2*np.linalg.inv(X.T@X); t_a=b[0]/np.sqrt(cov[0,0])
    cr=np.corrcoef(car,q)[0,1]
    print(f"  {etq:<30}{np.mean(ns):>5.0f} {100*cagr(car):>7.2f}% {100*cagr(q):>7.2f}% "
          f"{100*b[1]:>6.0f}% {100*b[0]:>+7.2f}% {t_a:>6.2f} {a:>+7.2f} {cr:>7.3f} "
          f"{(cagr(car[P])-cagr(fam[P]))*100:>6.1f} {(cagr(car[I])-cagr(fam[I]))*100:>6.1f}")
    return dict(cagr=cagr(car),alfaJ=b[0],t=t_a,ai=a,corr=cr,beta=b[1],car=car,q=q)

print()
print("  cartera                       n/anho    CAGR     QQQ   beta   alfaJ      t   alfaInt   corr  pares impar")
print("  "+"-"*112)
R={}
for frac,etq in ((0.15,'barato 15% de cada sector'),(0.25,'barato 25% de cada sector'),
                 (0.35,'barato 35% de cada sector')):
    c,f,q,n=cartera(frac); R[etq]=informe(etq,c,f,q,n)
c,f,q,n=cartera(0.25,{'Basic Materials','Industrials','Financial Services'})
R['3 sectores fuertes']=informe('barato 25%, solo 3 sectores',c,f,q,n)
c,f,q,n=cartera(0.25,{'Basic Materials','Industrials'})
R['BM+Indu']=informe('barato 25%, BasicMat+Indust',c,f,q,n)
# referencia: todo el universo sin filtro de valor
car=[];q2=[]
for y in yrs:
    pool=[e for s,l in by[y].items() for e in l]
    car.append(np.mean([e['ret'] for e in pool])/100); q2.append(np.mean([e['qqq'] for e in pool])/100)
car=np.array(car);q2=np.array(q2)
print(f"  {'(universo sin filtro valor)':<30}{'':>5} {100*cagr(car):>7.2f}% {100*cagr(q2):>7.2f}%")
print(f"  {'(QQQ)':<30}{'':>5} {100*cagr(q2):>7.2f}%")
import pickle; pickle.dump({k:{kk:vv for kk,vv in v.items() if kk not in('car','q')} for k,v in R.items()},open('/tmp/comb.pkl','wb'))
