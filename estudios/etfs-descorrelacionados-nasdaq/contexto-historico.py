#!/usr/bin/env python3
"""
Contexto historico: donde cae la decada actual del Nasdaq en sus propios 55 anos.
Datos: cierres de fin de ano del Nasdaq Composite (^IXIC), FMP. Solo precio,
sin dividendos (el Composite rinde ~0,7-1% de dividendo).
"""
import numpy as np

IXIC = {
1971:114.12,1972:133.73,1973:92.19,1974:59.82,1975:77.62,1976:97.88,1977:105.05,
1978:117.98,1979:151.14,1980:202.34,1981:195.84,1982:232.41,1983:278.60,1984:247.35,
1985:324.90,1986:348.80,1987:330.50,1988:381.40,1989:454.80,1990:373.80,1991:586.30,
1992:677.00,1993:776.80,1994:752.00,1995:1052.10,1996:1291.03,1997:1570.35,
1998:2192.48,1999:4069.31,2000:2470.52,2001:1950.40,2002:1335.51,2003:2003.37,
2004:2175.44,2005:2205.32,2006:2415.29,2007:2652.28,2008:1577.03,2009:2269.15,
2010:2652.87,2011:2605.15,2012:3019.51,2013:4176.59,2014:4736.05,2015:5007.41,
2016:5383.12,2017:6903.39,2018:6635.28,2019:8972.60,2020:12888.28,2021:15644.97,
2022:10466.48,2023:15011.35,2024:19310.79,2025:23241.99,
}
HOY = 26584.06        # ^IXIC 3-sep-2026
FRAC = 0.674          # fraccion de 2026 transcurrida (3 sep)

anos = sorted(IXIC)

print("="*74)
print("1. RENTABILIDAD POR ANO NATURAL (precio, sin dividendos)")
print("="*74)
rets = {}
for a in anos[1:]:
    rets[a] = IXIC[a]/IXIC[a-1] - 1
rets[2026] = HOY/IXIC[2025] - 1
r = np.array(list(rets.values()))
neg = [(a,v) for a,v in rets.items() if v < 0]
print(f"Anos completos analizados: {len(rets)-1} (1972-2025) + 2026 parcial")
print(f"Media aritmetica: {r.mean():.1%} | Mediana: {np.median(r):.1%} | Desv.: {r.std(ddof=1):.1%}")
print(f"Anos negativos: {len(neg)} de {len(rets)} ({len(neg)/len(rets):.0%})")
print("\nLos 6 peores:")
for a,v in sorted(rets.items(), key=lambda x:x[1])[:6]: print(f"   {a}  {v:7.1%}")
print("Los 6 mejores:")
for a,v in sorted(rets.items(), key=lambda x:-x[1])[:6]: print(f"   {a}  {v:7.1%}")

print("\nUltimos 11 anos:")
for a in range(2016, 2027):
    marca = "  <- parcial (hasta 3-sep)" if a == 2026 else ""
    print(f"   {a}  {rets[a]:7.1%}{marca}")

print("\n" + "="*74)
print("2. RENTABILIDAD ANUALIZADA A 10 ANOS, TODAS LAS VENTANAS (1981-2026)")
print("="*74)
roll = {}
for a in range(1981, 2026):
    roll[a] = (IXIC[a]/IXIC[a-10])**(1/10) - 1
# ventana actual: 30-dic-2016 -> 3-sep-2026
yrs_act = 2026 + FRAC - (2016 + 1.0)
act = (HOY/IXIC[2016])**(1/yrs_act) - 1
v = np.array(list(roll.values()))
print(f"Ventanas de 10 anos naturales: {len(roll)}")
print(f"Media: {v.mean():.1%} | Mediana: {np.median(v):.1%} | Min: {v.min():.1%} | Max: {v.max():.1%}")
print(f"\nVENTANA ACTUAL (dic-2016 -> 3-sep-2026, {yrs_act:.2f} anos): {act:.1%} anual")
pct = (v < act).mean()
print(f"Percentil frente a las {len(roll)} ventanas historicas: {pct:.0%}")
print(f"Ventanas historicas que la superan: {(v>=act).sum()}")

