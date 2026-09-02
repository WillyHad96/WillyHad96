# R-A2 (pre-registrada en la adenda) + diagnostico de supervivencia por tramos.
import numpy as np, collections
def carga(f):
    R=[l.split(',') for l in open(f).read().splitlines()[1:]]
    return [dict(yr=int(r[0]),tk=r[1],mb=float(r[3]),cr=float(r[4]),r40=float(r[5]),
                 mc=float(r[6]),mom=float(r[7])/100,ret=float(r[8])/100,qqq=float(r[9])/100) for r in R]
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
PEQ=lambda e: e['mc']<=0.25

def serie(ev,sel):
    byyr=collections.defaultdict(list)
    for e in ev: byyr[e['yr']].append(e)
    yrs=sorted(byyr); out=[]; ns=[]
    for y in yrs:
        c=[e for e in byyr[y] if sel(e)]
        out.append(float(np.mean([e['ret'] for e in c])) if c else 0.0); ns.append(len(c))
    return np.array(out), ns, yrs, byyr

print("="*84)
print("R-A2 — cuartil MAS PEQUENHO, equiponderado, sin ningun otro filtro")
print("="*84)
for et,f in [('descubrimiento (pares)','ciclicas_pares.csv'),('CONFIRMACION (impares)','ciclicas_impares.csv')]:
    ev=carga(f); r,ns,yrs,byyr=serie(ev,PEQ)
    Q=np.array([np.mean([e['qqq'] for e in byyr[y]]) for y in yrs])
    rng=np.random.default_rng(13); CG=[]
    for _ in range(4000):
        rr=[]
        for y,k in zip(yrs,ns):
            pool=byyr[y]; k=min(len(pool),max(1,k))
            idx=rng.choice(len(pool),size=k,replace=False)
            rr.append(np.mean([pool[i]['ret'] for i in idx]))
        CG.append(cagr(rr))
    CG=np.array(CG); p=(np.sum(CG>=cagr(r))+1)/(len(CG)+1)
    print(f"  {et:<24} n/anho {np.mean(ns):>4.0f}   CAGR {100*cagr(r):>6.2f}%   "
          f"Nasdaq {100*cagr(Q):>6.2f}%   azar {100*CG.mean():>6.2f}%   p(CAGR)={p:.4f}")

ev=carga('ciclicas_pares.csv')+carga('ciclicas_impares.csv')
print()
print("  CRITERIO PRE-REGISTRADO (adenda seccion 11) sobre los impares:")
evi=carga('ciclicas_impares.csv'); r,ns,yrs,byyr=serie(evi,PEQ)
Q=np.array([np.mean([e['qqq'] for e in byyr[y]]) for y in yrs])
rng=np.random.default_rng(13); CG=[]
for _ in range(4000):
    rr=[]
    for y,k in zip(yrs,ns):
        pool=byyr[y]; k=min(len(pool),max(1,k))
        idx=rng.choice(len(pool),size=k,replace=False)
        rr.append(np.mean([pool[i]['ret'] for i in idx]))
    CG.append(cagr(rr))
CG=np.array(CG); p=(np.sum(CG>=cagr(r))+1)/(len(CG)+1)
c1=p<0.05; c2=cagr(r)>=cagr(Q)
print(f"    1. p(CAGR) < 0,05         : {p:.4f}  -> {'SI' if c1 else 'NO'}")
print(f"    2. CAGR >= Nasdaq {100*cagr(Q):.2f}%  : {100*cagr(r):.2f}%  -> {'SI' if c2 else 'NO'}")
print(f"    VEREDICTO: {'SUPERVIVIENTE' if (c1 and c2) else 'NO DISTINGUIBLE DEL RUIDO'}")

print()
print("="*84)
print("DIAGNOSTICO DE SUPERVIVENCIA — el efecto por tramos de calidad del panel")
print("="*84)
print("  Prediccion declarada en la adenda: si el efecto es sesgo, ENCOGE en 2021-2023.")
print()
byyr=collections.defaultdict(list)
for e in ev: byyr[e['yr']].append(e)
print(f"  {'anho':>5}{'n peq':>7}{'n resto':>8}{'peq':>9}{'resto':>9}{'PEQ-RESTO':>11}")
filas={}
for y in sorted(byyr):
    peq=[e['ret'] for e in byyr[y] if PEQ(e)]; res=[e['ret'] for e in byyr[y] if not PEQ(e)]
    if not peq or not res: continue
    d=np.mean(peq)-np.mean(res); filas[y]=d
    print(f"  {y:>5}{len(peq):>7}{len(res):>8}{100*np.mean(peq):>8.1f}%{100*np.mean(res):>8.1f}%{100*d:>+10.1f}")
print()
for lo,hi,et in [(2007,2014,'2007-2014  sin muertes registradas'),
                 (2015,2020,'2015-2020  registro parcial'),
                 (2021,2023,'2021-2023  registro realista')]:
    v=[d for y,d in filas.items() if lo<=y<=hi]
    print(f"  {et:<38} media PEQ-RESTO = {100*np.mean(v):+6.2f} pp   ({len(v)} anhos, "
          f"{sum(1 for x in v if x>0)}/{len(v)} positivos)")
