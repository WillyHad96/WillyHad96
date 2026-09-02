# La MISMA regla R1 pre-registrada, sobre 54 decisiones (1972-2025) en vez de 17.
# Senal validada: reproduce 17/17 las decisiones del panel en 2007-2023.
# Serie: ^IXIC en el ultimo dia de cotizacion <= 15 de febrero.
import numpy as np, math
P={}
for l in open('nasdaq_febrero.csv').read().splitlines()[1:]:
    y,p=l.split(','); P[int(y)]=float(p)
yrs=np.array(sorted(y for y in P if y-1 in P and y+1 in P))       # 1972..2025
idx=np.array([P[y+1]/P[y]-1 for y in yrs])                        # lo que gana el anho Y
sig=np.array([1.0 if P[y]/P[y-1]-1 > 0 else 0.0 for y in yrs])    # senal R1
n=len(yrs)
cagr=lambda r: np.prod(1+r)**(1/len(r))-1

print("="*80)
print(f"R1 SOBRE EL INDICE — {n} decisiones ({yrs[0]}-{yrs[-1]}), frente a 17 antes")
print("="*80)
print(f"  dentro {int(sig.sum())}/{n} anhos  ·  fuera en: {', '.join(str(y) for y,s in zip(yrs,sig) if s==0)}")
print()
for rf,lab in [(0.0,'efectivo al 0%'),(0.02,'efectivo al 2%'),(0.05,'efectivo al 5%')]:
    ov=sig*idx+(1-sig)*rf
    dif=ov-idx
    t=dif.mean()/(dif.std(ddof=1)/math.sqrt(n))
    print(f"  {lab:<16} overlay {100*cagr(ov):6.2f}%   indice {100*cagr(idx):6.2f}%   "
          f"dif {100*(cagr(ov)-cagr(idx)):+6.2f} pp   t(pareado) {t:+5.2f}   corr {np.corrcoef(ov,idx)[0,1]:.3f}")
print()
print("  NOTA: el tipo sin riesgo real fue 8-15% en 1972-1990. Usar 2% plano")
print("  INFRAVALORA la regla en ese tramo: el test largo es CONSERVADOR.")

RF=0.02
ov=sig*idx+(1-sig)*RF
dif=ov-idx
print()
print("="*80)
print("PERMUTACION (mismo numero de salidas, al azar) — 20.000 it, semilla 13")
print("="*80)
rng=np.random.default_rng(13); IT=20000
E=np.array([rng.permutation(sig) for _ in range(IT)])
Pf=E*idx+(1-E)*RF
cg=np.prod(1+Pf,axis=1)**(1/n)-1
pm=Pf-Pf.mean(axis=1,keepdims=True); qm=idx-idx.mean()
cr=(pm@qm)/np.sqrt((pm**2).sum(axis=1)*(qm**2).sum())
obs_c,obs_r=cagr(ov),np.corrcoef(ov,idx)[0,1]
print(f"  CAGR observado {100*obs_c:.2f}%  vs azar {100*cg.mean():.2f}%   p={np.mean(cg>=obs_c):.4f}")
print(f"  corr observada {obs_r:.3f}      vs azar {cr.mean():.3f}       p={np.mean(cr<=obs_r):.4f}")
print(f"  DESCORRELACION REAL = {obs_r-cr.mean():+.3f}")
print(f"  p CONJUNTA = {np.mean((cg>=obs_c)&(cr<=obs_r)):.4f}")

print()
print("="*80)
print("¿FUE 2007-2023 UNA VENTANA REPRESENTATIVA? — todas las ventanas de 17 anhos")
print("="*80)
W=17; res=[]
for i in range(n-W+1):
    s=slice(i,i+W)
    o=sig[s]*idx[s]+(1-sig[s])*RF
    res.append((yrs[i],yrs[i+W-1],cagr(o)-cagr(idx[s]),np.corrcoef(o,idx[s])[0,1]-np.corrcoef(idx[s],idx[s])[0,1]))
d=np.array([r[2] for r in res])
print(f"  {len(res)} ventanas solapadas de 17 anhos")
print(f"  dCAGR: mediana {100*np.median(d):+.2f} pp   rango [{100*d.min():+.2f}, {100*d.max():+.2f}] pp")
print(f"  ventanas donde la regla MEJORA el CAGR: {np.sum(d>0)}/{len(res)} ({100*np.mean(d>0):.0f}%)")
print()
print(f"  {'ventana':>13} {'dCAGR':>9}")
for a,b,dd,_ in res:
    marca=' <<< la nuestra' if a==2007 else ''
    print(f"  {a}-{b} {100*dd:>+8.2f}{marca}")
