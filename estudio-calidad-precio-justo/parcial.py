# EXPLORATORIO — NO PRE-REGISTRADO. No prueba nada; dibuja el intercambio.
# Si la descorrelacion es real y el coste en rentabilidad no esta establecido,
# ¿como es la curva al salir solo PARCIALMENTE del mercado?
import numpy as np
RF=0.02
D=[l.split(',') for l in open('senal_regimen.csv').read().splitlines()[1:]]
yr=np.array([int(r[0]) for r in D]); slv=np.array([float(r[1]) for r in D])/100
qqq=np.array([float(r[2]) for r in D])/100; qprev=np.array([float(r[3]) for r in D])/100
cagr=lambda r: np.prod(1+r)**(1/len(r))-1
corr=lambda a,b: np.corrcoef(a,b)[0,1]
sig=(qprev>0).astype(float)
print(f"  {'exposicion fuera':>16} {'CAGR':>8} {'corr':>7} {'beta':>7} {'peor':>8}")
print(f"  {'(siempre dentro)':>16} {100*cagr(slv):>7.2f}% {corr(slv,qqq):>7.3f} "
      f"{np.cov(slv,qqq,ddof=1)[0,1]/np.var(qqq,ddof=1):>7.2f} {100*slv.min():>7.1f}%")
for w in (0.75,0.5,0.25,0.0):
    e=sig+(1-sig)*w
    p=e*slv+(1-e)*RF
    print(f"  {w:>16.0%} {100*cagr(p):>7.2f}% {corr(p,qqq):>7.3f} "
          f"{np.cov(p,qqq,ddof=1)[0,1]/np.var(qqq,ddof=1):>7.2f} {100*p.min():>7.1f}%")
print()
print(f"  Nasdaq: CAGR {100*cagr(qqq):.2f}%  peor {100*qqq.min():.1f}%")
print()
print("  Sin 2008 (la observacion que manda en la rentabilidad):")
m=yr!=2008
for w in (1.0,0.5,0.0):
    e=sig+(1-sig)*w; p=(e*slv+(1-e)*RF)[m]
    print(f"    fuera al {w:>4.0%}: CAGR {100*cagr(p):>6.2f}%  corr {corr(p,qqq[m]):>6.3f}   "
          f"(base {100*cagr(slv[m]):.2f}% / {corr(slv[m],qqq[m]):.3f})")
