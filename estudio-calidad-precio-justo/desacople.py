# ¿CAGR y correlacion estan atados por naturaleza, o es beta de mercado alcista?
# Descompone CAGR = beta*mercado + alfa, y mide la correlacion del ALFA, no de la cartera.
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
    if d['sec']: ev.append(d)
NOM={'Cons':'Consumer Cyclical','Indu':'Industrials','Basi':'Basic Materials','Ener':'Energy'}
yrs=sorted({e['yr'] for e in ev}); by=collections.defaultdict(list)
for e in ev: by[e['yr']].append(e)
Q=np.array([np.mean([e['qqq'] for e in by[y]])/100 for y in yrs])
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
def pct(e,pool,var,lo,hi):
    v=sorted(x[var] for x in pool if x.get(var) is not None)
    if e.get(var) is None or not v: return False
    p=bisect.bisect_left(v,e[var])/max(len(v)-1,1); return lo<=p<hi

def serie(sel):
    r=[]
    for y in yrs:
        c=[e for e in by[y] if sel(e,by[y])]
        r.append(np.mean([e['ret'] for e in c])/100 if c else 0.0)
    return np.array(r)

def stats(r):
    c=np.corrcoef(r,Q)[0,1]; b=np.cov(r,Q,ddof=1)[0,1]/np.var(Q,ddof=1)
    alfa=(r.mean()-RF)-b*(Q.mean()-RF)
    return cagr(r), c, r.std(ddof=1), b, alfa

print("="*104)
print("1. DESCOMPONER: ¿el CAGR extra es ALFA o es BETA?")
print("="*104)
print(f"  {'cartera':<34}{'CAGR':>9}{'corr':>8}{'vol':>8}{'beta':>7}{'ALFA Jensen':>13}{'ret sin beta':>14}")
print("  "+"-"*100)
filas=[]
for s in ('Cons','Indu','Basi','Ener'):
    r=serie(lambda e,p,s=s: e['sec']==s)
    cg,c,v,b,a=stats(r)
    filas.append((NOM[s],cg,c,b,a))
    print(f"  {NOM[s]:<34}{100*cg:>8.2f}%{c:>8.3f}{100*v:>7.1f}%{b:>7.2f}{100*a:>12.2f}%{100*(cg-b*cagr(Q)):>13.2f}%")
r_bar=serie(lambda e,p: e['sec'] in ('Indu','Basi') and pct(e,[x for x in p if x['sec'] in ('Indu','Basi')],'ps',0.0,0.25))
r_fam=serie(lambda e,p: e['sec'] in ('Indu','Basi'))
for nom,r in [("BARATAS Indu+Basi (C21)",r_bar),("familia Indu+Basi",r_fam)]:
    cg,c,v,b,a=stats(r); filas.append((nom,cg,c,b,a))
    print(f"  {nom:<34}{100*cg:>8.2f}%{c:>8.3f}{100*v:>7.1f}%{b:>7.2f}{100*a:>12.2f}%{100*(cg-b*cagr(Q)):>13.2f}%")
print(f"  {'Nasdaq':<34}{100*cagr(Q):>8.2f}%{1.0:>8.3f}{100*Q.std(ddof=1):>7.1f}%{1.0:>7.2f}{0.0:>12.2f}%{0.0:>13.2f}%")

print()
print("="*104)
print("2. ¿ESTAN ATADOS? — correlacion entre las columnas, sobre las 6 carteras")
print("="*104)
CG=np.array([f[1] for f in filas]); CO=np.array([f[2] for f in filas]); AL=np.array([f[4] for f in filas])
print(f"  corr(CAGR, correlacion con Nasdaq) = {np.corrcoef(CG,CO)[0,1]:+.3f}   <- lo que has visto tu")
print(f"  corr(ALFA, correlacion con Nasdaq) = {np.corrcoef(AL,CO)[0,1]:+.3f}   <- lo que importa")
print()
print("  Si la primera es alta y la segunda no, el CAGR extra era beta, no habilidad,")
print("  y el alfa SI se puede buscar con correlacion baja.")

print()
print("="*104)
print("3. LA PRUEBA DE FUEGO — ¿el ALFA de C21 correlaciona con el Nasdaq?")
print("="*104)
spread = r_bar - r_fam    # baratas menos su propio pool: el alfa puro, sin beta de mercado
print(f"  serie del alfa (baratas - familia), anho a anho:")
print("   "+" ".join(f"{int(y)}:{100*x:+.0f}" for y,x in zip(yrs,spread)))
print(f"   Nasdaq: "+" ".join(f"{int(y)}:{100*x:+.0f}" for y,x in zip(yrs,Q)))
print()
print(f"  media del alfa        {100*spread.mean():+.2f} pp     vol {100*spread.std(ddof=1):.1f}%")
print(f"  CORRELACION del alfa con el Nasdaq: {np.corrcoef(spread,Q)[0,1]:+.3f}")
print(f"  beta del alfa al Nasdaq:            {np.cov(spread,Q,ddof=1)[0,1]/np.var(Q,ddof=1):+.3f}")
print(f"  anhos con alfa positivo: {int(np.sum(spread>0))}/{len(yrs)}")

print()
print("="*104)
print("4. ¿SE INVIERTE LA RELACION EN ANHOS MALOS? — el test de que es beta de alcista")
print("="*104)
buenos=Q>0; malos=~buenos
print(f"  anhos buenos del Nasdaq: {int(buenos.sum())}   malos: {int(malos.sum())}")
print(f"  {'cartera':<34}{'CAGR anhos BUENOS':>20}{'CAGR anhos MALOS':>20}")
for s in ('Cons','Indu','Basi','Ener'):
    r=serie(lambda e,p,s=s: e['sec']==s)
    print(f"  {NOM[s]:<34}{100*r[buenos].mean():>19.1f}%{100*r[malos].mean():>19.1f}%")
print(f"  {'Nasdaq':<34}{100*Q[buenos].mean():>19.1f}%{100*Q[malos].mean():>19.1f}%")
