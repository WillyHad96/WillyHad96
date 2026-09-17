# Rehacer el hallazgo principal (P/S bajo dentro de Industrials) con retornos
# RECALCULADOS desde precio_post (verificado contra FMP) en vez de la columna fwd_4t.
import collections,numpy as np
NEW={}
for l in open('industrials_ret_real.csv').read().splitlines()[1:]:
    y,t,f,r,ps=l.split(',')
    NEW[(t,int(y))]=(float(r)/100,float(ps))
OLD={}
H=open('ciclicas_ampliado.csv').read().splitlines(); cols=H[0].split(',')
for l in H[1:]:
    p=dict(zip(cols,l.split(',')))
    try: OLD[(p['ticker'],int(float(p['yr'])))]=(float(p['ret'])/100,float(p['ps']))
    except: pass
com=sorted(set(NEW)&set(OLD))
print(f"observaciones en ambos: {len(com)}   (nuevo {len(NEW)}, viejo {len(OLD)})")
d=[abs(NEW[k][0]-OLD[k][0])*100 for k in com]
sg=sum(1 for k in com if np.sign(NEW[k][0])!=np.sign(OLD[k][0]))
print(f"diferencia mediana entre columnas: {np.median(d):.2f} pp   media {np.mean(d):.2f} pp   p90 {np.percentile(d,90):.2f} pp")
print(f"signo distinto en {sg} de {len(com)} ({100*sg/len(com):.1f}%)")
cagr=lambda a: np.prod(1+np.asarray(a))**(1/len(a))-1
rng=np.random.default_rng(3)

def corre(src,etq):
    by=collections.defaultdict(list)
    for k in com:
        r,ps=src[k]; by[k[1]].append((ps,r))
    yrs=sorted(by)
    car=[];fam=[];ns=[]
    for y in yrs:
        v=sorted(by[y]); k=max(1,int(round(len(v)*0.25)))
        car.append(np.mean([x[1] for x in v[:k]])); fam.append(np.mean([x[1] for x in by[y]])); ns.append(k)
    car=np.array(car);fam=np.array(fam)
    a=(cagr(car)-cagr(fam))*100
    dd=[]
    for _ in range(4000):
        c=[]
        for i,y in enumerate(yrs):
            allr=np.array([x[1] for x in by[y]])
            c.append(allr[rng.choice(len(allr),ns[i],replace=False)].mean())
        dd.append((cagr(c)-cagr(fam))*100)
    se=np.std(dd,ddof=1)
    P=[i for i,y in enumerate(yrs) if y%2==0]; I=[i for i,y in enumerate(yrs) if y%2==1]
    ap=(cagr(car[P])-cagr(fam[P]))*100; ai=(cagr(car[I])-cagr(fam[I]))*100
    print(f"  {etq:<34} {np.mean(ns):>4.0f}  {cagr(car)*100:>6.2f}%  {cagr(fam)*100:>6.2f}%  {a:>+7.2f} pp  {a/se:>5.2f}  {ap:>6.1f}  {ai:>6.1f}")

print()
print("  columna de retorno usada          n/anho   CAGR   familia   alfa int      t   pares impares")
print("  --------------------------------------------------------------------------------------------")
corre(OLD,'fwd_4t del panel (lo de siempre)')
corre(NEW,'RECALCULADO desde precio_post')

print()
print("  Muestra COMPLETA con precios verificados (990 obs, sin exigir key-metrics):")
print("  frac   n/anho   CAGR   familia   alfa int      t   pares impares")
print("  ------------------------------------------------------------------")
by=collections.defaultdict(list)
for k,(r,ps) in NEW.items(): by[k[1]].append((ps,r))
yrs=sorted(by)
for frac in (0.15,0.25,0.35,0.50):
    car=[];fam=[];ns=[]
    for y in yrs:
        v=sorted(by[y]); k=max(1,int(round(len(v)*frac)))
        car.append(np.mean([x[1] for x in v[:k]])); fam.append(np.mean([x[1] for x in by[y]])); ns.append(k)
    car=np.array(car);fam=np.array(fam); a=(cagr(car)-cagr(fam))*100
    dd=[]
    for _ in range(4000):
        c=[]
        for i,y in enumerate(yrs):
            allr=np.array([x[1] for x in by[y]]); c.append(allr[rng.choice(len(allr),ns[i],replace=False)].mean())
        dd.append((cagr(c)-cagr(fam))*100)
    se=np.std(dd,ddof=1)
    P=[i for i,y in enumerate(yrs) if y%2==0]; I=[i for i,y in enumerate(yrs) if y%2==1]
    print(f"  {frac:.0%}     {np.mean(ns):>5.0f}  {cagr(car)*100:>6.2f}%  {cagr(fam)*100:>6.2f}%  {a:>+7.2f} pp  {a/se:>5.2f}  {(cagr(car[P])-cagr(fam[P]))*100:>6.1f}  {(cagr(car[I])-cagr(fam[I]))*100:>6.1f}   (suelo {2*se:.1f} pp)")

print()
print("  ¿Cuanto ruido metia la columna corrupta? Suelo de deteccion con cada columna,")
print("  misma muestra de 772, cartera de 11 nombres:")
for src,etq in ((OLD,'fwd_4t del panel'),(NEW,'precio_post recalculado')):
    b=collections.defaultdict(list)
    for k in com: b[k[1]].append(src[k][0])
    ys=sorted(b); fam=[np.mean(b[y]) for y in ys]
    dd=[]
    for _ in range(4000):
        c=[]
        for y in ys:
            a2=np.array(b[y]); c.append(a2[rng.choice(len(a2),min(11,len(a2)),replace=False)].mean())
        dd.append((cagr(c)-cagr(fam))*100)
    se=np.std(dd,ddof=1)
    print(f"    {etq:<26} SE {se:.2f} pp  ->  suelo {2*se:.1f} pp")
