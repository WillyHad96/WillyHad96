# Robustez del resultado pre-registrado: leave-one-year-out.
# NO es una hipotesis nueva: comprueba si el efecto vive en una sola observacion.
import numpy as np, math
RF=0.02
D=[l.split(',') for l in open('senal_regimen.csv').read().splitlines()[1:]]
yr=np.array([int(r[0]) for r in D]); slv=np.array([float(r[1]) for r in D])/100
qqq=np.array([float(r[2]) for r in D])/100; qprev=np.array([float(r[3]) for r in D])/100
mmom=np.array([float(r[4]) for r in D])/100
cagr=lambda r: np.prod(1+r)**(1/len(r))-1
corr=lambda a,b: np.corrcoef(a,b)[0,1]

for nom,e in [("R1 indice",(qprev>0).astype(float)),("R2 universo",(mmom>0).astype(float))]:
    print("="*78); print(f"{nom} — leave-one-year-out"); print("="*78)
    p=e*slv+(1-e)*RF
    full_d=cagr(p)-cagr(slv); full_r=corr(p,qqq)-corr(slv,qqq)
    print(f"  completo: dCAGR {100*full_d:+6.2f} pp   dcorr {full_r:+.3f}")
    print(f"  {'quita':>6} {'dCAGR':>9} {'dcorr':>9}   {'anho fuera?':>12}")
    filas=[]
    for i,y in enumerate(yr):
        m=np.ones(len(yr),bool); m[i]=False
        pp=e[m]*slv[m]+(1-e[m])*RF
        d=cagr(pp)-cagr(slv[m]); r=corr(pp,qqq[m])-corr(slv[m],qqq[m])
        filas.append((y,d,r,e[i]))
    for y,d,r,ei in filas:
        flag="FUERA" if ei==0 else ""
        marca=" <<<" if abs(d-full_d)>0.02 else ""
        print(f"  {y:>6} {100*d:>+8.2f} {r:>+9.3f}   {flag:>12}{marca}")
    ds=[d for _,d,_,_ in filas]; rs=[r for _,_,r,_ in filas]
    print(f"  rango dCAGR: [{100*min(ds):+.2f}, {100*max(ds):+.2f}] pp   "
          f"rango dcorr: [{min(rs):+.3f}, {max(rs):+.3f}]")
    print(f"  -> el signo de dCAGR {'CAMBIA' if min(ds)*max(ds)<0 else 'NO cambia'} al quitar un solo anho")
    print()

print("="*78); print("¿Cuanto vale, mecanicamente, esquivar solo 2008?"); print("="*78)
i08=int(np.where(yr==2008)[0][0])
e=np.zeros(len(yr)); e[:]=1; e[i08]=0
p=e*slv+(1-e)*RF
print(f"  Oraculo que solo esquiva 2008: CAGR {100*cagr(p):.2f}%  corr {corr(p,qqq):.3f}  "
      f"(base {100*cagr(slv):.2f}% / {corr(slv,qqq):.3f})")
print(f"  -> esquivar UNA observacion vale {100*(cagr(p)-cagr(slv)):+.2f} pp de CAGR "
      f"y {corr(p,qqq)-corr(slv,qqq):+.3f} de correlacion.")
print()
e1=(qprev>0).astype(float)
m=yr!=2008
p1=e1[m]*slv[m]+(1-e1[m])*RF
print(f"  R1 SIN 2008: CAGR {100*cagr(p1):.2f}% vs base {100*cagr(slv[m]):.2f}%  "
      f"({100*(cagr(p1)-cagr(slv[m])):+.2f} pp)")
print(f"               corr {corr(p1,qqq[m]):.3f} vs base {corr(slv[m],qqq[m]):.3f}  "
      f"({corr(p1,qqq[m])-corr(slv[m],qqq[m]):+.3f})")
print()
print("  Sin 2008 la regla sigue saliendo en 2009, 2016 y 2023 — tres rebotes fuertes.")
