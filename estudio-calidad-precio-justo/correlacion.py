# Cuanta diversificacion real aporta C4 sobre el Nasdaq.
import math, statistics as st

# yr, C4, QQQ, SPY  (retornos anuales %, 2007-2023)
D=[(2007,-2.27,-0.81,-7.51),(2008,-42.47,-28.79,-40.18),(2009,27.18,42.91,32.35),
   (2010,30.65,26.94,19.11),(2011,13.55,9.78,3.01),(2012,11.52,8.05,12.40),
   (2013,39.03,32.87,24.02),(2014,8.98,17.32,12.64),(2015,-7.29,-4.48,-8.03),
   (2016,34.39,25.84,22.06),(2017,22.79,27.11,17.35),(2018,14.76,4.01,2.12),
   (2019,29.30,30.55,19.48),(2020,56.52,48.42,24.15),(2021,-3.40,6.87,10.99),
   (2022,1.59,-19.85,-10.16),(2023,51.93,45.94,27.41)]
c4=[d[1] for d in D]; qqq=[d[2] for d in D]; spy=[d[3] for d in D]

def corr(a,b):
    n=len(a); ma=sum(a)/n; mb=sum(b)/n
    return (sum((x-ma)*(y-mb) for x,y in zip(a,b))
            / (math.sqrt(sum((x-ma)**2 for x in a))*math.sqrt(sum((y-mb)**2 for y in b))))
def beta(a,b):
    n=len(a); ma=sum(a)/n; mb=sum(b)/n
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/sum((y-mb)**2 for y in b)
def cagr(v):
    p=1.0
    for x in v: p*=(1+x/100)
    return (p**(1/len(v))-1)*100

print("=== Lo que C4 aporta frente al Nasdaq ===")
print(f"  correlacion C4 ~ QQQ : {corr(c4,qqq):+.3f}      beta {beta(c4,qqq):.2f}")
print(f"  correlacion C4 ~ SPY : {corr(c4,spy):+.3f}      beta {beta(c4,spy):.2f}")
print(f"  correlacion QQQ ~ SPY: {corr(qqq,spy):+.3f}")
print(f"\n  R^2 de C4 explicado por el Nasdaq: {corr(c4,qqq)**2*100:.0f}%")
print(f"  -> solo el {100-corr(c4,qqq)**2*100:.0f}% del movimiento de C4 es independiente del Nasdaq")

print("\n=== Rentabilidad y riesgo (17 anhos) ===")
for n,v in [("C4",c4),("Nasdaq",qqq),("S&P 500",spy)]:
    peor=min(v)
    print(f"  {n:9s} CAGR {cagr(v):6.2f}%   desv {st.stdev(v):5.1f}   peor anho {peor:6.1f}%")

print("\n=== Mezclas 50/50 anuales (rebalanceadas cada anho) ===")
for nom,a,b in [("C4 + Nasdaq",c4,qqq),("C4 + S&P",c4,spy),("Nasdaq + S&P",qqq,spy)]:
    mix=[(x+y)/2 for x,y in zip(a,b)]
    print(f"  {nom:14s} CAGR {cagr(mix):6.2f}%   desv {st.stdev(mix):5.1f}   peor {min(mix):6.1f}%")

print("\n=== Tu estructura: 4 sleeves de renta variable + oro + cash ===")
print("  (oro y cash NO estan en el panel: se muestran solo los pesos, no simulados)")
rv = 4/6
print(f"  C4 + turnarounds + situaciones especiales + Nasdaq = {rv*100:.0f}% en bolsa USA")
print(f"  oro {1/6*100:.0f}%  |  cash {1/6*100:.0f}%")
b_media = beta(c4,spy)
print(f"\n  Beta agregada aproximada frente al S&P, suponiendo beta ~1 para los otros")
print(f"  sleeves de bolsa y 0 para oro y cash:  ~{(rv*1.0):.2f}")

# ---------------------------------------------------------------------------
# Concentracion: top N por momento, equiponderado, 2007-2023.
# Sacado del panel con la misma tuberia de c4_base.sql (ver ESTUDIO-CARTERAS.md).
# CAGR geometrico; el QQQ comparable en esa misma consulta da 15,04%.
TOPN = {10: 15.19, 15: 15.57, 20: 16.77, 30: 13.58, 50: 12.22}
QQQ_COMP = 15.04
print("\n=== Concentracion: top N por momento, equiponderado ===")
print("  (error tipico de la media ~6 pp/anho: NINGUNA de estas diferencias es significativa)")
for n, v in sorted(TOPN.items()):
    print(f"  top {n:2d}   CAGR {v:6.2f}%   vs Nasdaq {v-QQQ_COMP:+5.2f} pp")
print("  desviacion anual: 34,3 con 10 nombres, 24,5 con 20")
print("  peor anho:        -49,6% con 10 nombres, -37,5% con 20")
