# La familia del ciclo de capex (Industrials + Basic Materials) y las HUNDIDAS dentro.
# Descubrimiento en pares, confirmacion en impares, contrafactual aleatorio (B2) siempre.
import numpy as np, collections
SEC={}
for l in open('universo_sectorizado.csv').read().splitlines()[1:]:
    p=l.split(','); SEC[(p[0],p[1])]=p[3]
H=open('ciclicas_ampliado.csv').read().splitlines(); cols=H[0].split(',')
ev=[]
for l in H[1:]:
    p=l.split(','); d={}
    for c,v in zip(cols,p):
        if c=='ticker': d[c]=v
        else:
            try: d[c]=float(v) if v!='' else None
            except: d[c]=None
    d['sec']=SEC.get((str(int(d['yr'])),d['ticker']))
    if d['sec'] in ('Indu','Basi') and d['ps'] is not None: ev.append(d)
yrs=sorted({e['yr'] for e in ev}); PAR=[y for y in yrs if y%2==0]; IMP=[y for y in yrs if y%2==1]
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
byyr=collections.defaultdict(list)
for e in ev: byyr[e['yr']].append(e)
QQQ={y:np.mean([e['qqq'] for e in byyr[y]])/100 for y in yrs}

def cartera(sel, anos, w='ew'):
    r=[];ns=[]
    for y in anos:
        c=[e for e in byyr[y] if sel(e,byyr[y])]
        if not c: r.append(0.0); ns.append(0); continue
        r.append(np.mean([e['ret'] for e in c])/100); ns.append(len(c))
    return np.array(r), float(np.mean(ns))

def azar(nmed, anos, IT=600, seed=13):
    rng=np.random.default_rng(seed); C=[];G=[]
    Q=np.array([QQQ[y] for y in anos])
    for _ in range(IT):
        rr=[]
        for y in anos:
            pool=byyr[y]; k=min(len(pool),max(1,int(round(nmed))))
            idx=rng.choice(len(pool),size=k,replace=False)
            rr.append(np.mean([pool[i]['ret'] for i in idx])/100)
        C.append(np.corrcoef(rr,Q)[0,1]); G.append(cagr(rr))
    return float(np.mean(C)), float(np.mean(G))

def pct(e,pool,var,lo,hi):
    v=sorted(x[var] for x in pool if x.get(var) is not None)
    if not v or e.get(var) is None: return False
    import bisect
    p=bisect.bisect_left(v,e[var])/max(len(v)-1,1)
    return lo<=p<hi

DEFS=[
 ("familia entera (Indu+Basi)",      lambda e,p: True),
 ("BARATAS  P/S en el 25% inferior", lambda e,p: pct(e,p,'ps',0.0,0.25)),
 ("BARATAS  P/S en el 10% inferior", lambda e,p: pct(e,p,'ps',0.0,0.10)),
 ("CARAS    P/S en el 25% superior", lambda e,p: pct(e,p,'ps',0.75,1.01)),
 ("HUNDIDA: barata + margen bajo",   lambda e,p: pct(e,p,'ps',0.0,0.25) and pct(e,p,'mop',0.0,0.50)),
 ("HUNDIDA: barata + momento neg.",  lambda e,p: pct(e,p,'ps',0.0,0.25) and (e.get('mom') or 0)<0),
 ("HUNDIDA COMPLETA: las tres",      lambda e,p: pct(e,p,'ps',0.0,0.25) and pct(e,p,'mop',0.0,0.50) and (e.get('mom') or 0)<0),
 ("barata + momento POSITIVO",       lambda e,p: pct(e,p,'ps',0.0,0.25) and (e.get('mom') or 0)>=0),
]

for anos,et in [(PAR,'DESCUBRIMIENTO (pares)'),(IMP,'CONFIRMACION (impares)')]:
    Q=np.array([QQQ[y] for y in anos])
    print("="*100)
    print(f"{et} — {len(anos)} anhos, Nasdaq {100*cagr(Q):.2f}%")
    print("="*100)
    print(f"  {'variante':<36}{'n/anho':>7}{'CAGR':>9}{'corr':>8}{'azar':>8}{'REAL':>8}{'CAGR azar':>11}{'vs QQQ':>9}")
    print("  "+"-"*96)
    for nom,sel in DEFS:
        r,n=cartera(sel,anos)
        if n<1: print(f"  {nom:<36}{'vacia':>7}"); continue
        c=np.corrcoef(r,Q)[0,1]; ca,ga=azar(n,anos)
        print(f"  {nom:<36}{n:>7.0f}{100*cagr(r):>8.2f}%{c:>8.3f}{ca:>8.3f}{c-ca:>+8.3f}{100*ga:>10.2f}%{100*(cagr(r)-cagr(Q)):>+9.2f}")
    print()
