import numpy as np
# yr, cal_all, cal_t12, cal_t2, med_t1, spy   (%)
D = [
(2007,  0.00, -1.53, -8.59,  -4.05, -5.72),
(2008,-37.70,-39.53,-32.19, -39.29,-39.14),
(2009, 55.99, 63.91, 36.59, 147.05, 49.05),
(2010, 30.79, 29.70, 32.36,  43.68, 21.12),
(2011, 10.47, 10.62,  8.42,  -1.02,  2.77),
(2012, 18.50, 16.06, 14.42,   9.98, 12.08),
(2013, 33.17, 33.57, 31.19,  26.54, 21.13),
(2014,  6.47,  6.11, -2.77,  -0.27, 12.04),
(2015,-12.73,-14.64,-11.18, -16.41, -5.80),
(2016, 38.80, 43.98, 49.42,  58.87, 25.33),
(2017, 14.26, 14.14, 18.22,   9.35, 15.84),
(2018, -1.31, -3.68, -1.02,  -0.04,  1.55),
(2019,  6.86,  4.30, -0.38, -12.64, 14.99),
(2020, 33.39, 35.38, 17.48,  69.95, 31.49),
(2021, 11.06,  8.50,  6.51,  30.67, 12.60),
(2022,  3.50,  9.39,  5.86,  11.73, -7.90),
(2023, 19.75, 17.35,  1.02,   7.20, 21.86),
(2024, 12.57, 12.62, 24.23,  14.53, 18.37),
]
A = np.array(D, float)
yrs = A[:,0].astype(int); spy = A[:,5]/100
names = ["CALIDAD (todas)","CALIDAD T1+T2","CALIDAD T2 (precio justo)","MEDIOCRE T1 (barato)","SPY"]
cols  = [1,2,3,4,5]
RF = 0.02

def stats(r, bm, label, costes=0.006):
    r = r - costes                      # 0.30%/lado, rotacion anual completa
    n = len(r)
    cagr = np.prod(1+r)**(1/n)-1
    arit = r.mean(); vol = r.std(ddof=1)
    sharpe_c = (cagr-RF)/vol
    sharpe_a = (arit-RF)/vol
    beta = np.cov(r,bm,ddof=1)[0,1]/np.var(bm,ddof=1)
    alpha = (arit-RF) - beta*(bm.mean()-RF)
    return dict(label=label,n=n,cagr=100*cagr,arit=100*arit,vol=100*vol,
                sharpe_cagr=sharpe_c,sharpe_arit=sharpe_a,beta=beta,alpha=100*alpha,
                peor=100*r.min(),peor_yr=int(yrs[r.argmin()]),
                bate=100*np.mean(r>bm))

print(f"{'cartera':<28}{'CAGR':>7}{'media':>7}{'vol':>7}{'Sh(g)':>7}{'Sh(a)':>7}{'beta':>6}{'alfa':>7}{'peor':>8}{'año':>6}{'%>SPY':>7}")
print("-"*103)
rows=[]
for c,nm in zip(cols,names):
    r = A[:,c]/100
    s = stats(r, spy, nm, costes=0.0 if nm=="SPY" else 0.006)
    rows.append(s)
    print(f"{s['label']:<28}{s['cagr']:>7.2f}{s['arit']:>7.2f}{s['vol']:>7.2f}{s['sharpe_cagr']:>7.2f}{s['sharpe_arit']:>7.2f}{s['beta']:>6.2f}{s['alpha']:>7.2f}{s['peor']:>8.1f}{s['peor_yr']:>6}{s['bate']:>7.1f}")

print("\n--- Sub-periodos (CALIDAD todas vs MEDIOCRE T1) ---")
for lo,hi in [(2007,2016),(2017,2024)]:
    m = (yrs>=lo)&(yrs<=hi)
    for c,nm in [(1,"CALIDAD"),(4,"MEDIOCRE T1"),(5,"SPY")]:
        r=A[m,c]/100 - (0.0 if c==5 else 0.006)
        cg=np.prod(1+r)**(1/m.sum())-1
        print(f"  {lo}-{hi} {nm:<12} CAGR {100*cg:6.2f}%  vol {100*r.std(ddof=1):5.1f}%  peor {100*r.min():6.1f}%")