print("\nLas 8 mejores decadas del Nasdaq:")
for a,x in sorted(roll.items(), key=lambda t:-t[1])[:8]:
    print(f"   {a-10}-{a}  {x:6.1%} anual   ({IXIC[a]/IXIC[a-10]:5.1f}x)")
print("\nLas 5 peores:")
for a,x in sorted(roll.items(), key=lambda t:t[1])[:5]:
    print(f"   {a-10}-{a}  {x:6.1%} anual   ({IXIC[a]/IXIC[a-10]:5.1f}x)")

print("\nDecadas terminadas en cada ano desde 2010:")
for a in range(2010, 2026):
    print(f"   {a-10}-{a}  {roll[a]:6.1%} anual")

print("\n" + "="*74)
print("3. CONSTANCIA: RACHAS Y CAIDAS (cierres anuales)")
print("="*74)
# racha positiva mas larga
mejor=cur=0; ini=None; best_ini=None
for a in sorted(rets):
    if rets[a] > 0:
        if cur == 0: ini = a
        cur += 1
        if cur > mejor: mejor, best_ini = cur, ini
    else: cur = 0
print(f"Racha positiva mas larga: {mejor} anos ({best_ini}-{best_ini+mejor-1})")
# racha actual
cur=0
for a in sorted(rets, reverse=True):
    if rets[a] > 0: cur += 1
    else: break
print(f"Racha positiva actual: {cur} anos ({2026-cur+1}-2026, 2026 en curso)")
rachas=[]; ini=None; n=0
for a in sorted(rets):
    if rets[a]>0:
        if n==0: ini=a
        n+=1
    else:
        if n>=4: rachas.append((ini,a-1,n))
        n=0
if n>=4: rachas.append((ini,2026,n))
print("Todas las rachas de 4+ anos positivos:")
for i,f,k in rachas: print(f"   {i}-{f}  ({k} anos)")

# drawdowns sobre cierres anuales
serie = [(a, IXIC[a]) for a in anos] + [(2026, HOY)]
peak = serie[0][1]; peak_a = serie[0][0]; dd_min = 0; dd_a = None; dd_peak = None
for a, v_ in serie:
    if v_ > peak: peak, peak_a = v_, a
    d = v_/peak - 1
    if d < dd_min: dd_min, dd_a, dd_peak = d, a, peak_a
print(f"\nPeor caida en cierres anuales: {dd_min:.1%} ({dd_peak} -> {dd_a})")
# recuperacion del pico de 1999
rec = next(a for a in anos if a > 1999 and IXIC[a] > IXIC[1999])
print(f"El cierre de 1999 ({IXIC[1999]:.0f}) no se supero hasta {rec} ({IXIC[rec]:.0f}): {rec-1999} anos")
# caidas anuales encadenadas
print(f"Caida acumulada 1999->2002: {IXIC[2002]/IXIC[1999]-1:.1%}")
print(f"Caida acumulada 2007->2008: {IXIC[2008]/IXIC[2007]-1:.1%}")
print(f"Caida del ano 2022:         {rets[2022]:.1%}")

print("\n" + "="*74)
print("4. COMPARACION CON EL S&P 500 (precio)")
print("="*74)
GSPC = {1989:353.40, 1999:1469.25, 2016:2238.83}
SP_HOY = 7747.71
print(f"Misma decada (dic-2016 -> hoy):")
print(f"   Nasdaq Composite {act:.1%} anual   ({HOY/IXIC[2016]:.2f}x)")
sp = (SP_HOY/GSPC[2016])**(1/yrs_act)-1
print(f"   S&P 500          {sp:.1%} anual   ({SP_HOY/GSPC[2016]:.2f}x)")
print(f"   Diferencial      {(act-sp)*100:+.1f} pp anuales")
print(f"\nDecada de los 90 (1989-1999):")
print(f"   Nasdaq Composite {(IXIC[1999]/IXIC[1989])**.1-1:.1%} anual   ({IXIC[1999]/IXIC[1989]:.2f}x)")
print(f"   S&P 500          {(GSPC[1999]/GSPC[1989])**.1-1:.1%} anual   ({GSPC[1999]/GSPC[1989]:.2f}x)")
print(f"   Diferencial      {((IXIC[1999]/IXIC[1989])**.1-(GSPC[1999]/GSPC[1989])**.1)*100:+.1f} pp anuales")
