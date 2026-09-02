# CONFIRMACION — reglas cerradas en PREREGISTRO-CICLICAS-INVERTIDAS.md.
# Null de B2: carteras ALEATORIAS del mismo tamanho y mismo pool ciclico,
# con el mismo esquema de pesos (rank^2 por momento). 4.000 sims, semilla 13.
import numpy as np, collections, sys

def carga(f):
    R=[l.split(',') for l in open(f).read().splitlines()[1:]]
    return [dict(yr=int(r[0]),tk=r[1],mb=float(r[3]),cr=float(r[4]),r40=float(r[5]),
                 mc=float(r[6]),mom=float(r[7])/100,ret=float(r[8])/100,qqq=float(r[9])/100) for r in R]
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1

def r2w(c):
    n=len(c); s=sorted(c,key=lambda e:-e['mom'])
    pw=np.array([(n-i)**2 for i in range(n)],float)
    return float(np.dot([e['ret'] for e in s],pw)/pw.sum())

REGLAS={
 'R-A capitalizacion invertida': lambda e: e['mc']<=0.25 and e['mb']<0.5 and e['cr']<0.5 and e['r40']>0.25,
 'R-B estabilidad invertida'   : lambda e: e['mb']>0.5 and e['cr']>0.5,
 'R-C las dos juntas'          : lambda e: e['mb']>0.5 and e['cr']>0.5 and e['mc']<=0.25,
}

def evalua(ev, sel):
    byyr=collections.defaultdict(list)
    for e in ev: byyr[e['yr']].append(e)
    yrs=sorted(byyr); rets=[]; ns=[]
    for y in yrs:
        c=[e for e in byyr[y] if sel(e)]
        c=sorted(c,key=lambda e:-e['mom'])[:max(1,int(round(len(c)*0.20)))] if c else []
        if not c: rets.append(0.0); ns.append(0); continue
        rets.append(r2w(c)); ns.append(len(c))
    return np.array(rets), ns, yrs, byyr

def null(byyr, yrs, ns, IT=4000, seed=13):
    rng=np.random.default_rng(seed); CG=[]; CR=[]
    Q=np.array([np.mean([e['qqq'] for e in byyr[y]]) for y in yrs])
    for _ in range(IT):
        rr=[]
        for y,k in zip(yrs,ns):
            pool=byyr[y]; k=min(len(pool),max(1,k))
            idx=rng.choice(len(pool),size=k,replace=False)
            rr.append(r2w([pool[i] for i in idx]))
        CG.append(cagr(rr)); CR.append(np.corrcoef(rr,Q)[0,1])
    return np.array(CG),np.array(CR),Q

for etiqueta,fich in [('DESCUBRIMIENTO (pares)','ciclicas_pares.csv'),
                      ('CONFIRMACION (impares)','ciclicas_impares.csv')]:
    ev=carga(fich)
    print("="*92)
    print(f"{etiqueta} — {len(sorted({e['yr'] for e in ev}))} anhos, {len(ev)} eventos")
    print("="*92)
    _,_,yrs,byyr=evalua(ev,lambda e:True)
    Q=np.array([np.mean([e['qqq'] for e in byyr[y]]) for y in yrs])
    print(f"  Nasdaq en estos anhos: {100*cagr(Q):.2f}%")
    print(f"  {'regla':<30}{'n/anho':>7}{'CAGR':>9}{'corr':>7}{'azar':>7}{'REAL':>8}{'pCAGR':>8}{'pcorr':>8}{'pCONJ':>8}")
    print("  "+"-"*86)
    for nom,sel in REGLAS.items():
        r,ns,_,_=evalua(ev,sel)
        c=np.corrcoef(r,Q)[0,1]
        CG,CR,_=null(byyr,yrs,ns)
        pc=(np.sum(CG>=cagr(r))+1)/(len(CG)+1)
        pr=(np.sum(CR<=c)+1)/(len(CR)+1)
        pj=(np.sum((CG>=cagr(r))&(CR<=c))+1)/(len(CG)+1)
        print(f"  {nom:<30}{np.mean(ns):>7.0f}{100*cagr(r):>8.2f}%{c:>7.3f}{CR.mean():>7.3f}"
              f"{c-CR.mean():>+8.3f}{pc:>8.4f}{pr:>8.4f}{pj:>8.4f}")
    print()

print("="*92)
print("CRITERIO PRE-REGISTRADO (seccion 5) sobre los IMPARES — las tres condiciones")
print("="*92)
ev=carga('ciclicas_impares.csv')
_,_,yrs,byyr=evalua(ev,lambda e:True)
Q=np.array([np.mean([e['qqq'] for e in byyr[y]]) for y in yrs]); qc=cagr(Q)
for nom,sel in REGLAS.items():
    r,ns,_,_=evalua(ev,sel)
    c=np.corrcoef(r,Q)[0,1]; CG,CR,_=null(byyr,yrs,ns)
    pj=(np.sum((CG>=cagr(r))&(CR<=c))+1)/(len(CG)+1)
    c1=pj<0.0167; c2=cagr(r)>=qc; c3=(c-CR.mean())<0
    print(f"\n  {nom}")
    print(f"    1. p_conjunta < 0,0167      : {pj:.4f}  -> {'SI' if c1 else 'NO'}")
    print(f"    2. CAGR >= Nasdaq ({100*qc:.2f}%)   : {100*cagr(r):.2f}%  -> {'SI' if c2 else 'NO'}")
    print(f"    3. descorrelacion real < 0  : {c-CR.mean():+.3f}  -> {'SI' if c3 else 'NO'}")
    print(f"    VEREDICTO: {'SUPERVIVIENTE' if (c1 and c2 and c3) else 'NO DISTINGUIBLE DEL RUIDO'}")
