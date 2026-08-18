import numpy as np
from math import comb
# yr, perf20, resto20, perf_r4, spy_r4
D=[(2007,22.69,4.08,-10.31,-5.65),(2008,35.01,4.98,-35.57,-41.06),(2009,34.93,5.96,64.95,45.10),
(2010,17.80,1.03,33.60,20.93),(2011,4.88,-15.95,8.35,2.66),(2012,18.62,-8.56,18.61,12.39),
(2013,2.54,-13.59,36.17,22.26),(2014,-11.62,-18.54,10.86,12.60),(2015,-17.76,-24.32,-13.35,-6.08),
(2016,2.06,-18.43,47.09,25.45),(2017,-16.50,-27.96,20.34,16.41),(2018,-1.02,-20.64,3.62,1.10),
(2019,-4.50,-32.06,7.58,15.58),(2020,-8.96,-27.57,40.67,28.43),(2021,-6.46,-22.80,6.82,13.54),
(2022,None,None,7.91,-8.33),(2023,None,None,19.84,21.96),(2024,None,None,19.54,18.96)]
yr=np.array([d[0] for d in D])
m=np.array([d[1] is not None for d in D])
dif=np.array([ (d[1]-d[2]) if d[1] is not None else np.nan for d in D])
r=np.array([d[3] for d in D])/100; spy=np.array([d[4] for d in D])/100
RF=0.02

d=dif[m]; n=len(d); pos=int((d>0).sum())
print("=== PERFIL (dilucion<2% + margen bruto estable + crecimiento consistente, sin Fin/RE) ===")
print(f"efecto 20T vs resto: {d.mean():+.2f} pp   EE {d.std(ddof=1)/np.sqrt(n):.2f}   t {d.mean()/(d.std(ddof=1)/np.sqrt(n)):.2f}   {pos}/{n} cohortes")
print(f"  banda de ruido por permutacion (p95) = 5.77 pp  ->  efecto = {d.mean()/5.77:.1f}x la banda")
ins=(yr[m]<=2016); out=(yr[m]>=2017)
print(f"  EN muestra 2007-2016 : {d[ins].mean():+.2f} pp   ({int((d[ins]>0).sum())}/{ins.sum()})")
print(f"  FUERA muestra 2017-21: {d[out].mean():+.2f} pp   ({int((d[out]>0).sum())}/{out.sum()})   degradacion {100*(1-d[out].mean()/d[ins].mean()):.0f}%")

def stats(r,bm,lab,cost=0.006):
    r=r-cost; n=len(r)
    cagr=np.prod(1+r)**(1/n)-1; arit=r.mean(); vol=r.std(ddof=1)
    beta=np.cov(r,bm,ddof=1)[0,1]/np.var(bm,ddof=1)
    alpha=(arit-RF)-beta*(bm.mean()-RF)
    print(f"{lab:<26}{100*cagr:>7.2f}{100*arit:>8.2f}{100*vol:>7.1f}{(cagr-RF)/vol:>7.2f}{beta:>6.2f}{100*alpha:>7.2f}{100*r.min():>8.1f}{100*np.mean(r>bm):>7.1f}")

print(f"\n=== Cartera anual 2007-2024 (n={len(r)} años, ~90-143 nombres, neta 0,60%/año) ===")
print(f"{'cartera':<26}{'CAGR':>7}{'media':>8}{'vol':>7}{'Sharpe':>7}{'beta':>6}{'alfa':>7}{'peor':>8}{'%>SPY':>7}")
print("-"*83)
stats(r,spy,"PERFIL")
stats(spy,spy,"SPY",cost=0.0)
print("\nReferencias del estudio: CALIDAD 5/5 Sharpe 0,42 · MEDIOCRE-T1 barato Sharpe 0,28 · liston previo 0,60")
