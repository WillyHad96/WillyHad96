# El cuartil BARATO dentro de CADA subtipo por separado, con alfa y beta.
# Objetivo: encontrar alfa a correlacion baja, no CAGR a correlacion alta.
import numpy as np, collections, bisect
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
    if d['sec'] and d.get('ps') is not None: ev.append(d)
NOM={'Cons':'Consumer Cyclical','Indu':'Industrials','Basi':'Basic Materials','Ener':'Energy'}
yrs=sorted({e['yr'] for e in ev}); by=collections.defaultdict(list)
for e in ev: by[e['yr']].append(e)
Q=np.array([np.mean([e['qqq'] for e in by[y]])/100 for y in yrs])
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
buenos=Q>0; malos=~buenos
PAR=[i for i,y in enumerate(yrs) if y%2==0]; IMP=[i for i,y in enumerate(yrs) if y%2==1]

def cuartil_barato(s, q=0.25):
    r=[];n=[]
    for y in yrs:
        pool=[e for e in by[y] if e['sec']==s]
        if len(pool)<8: r.append(0.0); n.append(0); continue
        v=sorted(x['ps'] for x in pool)
        u=v[max(0,int(len(v)*q)-1)]
        c=[e for e in pool if e['ps']<=u]
        r.append(np.mean([e['ret'] for e in c])/100); n.append(len(c))
    return np.array(r), np.mean(n)

def stats(r):
    c=np.corrcoef(r,Q)[0,1]; b=np.cov(r,Q,ddof=1)[0,1]/np.var(Q,ddof=1)
    return cagr(r), c, b, (r.mean()-RF)-b*(Q.mean()-RF), r.std(ddof=1)

print("="*112)
print("EL CUARTIL BARATO DENTRO DE CADA SUBTIPO — buscando alfa a correlacion baja")
print("="*112)
print(f"  {'cartera':<28}{'n/anho':>7}{'CAGR':>9}{'corr':>7}{'beta':>7}{'ALFA':>8}{'vol':>7}"
      f"{'malos anhos':>13}{'alfa pares':>12}{'impares':>10}")
print("  "+"-"*108)
for s in ('Cons','Indu','Basi','Ener'):
    fam=np.array([np.mean([e['ret'] for e in by[y] if e['sec']==s])/100 for y in yrs])
    bar,n=cuartil_barato(s)
    cf,_,_,af,_=stats(fam); cb,c,b,a,v=stats(bar)
    sp=bar-fam
    print(f"  {NOM[s]+' TODAS':<28}{len([e for e in ev if e['sec']==s])/len(yrs):>7.0f}"
          f"{100*cf:>8.2f}%{np.corrcoef(fam,Q)[0,1]:>7.3f}"
          f"{np.cov(fam,Q,ddof=1)[0,1]/np.var(Q,ddof=1):>7.2f}{100*af:>7.2f}%{100*fam.std(ddof=1):>6.1f}%"
          f"{100*fam[malos].mean():>12.1f}%{'':>12}{'':>10}")
    print(f"  {'  -> BARATAS 25%':<28}{n:>7.0f}{100*cb:>8.2f}%{c:>7.3f}{b:>7.2f}{100*a:>7.2f}%{100*v:>6.1f}%"
          f"{100*bar[malos].mean():>12.1f}%{100*sp[PAR].mean():>11.1f}%{100*sp[IMP].mean():>9.1f}%")
print(f"  {'Nasdaq':<28}{'':>7}{100*cagr(Q):>8.2f}%{1.0:>7.3f}{1.0:>7.2f}{0.0:>7.2f}%{100*Q.std(ddof=1):>6.1f}%"
      f"{100*Q[malos].mean():>12.1f}%")
print()
print("  'malos anhos' = retorno medio en los 4 anhos en que el Nasdaq cayo.")
print("  'alfa pares/impares' = media anual de (baratas - su propia familia), por mitades.")
