# Si la cola no es predecible, ¿que implica la asimetria para el TAMANHO de la cartera?
import numpy as np, collections
R=[l.split(',') for l in open('universo_sectorizado.csv').read().splitlines()[1:]]
ev=[dict(yr=int(r[0]),g=r[2],ret=float(r[9])/100,qqq=float(r[10])/100) for r in R]
yrs=sorted({e['yr'] for e in ev})
QQQ=np.array([np.mean([e['qqq'] for e in ev if e['yr']==y]) for y in yrs])
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1

print("="*86)
print("1. CUANTO DEPENDE EL POOL DE SU PROPIA COLA")
print("="*86)
for g,et in [('CIC','ciclicas'),('NOC','no cic.')]:
    todo=[];sin10=[];sin5=[];solo10=[]
    for y in yrs:
        v=np.array([e['ret'] for e in ev if e['yr']==y and e['g']==g])
        u10=np.percentile(v,90); u5=np.percentile(v,95)
        todo.append(v.mean()); sin10.append(v[v<u10].mean()); sin5.append(v[v<u5].mean())
        solo10.append(v[v>=u10].mean())
    print(f"  {et}:")
    print(f"    pool completo            CAGR {100*cagr(todo):>6.2f}%   media {100*np.mean(todo):>6.1f}%")
    print(f"    quitando el 10% superior CAGR {100*cagr(sin10):>6.2f}%   media {100*np.mean(sin10):>6.1f}%"
          f"   -> se pierden {100*(cagr(todo)-cagr(sin10)):.2f} pp de CAGR")
    print(f"    quitando el  5% superior CAGR {100*cagr(sin5):>6.2f}%   media {100*np.mean(sin5):>6.1f}%")
    print(f"    SOLO el 10% superior     CAGR {100*cagr(solo10):>6.2f}%   corr {np.corrcoef(solo10,QQQ)[0,1]:.3f}")
    print()

print("="*86)
print("2. ¿CUANTOS NOMBRES HACEN FALTA PARA NO PERDERSE LA COLA?")
print("="*86)
print("  Carteras ALEATORIAS del pool ciclico. 3.000 sims por tamanho, semilla 13.")
print(f"  {'nombres':>8}{'CAGR mediano':>14}{'p10':>8}{'p90':>8}{'corr QQQ':>10}{'% que bate al QQQ':>19}")
rng=np.random.default_rng(13)
byyg=collections.defaultdict(list)
for e in ev:
    if e['g']=='CIC': byyg[e['yr']].append(e['ret'])
qc=cagr(QQQ)
for k in (5,10,15,20,30,50,100,200):
    CG=[];CR=[]
    for _ in range(3000):
        rr=[]
        for y in yrs:
            v=byyg[y]; kk=min(len(v),k)
            rr.append(np.mean(rng.choice(v,size=kk,replace=False)))
        CG.append(cagr(rr)); CR.append(np.corrcoef(rr,QQQ)[0,1])
    CG=np.array(CG);CR=np.array(CR)
    print(f"  {k:>8}{100*np.median(CG):>13.2f}%{100*np.percentile(CG,10):>8.1f}{100*np.percentile(CG,90):>8.1f}"
          f"{np.mean(CR):>10.3f}{100*np.mean(CG>qc):>18.0f}%")
print(f"\n  Nasdaq en estos 17 anhos: {100*qc:.2f}%")
