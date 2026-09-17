# ¿Suman P/S bajo + ROIC bajo? Alfa interno y beta, pares/impares.
import json,glob,os,collections,numpy as np,bisect
RF=0.02
SEC={}
for l in open('universo_sectorizado.csv').read().splitlines()[1:]:
    p=l.split(','); SEC.setdefault(p[1],p[3])
KM={}
for f in glob.glob('fmp_raw/*.json'):
    sym=os.path.basename(f)[:-5]
    if SEC.get(sym)!='Indu': continue
    rows=[r for r in json.load(open(f)) if r.get('date')]
    rows.sort(key=lambda r:r['date']); KM[sym]=rows
H=open('ciclicas_ampliado.csv').read().splitlines(); cols=H[0].split(',')
ev=[]
for l in H[1:]:
    p=l.split(','); e={}
    for c,v in zip(cols,p):
        if c=='ticker': e[c]=v
        else:
            try: e[c]=float(v) if v!='' else None
            except: e[c]=None
    if SEC.get(e['ticker'])!='Indu' or e['ticker'] not in KM: continue
    prev=[r for r in KM[e['ticker']] if r['date']<=f"{int(e['yr'])-1}-11-15"]
    if not prev: continue
    e['roic']=prev[-1].get('returnOnInvestedCapital')
    if e.get('ps') is not None and e['roic'] is not None: ev.append(e)
yrs=sorted({e['yr'] for e in ev}); by=collections.defaultdict(list)
for e in ev: by[e['yr']].append(e)
Q=np.array([np.mean([e['qqq'] for e in by[y]])/100 for y in yrs])
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
PAR=[i for i,y in enumerate(yrs) if y%2==0]; IMP=[i for i,y in enumerate(yrs) if y%2==1]
print(f"decisiones: {len(ev)}   anhos: {len(yrs)}   n/anho: {len(ev)/len(yrs):.0f}")

def rk(vals):
    o=sorted(range(len(vals)),key=lambda i:vals[i]); r=[0.0]*len(vals)
    for j,i in enumerate(o): r[i]=j/max(len(vals)-1,1)
    return r

def cartera(sel):
    bar=[];fam=[];ns=[]
    for y in yrs:
        pool=by[y]
        if len(pool)<8: bar.append(0.0); fam.append(0.0); ns.append(0); continue
        c=sel(pool)
        bar.append(np.mean([e['ret'] for e in c])/100 if c else 0.0)
        fam.append(np.mean([e['ret'] for e in pool])/100); ns.append(len(c))
    return np.array(bar),np.array(fam),np.mean(ns)

def q_bajo(pool,var,frac=0.25):
    v=sorted(x[var] for x in pool); u=v[max(0,int(len(v)*frac)-1)]
    return [e for e in pool if e[var]<=u]

def combo(pool,frac=0.25):
    r1=rk([e['ps'] for e in pool]); r2=rk([e['roic'] for e in pool])
    sc=[a+b for a,b in zip(r1,r2)]           # bajo = barato Y poco rentable
    o=sorted(range(len(pool)),key=lambda i:sc[i])
    k=max(1,int(round(len(pool)*frac)))
    return [pool[i] for i in o[:k]]

print()
print("="*104)
print("¿SUMAN? — alfa interno (cartera menos su propia familia Industrials)")
print("="*104)
print(f"  {'variante':<34}{'n/anho':>7}{'CAGR':>9}{'beta':>7}{'alfaJ':>8}{'alfa int':>10}{'t':>7}{'pares':>8}{'impares':>9}")
print("  "+"-"*100)
for nom,sel in [("P/S bajo 25% (base)", lambda p: q_bajo(p,'ps')),
                ("ROIC bajo 25%", lambda p: q_bajo(p,'roic')),
                ("COMBO barato + ROIC bajo 25%", lambda p: combo(p,0.25)),
                ("COMBO 15% (mas estrecho)", lambda p: combo(p,0.15))]:
    bar,fam,n=cartera(sel); sp=bar-fam
    b=np.cov(bar,Q,ddof=1)[0,1]/np.var(Q,ddof=1)
    aj=(bar.mean()-RF)-b*(Q.mean()-RF)
    t=sp.mean()/(sp.std(ddof=1)/np.sqrt(len(sp)))
    print(f"  {nom:<34}{n:>7.0f}{100*cagr(bar):>8.2f}%{b:>7.2f}{100*aj:>7.2f}%{100*sp.mean():>9.2f}{t:>7.2f}"
          f"{100*sp[PAR].mean():>7.1f}{100*sp[IMP].mean():>8.1f}")
famr=np.array([np.mean([e['ret'] for e in by[y]])/100 for y in yrs])
print(f"  {'(familia Industrials)':<34}{len(ev)/len(yrs):>7.0f}{100*cagr(famr):>8.2f}%"
      f"{np.cov(famr,Q,ddof=1)[0,1]/np.var(Q,ddof=1):>7.2f}")
print(f"  {'(Nasdaq)':<34}{'':>7}{100*cagr(Q):>8.2f}%{1.0:>7.2f}")
