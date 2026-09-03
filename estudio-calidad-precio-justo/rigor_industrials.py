# ¿El alfa de Industrials baratas esta ESTABLECIDO o esta dentro del ruido?
import numpy as np, collections, bisect, math
RF=0.02
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
    if d['sec']=='Indu' and d.get('ps') is not None: ev.append(d)
yrs=sorted({e['yr'] for e in ev}); by=collections.defaultdict(list)
for e in ev: by[e['yr']].append(e)
Q=np.array([np.mean([e['qqq'] for e in by[y]])/100 for y in yrs])
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
def bar(q=0.25):
    r=[];n=[]
    for y in yrs:
        pool=by[y]; v=sorted(x['ps'] for x in pool)
        u=v[max(0,int(len(v)*q)-1)]
        c=[e for e in pool if e['ps']<=u]
        r.append(np.mean([e['ret'] for e in c])/100); n.append(len(c))
    return np.array(r), np.mean(n)
B,n=bar(); F=np.array([np.mean([e['ret'] for e in by[y]])/100 for y in yrs])
N=len(yrs)

def jensen(r,Q):
    """alfa Jensen con su error tipico via regresion OLS."""
    x=Q-RF; y=r-RF
    b=np.cov(y,x,ddof=1)[0,1]/np.var(x,ddof=1); a=y.mean()-b*x.mean()
    res=y-(a+b*x); s2=(res**2).sum()/(len(y)-2)
    se_a=math.sqrt(s2*(1/len(y)+x.mean()**2/((x-x.mean())**2).sum()))
    se_b=math.sqrt(s2/((x-x.mean())**2).sum())
    return a,se_a,a/se_a,b,se_b

print("="*88); print("INDUSTRIALS BARATAS — ¿el alfa aguanta la barra de error?"); print("="*88)
a,se,t,b,seb=jensen(B,Q)
print(f"  n = {N} anhos, {n:.0f} nombres/anho")
print(f"  CAGR {100*cagr(B):.2f}%   Nasdaq {100*cagr(Q):.2f}%   dif {100*(cagr(B)-cagr(Q)):+.2f} pp")
print(f"  ALFA Jensen {100*a:+.2f}%   SE {100*se:.2f}%   **t = {t:+.2f}**")
print(f"  IC95% del alfa: [{100*(a-1.96*se):+.2f}%, {100*(a+1.96*se):+.2f}%]")
print(f"  beta {b:.2f}   SE {seb:.2f}   IC95%: [{b-1.96*seb:.2f}, {b+1.96*seb:.2f}]")
print(f"  vol {100*B.std(ddof=1):.1f}%  vs Nasdaq {100*Q.std(ddof=1):.1f}%")
print(f"  peor anho {100*B.min():.1f}%  vs Nasdaq {100*Q.min():.1f}%")
print(f"  Sharpe (rf=2%) {(cagr(B)-RF)/B.std(ddof=1):.3f}  vs Nasdaq {(cagr(Q)-RF)/Q.std(ddof=1):.3f}")
print(f"  anhos batiendo al Nasdaq: {int(np.sum(B>Q))}/{N}")
print()
print("  --- el alfa INTERNO (baratas - su propia familia), inmune a supervivencia ---")
sp=B-F; ti=sp.mean()/(sp.std(ddof=1)/math.sqrt(N))
print(f"  media {100*sp.mean():+.2f} pp   SE {100*sp.std(ddof=1)/math.sqrt(N):.2f}   **t = {ti:+.2f}**")
print(f"  anhos positivos: {int(np.sum(sp>0))}/{N}")
print()
print("="*88); print("LEAVE-ONE-YEAR-OUT sobre el alfa Jensen"); print("="*88)
As=[]
for i in range(N):
    m=np.ones(N,bool); m[i]=False
    ai,_,ti_,bi,_=jensen(B[m],Q[m]); As.append(ai)
    marca=' <<<' if abs(ai-a)>0.02 else ''
    print(f"  quita {int(yrs[i])}: alfa {100*ai:+6.2f}%  beta {bi:.2f}  t {ti_:+.2f}{marca}")
As=np.array(As)
print(f"\n  rango del alfa: [{100*As.min():+.2f}%, {100*As.max():+.2f}%]")
print(f"  el signo {'CAMBIA' if As.min()*As.max()<0 else 'NO cambia'} al quitar un solo anho")
print()
print("="*88); print("CONTRAFACTUAL ALEATORIO (B2) — 22 nombres al azar de Industrials"); print("="*88)
rng=np.random.default_rng(13); AA=[]
for _ in range(4000):
    rr=[]
    for y in yrs:
        pool=by[y]; k=min(len(pool),int(round(n)))
        idx=rng.choice(len(pool),size=k,replace=False)
        rr.append(np.mean([pool[i]['ret'] for i in idx])/100)
    aa,_,_,_,_=jensen(np.array(rr),Q); AA.append(aa)
AA=np.array(AA)
print(f"  alfa Jensen del azar: media {100*AA.mean():+.2f}%   p95 {100*np.percentile(AA,95):+.2f}%")
print(f"  alfa observado {100*a:+.2f}%  ->  percentil {100*np.mean(AA<a):.1f}   p = {np.mean(AA>=a):.4f}")
