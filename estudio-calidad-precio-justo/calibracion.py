# ¿Esta rota la barra de medir? Control positivo: plantamos un efecto de tamanho
# CONOCIDO en los datos y vemos si el mismo procedimiento que usamos siempre lo
# recupera. Si no recupera ni un efecto grande, la barra esta rota.
import json,glob,os,collections,numpy as np
SEC={}
for l in open('universo_sectorizado.csv').read().splitlines()[1:]:
    p=l.split(','); SEC.setdefault(p[1],p[3])
OK={s for s in (os.path.basename(f)[:-5] for f in glob.glob('fmp_raw/*.json')) if SEC.get(s)=='Indu'}
H=open('ciclicas_ampliado.csv').read().splitlines(); cols=H[0].split(',')
by=collections.defaultdict(list)
for l in H[1:]:
    p=dict(zip(cols,l.split(',')))
    if p['ticker'] not in OK: continue
    try: r=float(p['ret']); y=int(float(p['yr'])); ps=float(p['ps'])
    except: continue
    by[y].append(r/100)
yrs=sorted(by); R={y:np.array(by[y]) for y in yrs}
T=len(yrs)
cagr=lambda a: np.prod(1+np.asarray(a))**(1/len(a))-1
rng=np.random.default_rng(11)

EST={
 'media (lo que usamos)': lambda v: v.mean(),
 'mediana':               lambda v: np.median(v),
 'media winsorizada 10%': lambda v: np.clip(v,np.percentile(v,10),np.percentile(v,90)).mean(),
 'media log(1+r)':        lambda v: np.expm1(np.log1p(np.clip(v,-0.95,None)).mean()),
}

def sim(efecto_pp, k, est, nsim=3000):
    """Planta un efecto NETO de efecto_pp contra la familia, en k nombres/anho."""
    f=EST[est]; rec=[]; det=0
    for _ in range(nsim):
        car=[]; fam=[]
        for y in yrs:
            v=R[y].copy(); N=len(v); kk=min(k,N)
            bruto=(efecto_pp/100)/(1-kk/N)          # para que el neto vs familia sea efecto_pp
            idx=rng.choice(N,kk,replace=False)
            v[idx]+=bruto
            car.append(f(v[idx])); fam.append(f(v))
        d=(cagr(car)-cagr(fam))*100
        rec.append(d)
    rec=np.array(rec); se=rec.std(ddof=1)
    # tasa de deteccion: |alfa| > 2*SE_nulo
    return rec.mean(), se

print("="*92)
print("TEST 1 — CONTROL POSITIVO: plantamos un efecto conocido y vemos si la barra lo lee")
print("="*92)
print("  (cartera de 11 nombres/anho, 17 anhos, estimador = media aritmetica, el de siempre)")
print()
m0,se0=sim(0.0,11,'media (lo que usamos)')
print(f"  efecto plantado 0 pp  -> lee {m0:+.2f} pp   (ruido: SE {se0:.2f} pp)   sesgo: {'ninguno' if abs(m0)<0.3 else 'SESGADA'}")
print()
print("  efecto plantado   lo que lee la barra   ¿lo distingue del ruido? (t=2)")
print("  ----------------------------------------------------------------------")
for ef in (2.0,3.5,5.0,7.3,10.0,15.0):
    m,se=sim(ef,11,'media (lo que usamos)')
    t=m/se0
    print(f"  {ef:>6.1f} pp          {m:>+6.2f} pp            t={t:>4.1f}   {'SI' if t>2 else 'NO — invisible'}")

print()
print("="*92)
print("TEST 2 — ¿HAY UNA BARRA MEJOR? Mismo efecto plantado (3,5 pp), distintos estimadores")
print("="*92)
print()
print("  estimador                 lee        ruido(SE)      t     ¿ve un efecto de 3,5 pp?")
print("  ------------------------------------------------------------------------------")
for nm in EST:
    m0n,se0n=sim(0.0,11,nm,2000)
    m,se=sim(3.5,11,nm,2000)
    t=(m-m0n)/se0n
    print(f"  {nm:<24} {m:>+6.2f} pp    {se0n:>5.2f} pp   {t:>5.2f}   {'SI' if t>2 else 'no'}")

print()
print("="*92)
print("TEST 3 — ¿QUE PALANCA IMPORTA? efecto plantado 3,5 pp, estimador de siempre")
print("="*92)
print()
print("  nombres/anho     lee      ruido(SE)      t     ¿visible?")
print("  --------------------------------------------------------")
for k in (5,11,20,30):
    m0n,se0n=sim(0.0,k,'media (lo que usamos)',2000)
    m,se=sim(3.5,k,'media (lo que usamos)',2000)
    t=(m-m0n)/se0n
    print(f"  {k:>8}      {m:>+6.2f} pp   {se0n:>5.2f} pp   {t:>5.2f}   {'SI' if t>2 else 'no'}")
