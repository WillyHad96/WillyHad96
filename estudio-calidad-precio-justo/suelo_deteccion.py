# ¿Cual es el efecto anual mas pequenho que este dataset puede distinguir del ruido?
# Bootstrap: carteras ALEATORIAS de n nombres/anho dentro de Industrials.
# El alfa interno de una cartera aleatoria es CERO por construccion; su desviacion
# tipica es el ruido de medicion. Minimo detectable (t=2) = 2 x SE.
import json,glob,os,collections,numpy as np
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
    if e.get('ps') is not None and e['roic'] is not None and e.get('ret') is not None: ev.append(e)
yrs=sorted({e['yr'] for e in ev}); by=collections.defaultdict(list)
for e in ev: by[e['yr']].append(e)
R={y:np.array([e['ret'] for e in by[y]])/100 for y in yrs}
fam={y:R[y].mean() for y in yrs}
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
rng=np.random.default_rng(20260917)
print(f"anhos: {len(yrs)}   nombres/anho en la familia Industrials: {int(np.mean([len(R[y]) for y in yrs]))}")
print()
print("  n/anho    SE del alfa interno    minimo detectable (t=2)")
print("  ------------------------------------------------------")
for n in (7,11,22,45):
    d=[]
    for _ in range(4000):
        pr=[]
        for y in yrs:
            k=min(n,len(R[y]))
            pr.append(R[y][rng.choice(len(R[y]),k,replace=False)].mean())
        d.append((cagr(pr)-cagr([fam[y] for y in yrs]))*100)
    se=np.std(d,ddof=1)
    print(f"  {n:>6}    {se:>13.2f} pp    {2*se:>18.1f} pp anuales")
print()
print("  Magnitudes documentadas en la literatura, para comparar:")
for nm,v in (("valor / HML",3.5),("inversion / CMA",3.5),("rentabilidad / RMW",3.0),
             ("momentum / UMD",7.5),("NUESTRO P/S bajo dentro de Industrials",7.31)):
    print(f"    {nm:<40} {v:>5.2f} pp")

# --- ¿Y si el universo fuera mas ancho? ---
# El bootstrap de arriba sufre correccion por poblacion finita: con n=45 la
# "cartera" ES la familia entera y el ruido cae a cero artificialmente.
# Aqui repetimos el calculo con la MISMA dispersion transversal pero suponiendo
# un universo point-in-time de N nombres/anho, que es lo que no tenemos.
sig=np.mean([R[y].std(ddof=1) for y in yrs])
print()
print(f"  dispersion transversal media dentro del anho: {sig*100:.1f} pp")
print()
print("  universo N/anho   n=11    n=20    n=45   (minimo detectable, pp anuales)")
print("  ---------------------------------------------------------------------")
for N in (45,150,300,1000):
    fila=[]
    for n in (11,20,45):
        if n>=N: fila.append("  --  "); continue
        fpc=1-(n-1)/(N-1)
        se=sig*np.sqrt(fpc/n)/np.sqrt(len(yrs))*100
        fila.append(f"{2*se:>5.1f} ")
    print(f"  {N:>13}   "+"  ".join(fila))

# --- El cuello de botella real: los ANHOS, no el ancho del universo ---
print()
print("  Con 20 nombres/anho (lo que cabe en la cartera del usuario), anhos de historia")
print("  necesarios para que un efecto sea distinguible del ruido con t=2:")
print()
print("    efecto real   anhos necesarios")
print("    ------------------------------")
for ef in (3.0,3.5,5.0,7.3,10.0):
    T=(2*sig*100*np.sqrt(1/20)/ef)**2
    print(f"    {ef:>5.1f} pp        {T:>6.0f}")
