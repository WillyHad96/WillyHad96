# REHECHO 7 — factores de la literatura (C29) y el ROIC (C30) con retornos verificados.
import collections, numpy as np, json, glob, os
from base_lib import *
ev=carga()
KM={}
for f in glob.glob('fmp_raw/*.json'):
    sym=os.path.basename(f)[:-5]
    rows=[r for r in json.load(open(f)) if r.get('date')]
    rows.sort(key=lambda r:r['date']); KM[sym]=rows
IS={}
for f in glob.glob('fmp_is/*.json'):
    sym=os.path.basename(f)[:-5]
    rows=[r for r in json.load(open(f)) if r.get('date')]
    rows.sort(key=lambda r:r['date']); IS[sym]=rows
def prev(sym,yr,src):
    r=[d for d in src.get(sym,[]) if d['date']<=f"{yr-1}-11-15"]
    return r[-1] if r else None
sub=[]
for e in ev:
    if e['sector']!='Industrials' or e['ticker'] not in KM: continue
    u=prev(e['ticker'],e['yr'],KM)
    if not u: continue
    hist=[d for d in KM[e['ticker']] if d['date']<=f"{e['yr']-1}-11-15"]
    e=dict(e); e['km']=u; e['km_hist']=hist
    e['roic']=u.get('returnOnInvestedCapital')
    sub.append(e)
print(f"Industrials con key-metrics y retorno verificado: {len({x['ticker'] for x in sub})} tickers, {len(sub)} decisiones")
by=collections.defaultdict(list)
for e in sub: by[e['yr']].append(e)
yrs=sorted(by)

def var_crec(e,campo,k):
    h=e['km_hist']
    if len(h)<=k: return None
    a=h[-1].get(campo); b=h[-1-k].get(campo)
    if a is None or b is None or b<=0 or a<=0: return None
    return (a/b)**(4/k)-1 if k>=4 else a/b-1

def auc(pool,f,alto=0.10):
    v=[(f(e),e['ret']) for e in pool]
    v=[(a,b) for a,b in v if a is not None]
    if len(v)<8: return None
    thr=np.percentile([b for a,b in v],100*(1-alto))
    pos=[a for a,b in v if b>=thr]; neg=[a for a,b in v if b<thr]
    if not pos or not neg: return None
    return float(np.mean([(p>n)+0.5*(p==n) for p in pos for n in neg]))

VARS={
 'crec. capital invertido 1 anho': lambda e: var_crec(e,'investedCapital',4),
 'crec. capital invertido 2 anhos': lambda e: var_crec(e,'investedCapital',8),
 'capex / depreciacion':           lambda e: e['km'].get('capexToDepreciation'),
 'capex / ventas':                 lambda e: e['km'].get('capexToRevenue'),
 'ROIC (nivel)':                   lambda e: e['roic'],
 '(control) P/S del panel':        lambda e: e['ps'],
}
print()
print("  variable                            pares   impares   veredicto")
print("  "+"-"*62)
for nm,f in VARS.items():
    ap=[];ai=[]
    for y in yrs:
        a=auc(by[y],f)
        if a is None: continue
        (ap if y%2==0 else ai).append(a)
    if not ap or not ai: continue
    mp,mi=np.mean(ap),np.mean(ai)
    ok=abs(mp-0.5)>=0.05 and abs(mi-0.5)>=0.05 and np.sign(mp-0.5)==np.sign(mi-0.5)
    print(f"  {nm:<34} {mp:>6.3f}  {mi:>7.3f}   {'REPLICA' if ok else ('signo ok' if np.sign(mp-0.5)==np.sign(mi-0.5) else 'NO')}")

print()
print("  ¿Y en dinero? alfa INTERNO de la cartera (cuartil bajo) dentro de Industrials:")
print("  variante                      n/anho    CAGR   familia   alfaInt    pares impar")
print("  "+"-"*74)
rng=np.random.default_rng(67)
def cart(f,frac=0.25,rev=False):
    c=[];fam=[];ns=[]
    for y in yrs:
        pool=[e for e in by[y] if f(e) is not None]
        if len(pool)<8: continue
        o=sorted(pool,key=lambda e:f(e),reverse=rev); k=max(1,int(round(len(o)*frac)))
        c.append(np.mean([e['ret'] for e in o[:k]])/100); fam.append(np.mean([e['ret'] for e in by[y]])/100); ns.append(k)
    c=np.array(c);fam=np.array(fam)
    P=[i for i,y in enumerate(yrs) if y%2==0][:len(c)]; I=[i for i,y in enumerate(yrs) if y%2==1][:len(c)]
    P=[i for i in range(len(c)) if yrs[i]%2==0]; I=[i for i in range(len(c)) if yrs[i]%2==1]
    return (np.mean(ns),cagr(c),cagr(fam),(cagr(c)-cagr(fam))*100,
            (cagr(c[P])-cagr(fam[P]))*100,(cagr(c[I])-cagr(fam[I]))*100)
for nm,f in (('P/S bajo 25%',lambda e:e['ps']),('ROIC bajo 25%',lambda e:e['roic']),
             ('capex/depreciacion bajo 25%',lambda e:e['km'].get('capexToDepreciation')),
             ('crec.cap.invertido bajo 25%',lambda e:var_crec(e,'investedCapital',4))):
    n,cg,fm,a,p,i=cart(f)
    print(f"  {nm:<30}{n:>5.0f}  {100*cg:>6.2f}%  {100*fm:>6.2f}%  {a:>+7.2f} pp  {p:>6.1f}{i:>6.1f}")
