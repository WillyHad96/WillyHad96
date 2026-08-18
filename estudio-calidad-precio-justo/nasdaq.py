import numpy as np
D=[(2007,-6.51,-5.93,-0.05),(2008,-36.56,-40.90,-30.91),(2009,65.79,42.79,55.48),(2010,34.70,20.59,28.83),
(2011,8.08,2.73,9.01),(2012,18.96,12.94,8.27),(2013,39.96,23.53,32.71),(2014,12.27,13.28,17.83),
(2015,-13.71,-6.69,-2.94),(2016,47.18,25.77,30.12),(2017,22.24,17.52,27.12),(2018,9.68,1.04,3.64),
(2019,8.96,16.50,25.74),(2020,47.67,27.31,47.94),(2021,3.93,12.77,7.68),(2022,4.42,-9.28,-17.51),
(2023,22.25,23.34,37.20),(2024,20.05,18.60,19.10)]
A=np.array(D,float); yr=A[:,0].astype(int)
perf=A[:,1]/100-0.0025; spy=A[:,2]/100; qqq=A[:,3]/100
RF=0.02
def st(r,bm,lab):
    k=len(r); cagr=np.prod(1+r)**(1/k)-1; ar=r.mean(); vol=r.std(ddof=1)
    beta=np.cov(r,bm,ddof=1)[0,1]/np.var(bm,ddof=1)
    alpha=(ar-RF)-beta*(bm.mean()-RF)
    print(f"{lab:<34}{100*cagr:>8.2f}{100*vol:>7.1f}{(cagr-RF)/vol:>8.2f}{beta:>7.2f}{100*alpha:>8.2f}{100*r.min():>8.1f}{100*np.mean(r>bm):>8.1f}")
print(f"{'':<34}{'CAGR':>8}{'vol':>7}{'Sharpe':>8}{'beta':>7}{'alfa':>8}{'peor':>8}{'%>bench':>8}")
print("-"*80); print("--- contra SPY ---")
st(perf,spy,"PERFIL")
st(spy,spy,"SPY")
print("--- contra NASDAQ (QQQ) ---")
st(perf,qqq,"PERFIL")
st(qqq,qqq,"QQQ (NASDAQ 100)")
print()
c=lambda r: 100*(np.prod(1+r)**(1/len(r))-1)
print(f"1$ en 2007 -> PERFIL {np.prod(1+perf):.2f}$  ·  QQQ {np.prod(1+qqq):.2f}$  ·  SPY {np.prod(1+spy):.2f}$")
print(f"correlacion PERFIL-QQQ {np.corrcoef(perf,qqq)[0,1]:.2f}   PERFIL-SPY {np.corrcoef(perf,spy)[0,1]:.2f}   QQQ-SPY {np.corrcoef(qqq,spy)[0,1]:.2f}")
print()
for lo,hi in [(2007,2016),(2017,2024)]:
    m=(yr>=lo)&(yr<=hi)
    print(f"  {lo}-{hi}: PERFIL {c(perf[m]):6.2f}%  ·  QQQ {c(qqq[m]):6.2f}%  ·  SPY {c(spy[m]):6.2f}%")
print()
print("Años en que PERFIL bate al QQQ:", ", ".join(str(y) for y,d in zip(yr,perf-qqq) if d>0))
print("Años en que PERFIL pierde vs QQQ:", ", ".join(str(y) for y,d in zip(yr,perf-qqq) if d<=0))
