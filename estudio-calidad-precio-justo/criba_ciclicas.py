# DESCUBRIMIENTO — solo anhos PARES (2008..2022). No se mira 2007..2023 impares.
# Pregunta: que renta y como correlaciona el lado que cada filtro DESCARTA,
# dentro de los 4 sectores ciclicos.
import numpy as np, math, collections
R=[l.split(',') for l in open('ciclicas_pares.csv').read().splitlines()[1:]]
ev=[dict(yr=int(r[0]),tk=r[1],sec=r[2],mb=float(r[3]),cr=float(r[4]),r40=float(r[5]),
         mc=float(r[6]),mom=float(r[7])/100,ret=float(r[8])/100,qqq=float(r[9])/100) for r in R]
yrs=sorted({e['yr'] for e in ev})
byyr=collections.defaultdict(list)
for e in ev: byyr[e['yr']].append(e)
QQQ=np.array([np.mean([e['qqq'] for e in byyr[y]]) for y in yrs])
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1

def cartera(sel, mom_top=None, w='ew'):
    """sel: filtro sobre evento. mom_top: fraccion superior por momento dentro de lo filtrado."""
    rets=[]; ns=[]
    for y in yrs:
        c=[e for e in byyr[y] if sel(e)]
        if mom_top is not None and c:
            c=sorted(c,key=lambda e:-e['mom'])[:max(1,int(round(len(c)*mom_top)))]
        if not c: rets.append(0.0); ns.append(0); continue
        if w=='ew': rets.append(float(np.mean([e['ret'] for e in c])))
        else:
            n=len(c); s=sorted(c,key=lambda e:-e['mom'])
            pw=np.array([ (n-i)**2 for i in range(n)],float)
            rets.append(float(np.dot([e['ret'] for e in s],pw)/pw.sum()))
        ns.append(len(c))
    return np.array(rets), float(np.mean(ns))

def azar(nmed, IT=400, seed=13):
    rng=np.random.default_rng(seed); cs=[]
    for _ in range(IT):
        rr=[]
        for y in yrs:
            pool=byyr[y]; k=min(len(pool),max(1,int(round(nmed))))
            idx=rng.choice(len(pool),size=k,replace=False)
            rr.append(np.mean([pool[i]['ret'] for i in idx]))
        cs.append(np.corrcoef(rr,QQQ)[0,1])
    return float(np.mean(cs))

def linea(nom, sel, mom_top=None, w='ew'):
    r,n=cartera(sel,mom_top,w)
    c=np.corrcoef(r,QQQ)[0,1]; a=azar(n)
    print(f"  {nom:<34}{n:>6.0f}{100*cagr(r):>9.2f}%{c:>8.3f}{a:>8.3f}{c-a:>+9.3f}{100*(cagr(r)-cagr(QQQ)):>+9.2f}")
    return r,n,c-a

print("="*94)
print(f"DESCUBRIMIENTO — anhos PARES {yrs[0]}-{yrs[-1]} ({len(yrs)} anhos, {len(ev)} eventos)")
print(f"Nasdaq en estos anhos: CAGR {100*cagr(QQQ):.2f}%")
print("="*94)
print(f"  {'variante':<34}{'n/anho':>6}{'CAGR':>10}{'corr':>8}{'azar':>8}{'REAL':>9}{'vs QQQ':>9}")
print("  "+"-"*88)
linea("TODAS las ciclicas (sin filtro)", lambda e: True)
print("  --- filtro de ESTABILIDAD (el que mas quita) ---")
linea("estabilidad PASA (mb<.5 y cr<.5)", lambda e: e['mb']<0.5 and e['cr']<0.5)
linea("estabilidad FALLA", lambda e: not(e['mb']<0.5 and e['cr']<0.5))
linea("estabilidad INVERTIDA (mb>.5 y cr>.5)", lambda e: e['mb']>0.5 and e['cr']>0.5)
print("  --- regla 40 ---")
linea("r40 PASA (>p25)", lambda e: e['r40']>0.25)
linea("r40 FALLA (<p25)", lambda e: e['r40']<=0.25)
print("  --- capitalizacion ---")
linea("mcap PASA (>p25)", lambda e: e['mc']>0.25)
linea("mcap FALLA (<p25)", lambda e: e['mc']<=0.25)
print("  --- momento ---")
linea("momento top 20%", lambda e: True, mom_top=0.20)
linea("momento resto 80%", lambda e: True)
print("  --- combinaciones ---")
linea("C4 ciclicas (todos + mom20, rank^2)", lambda e: e['mb']<0.5 and e['cr']<0.5 and e['r40']>0.25 and e['mc']>0.25, mom_top=0.20, w='r2')
linea("ESTAB INVERTIDA + mom20 (rank^2)", lambda e: e['mb']>0.5 and e['cr']>0.5 and e['r40']>0.25 and e['mc']>0.25, mom_top=0.20, w='r2')
linea("ESTAB INVERTIDA + mom20, sin r40/mc", lambda e: e['mb']>0.5 and e['cr']>0.5, mom_top=0.20, w='r2')
