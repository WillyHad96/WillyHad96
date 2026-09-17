# Libreria comun para rehacer los estudios con retornos verificados (hallazgo A9).
# El retorno viene de base_corregida.csv, recalculado como p4/precio_post-1.
import collections, numpy as np
RF=0.02

def _serie(f):
    d={}
    for l in open(f).read().splitlines()[1:]:
        a,b=l.split(','); d[a]=float(b)
    return sorted(d), d

def carga(con_indice=True):
    H=open('base_corregida.csv').read().splitlines(); cols=H[0].split(',')
    ev=[]
    for l in H[1:]:
        p=dict(zip(cols,l.split(',')))
        e={'ticker':p['ticker'],'yr':int(p['yr']),'fecha':p['fecha'],'sector':p['sector']}
        ok=True
        for c in ('ret','ps','mcap','mom','r40','sdmb','sdcr','mb','cr'):
            try: e[c]=float(p[c])
            except: ok=False; break
        if ok: e['f4']=p['f4']; ev.append(e)
    if con_indice:
        import bisect
        IX=_serie('ixic_diario.csv'); QQ=_serie('qqq_diario.csv')
        out=[]
        for e in ev:
            bien=True
            for nom,(ds,d) in (('ixic',IX),('qqq',QQ)):
                i=bisect.bisect_right(ds,e['fecha'])-1; j=bisect.bisect_right(ds,e['f4'])-1
                if i<0 or j<0 or ds[i]<'2006-10-31': bien=False; break
                e[nom]=(d[ds[j]]/d[ds[i]]-1)*100
            if bien: out.append(e)
        ev=out
    return ev

def nasdaq():
    d={int(l.split(',')[0]):float(l.split(',')[1]) for l in open('nasdaq_febrero.csv').read().splitlines()[1:]}
    # retorno de feb(y) a feb(y+1)
    return {y:(d[y+1]/d[y]-1) for y in d if y+1 in d}

cagr=lambda r: float(np.prod(1+np.asarray(r))**(1/len(r))-1)

def pr(vals):
    """percent_rank como en SQL: fraccion de valores estrictamente menores."""
    o=sorted(range(len(vals)),key=lambda i:vals[i]); r=[0.0]*len(vals); n=len(vals)
    i=0
    while i<n:
        j=i
        while j+1<n and vals[o[j+1]]==vals[o[i]]: j+=1
        for k in range(i,j+1): r[o[k]]=i/max(n-1,1)
        i=j+1
    return r

def stats(r,bm,etq,extra=''):
    r=np.asarray(r); bm=np.asarray(bm)
    beta=np.cov(r,bm,ddof=1)[0,1]/np.var(bm,ddof=1)
    alfa=(r.mean()-RF)-beta*(bm.mean()-RF)
    corr=np.corrcoef(r,bm)[0,1]
    print(f"  {etq:<32}{100*cagr(r):>8.2f}%{100*r.std(ddof=1):>8.1f}%{beta:>7.2f}{100*alfa:>8.2f}%{corr:>8.3f}  {extra}")
    return dict(cagr=cagr(r),vol=r.std(ddof=1),beta=beta,alfa=alfa,corr=corr)

def cab():
    print(f"  {'':<32}{'CAGR':>9}{'vol':>9}{'beta':>7}{'alfaJ':>9}{'corr':>8}")
    print("  "+"-"*78)

def ruido_interno(by, ns, yrs, fam, nsim=4000, seed=11):
    """SE del alfa interno para carteras aleatorias del mismo tamanho."""
    rng=np.random.default_rng(seed); d=[]
    for _ in range(nsim):
        c=[]
        for i,y in enumerate(yrs):
            a=np.array([e['ret'] for e in by[y]])/100
            c.append(a[rng.choice(len(a),min(ns[i],len(a)),replace=False)].mean())
        d.append((cagr(c)-cagr(fam))*100)
    return float(np.std(d,ddof=1))
