# C4 partido en dos: la mitad de sectores ciclicos y la mitad del resto.
# Todo en %, ventanas feb-feb 2007-2023, ponderacion rank^2 dentro de cada mitad.
import math, statistics as st
D=[ # yr, c4_cic, c4_nocic, qqq, spy, peso_cic, sd_margen_pasa, sd_margen_falla
(2007,  1.81,-13.25, -0.81, -7.51,73,1.37,4.17),(2008,-49.88,-23.44,-28.79,-40.18,72,1.24,3.85),
(2009, 28.73, 25.89, 42.91, 32.35,45,1.42,4.50),(2010, 26.96, 33.42, 26.94, 19.11,43,1.53,4.75),
(2011, 22.45, -6.86,  9.78,  3.01,70,1.56,4.53),(2012,  3.81, 18.25,  8.05, 12.40,47,1.28,4.44),
(2013, 38.39, 39.97, 32.87, 24.02,59,1.28,5.16),(2014,  3.69, 10.48, 17.32, 12.64,22,1.31,5.68),
(2015, -7.09, -7.44, -4.48, -8.03,44,1.17,3.92),(2016, 35.03, 33.89, 25.84, 22.06,43,1.26,4.14),
(2017, 19.34, 25.23, 27.11, 17.35,41,1.26,4.66),(2018, -9.74, 35.95,  4.01,  2.12,46,1.26,4.30),
(2019, 31.71, 28.30, 30.55, 19.48,29,1.30,4.21),(2020, 40.30, 66.95, 48.42, 24.15,39,1.25,4.74),
(2021, 14.59,-16.48,  6.87, 10.99,42,1.82,5.91),(2022, 15.63, -9.44,-19.85,-10.16,44,1.81,6.36),
(2023, 44.05, 57.11, 45.94, 27.41,40,1.78,5.59)]
cic=[d[1] for d in D]; noc=[d[2] for d in D]; qqq=[d[3] for d in D]; spy=[d[4] for d in D]
def corr(a,b):
    n=len(a); ma=sum(a)/n; mb=sum(b)/n
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/(math.sqrt(sum((x-ma)**2 for x in a))*math.sqrt(sum((y-mb)**2 for y in b)))
def beta(a,b):
    n=len(a); ma=sum(a)/n; mb=sum(b)/n
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/sum((y-mb)**2 for y in b)
def cagr(v):
    p=1.0
    for x in v: p*=(1+x/100)
    return (p**(1/len(v))-1)*100

print("=== Las dos mitades de C4 frente a los indices ===")
print(f"  {'':24s} {'corr QQQ':>9s} {'beta QQQ':>9s} {'corr SPY':>9s} {'beta SPY':>9s} {'CAGR':>7s} {'desv':>6s}")
for nom,v in [("C4 sectores ciclicos",cic),("C4 resto de sectores",noc)]:
    print(f"  {nom:24s} {corr(v,qqq):+9.3f} {beta(v,qqq):9.2f} {corr(v,spy):+9.3f} {beta(v,spy):9.2f} {cagr(v):7.2f} {st.stdev(v):6.1f}")
print(f"\n  correlacion entre las dos mitades de C4: {corr(cic,noc):+.3f}")
print(f"  R2 de la mitad ciclica explicado por el Nasdaq: {corr(cic,qqq)**2*100:.0f}%")
print(f"  R2 de la otra mitad explicado por el Nasdaq:    {corr(noc,qqq)**2*100:.0f}%")

print("\n=== Anhos en que las dos mitades divergen mas de 20 pp ===")
for d in D:
    if abs(d[1]-d[2])>20:
        print(f"  {d[0]}  ciclicos {d[1]:+6.1f}   resto {d[2]:+6.1f}   Nasdaq {d[3]:+6.1f}   S&P {d[4]:+6.1f}")

print("\n=== Lo que hace el filtro DENTRO de los sectores ciclicos ===")
sp=[d[6] for d in D]; sf=[d[7] for d in D]
print(f"  sd(margen bruto) 8T, media de los que PASAN el filtro: {sum(sp)/len(sp):.2f} pp")
print(f"  sd(margen bruto) 8T, media de los que FALLAN:          {sum(sf)/len(sf):.2f} pp")
print(f"  ratio: los que fallan tienen {sum(sf)/sum(sp):.1f}x mas volatilidad de margen")
print(f"\n  peso medio de sectores ciclicos en C4: {sum(d[5] for d in D)/len(D):.0f}%  (rango {min(d[5] for d in D)}-{max(d[5] for d in D)}%)")
