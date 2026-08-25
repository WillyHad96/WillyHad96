import numpy as np
# yr, perfil, top30, top10, spy  (%)
D=[(2007,-8.31,-9.63,3.94,-5.86),(2008,-36.67,-37.27,-32.51,-41.01),(2009,62.94,37.86,41.40,41.60),
(2010,33.92,43.40,54.21,20.78),(2011,7.55,24.04,28.21,2.71),(2012,20.23,22.39,27.13,13.07),
(2013,38.46,41.25,41.83,23.30),(2014,9.96,5.51,3.16,13.20),(2015,-13.02,-12.73,-13.77,-6.75),
(2016,44.47,36.29,34.46,25.07),(2017,20.53,24.98,35.09,17.37),(2018,6.91,12.81,28.97,1.05),
(2019,9.81,18.25,34.69,16.46),(2020,44.08,45.05,61.79,26.68),(2021,4.40,0.14,-6.53,12.86),
(2022,5.44,15.94,18.03,-9.35),(2023,21.77,32.80,63.33,23.34),(2024,20.51,28.29,44.38,18.59)]
A=np.array(D,float); yr=A[:,0].astype(int); spy=A[:,4]/100
RF=0.02
# costes: perfil rota ~41%/anio -> 0,25%; top30 y top10 rotan mas al reordenar por momentum -> 0,60% y 0,90%
def st(col,cost,lab,n=None):
    r=A[:,col]/100-cost; k=len(r)
    cagr=np.prod(1+r)**(1/k)-1; vol=r.std(ddof=1)
    beta=np.cov(r,spy,ddof=1)[0,1]/np.var(spy,ddof=1)
    alpha=(r.mean()-RF)-beta*(spy.mean()-RF)
    nm=f"{n:>6}" if n else "     -"
    print(f"{lab:<30}{nm}{100*cagr:>8.2f}{100*vol:>7.1f}{(cagr-RF)/vol:>8.2f}{beta:>6.2f}{100*alpha:>7.2f}{100*r.min():>8.1f}{100*np.mean(r>spy):>7.1f}")
print(f"{'cartera':<30}{'n/año':>6}{'CAGR':>8}{'vol':>7}{'Sharpe':>8}{'beta':>6}{'alfa':>7}{'peor':>8}{'%>SPY':>7}")
print("-"*88)
st(1,0.0025,"PERFIL completo",151)
st(2,0.0060,"PERFIL + top 30% momentum",44)
st(3,0.0090,"PERFIL + top 10% momentum",15)
st(4,0.0,"SPY")
print("\n--- prueba ciega ---")
for lo,hi in [(2007,2015),(2016,2024)]:
    m=(yr>=lo)&(yr<=hi); k=m.sum()
    o=[]
    for c,cost,nm in [(1,0.0025,"PERFIL"),(2,0.0060,"top30"),(3,0.0090,"top10"),(4,0.0,"SPY")]:
        r=A[m,c]/100-cost
        o.append(f"{nm} {100*(np.prod(1+r)**(1/k)-1):6.2f}%")
    print(f"  {lo}-{hi}: " + "  ·  ".join(o))
