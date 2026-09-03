#!/usr/bin/env python3
"""Anos naturales, ventana larga y optimizacion de carteras QQQ + diversificadores."""
import numpy as np, itertools
from analisis import series, res, q, i0, i1, midx, mlabel, cagr, maxdd, RF, load, DIV_ANCHOR, YEARS

n_ret = i1 - i0

# ---------------------------------------------------- retornos por ano natural
print("RETORNOS POR ANO NATURAL (retorno total, %)  -- 2026 hasta agosto\n")
anos = list(range(2017, 2027))
orden = ["QQQ","GLD","GDX","SIL","COPX","XME","URA","GREK","ARGT","EWP","EWI","EPOL","EWY","EWT","EWZ","ITA"]
print(f"{'Tick':5}" + "".join(f"{a:>8}" for a in anos))
print("-"*(5+8*len(anos)))
for tk in orden:
    r = series[tk]["ret"]; row = f"{tk:5}"
    for a in anos:
        ia, ib = midx(a,1)-i0-1, min(midx(a,12)-i0, n_ret-1)
        row += f"{(np.prod(1+r[ia:ib+1])-1)*100:7.0f} "
    print(row)

# ------------------------------------------------- ventana larga (2014-03 -> )
print("\n\nVENTANA LARGA 2014-03 -> 2026-08 (12,4 anos) -- solo activos con historico completo")
j0, j1 = midx(2014,3), midx(2026,8)
largo = {}
for tk in ["QQQ","GLD","GDX","XME","GREK","ARGT","EWP","EPOL","EWY","EWZ","ITA"]:
    px = load(tk)
    if j0 not in px: continue
    div_m = (1+series[tk]["div"])**(1/12)-1
    p = np.array([px[i] for i in range(j0, j1+1)])
    largo[tk] = p[1:]/p[:-1]-1+div_m
ql = largo["QQQ"]; yrs = (j1-j0)/12
print(f"\n{'Tick':5} {'CAGR':>7} {'Vol':>7} {'Sharpe':>7} {'MaxDD':>8} {'Corr':>6}")
print("-"*46)
for tk in sorted(largo, key=lambda t: -cagr(largo[t], yrs)):
    r = largo[tk]; v = r.std(ddof=1)*np.sqrt(12); g = cagr(r, yrs)
    print(f"{tk:5} {g:6.1%} {v:6.1%} {(g-RF)/v:7.2f} {maxdd(np.cumprod(1+r)):7.1%} {np.corrcoef(r,ql)[0,1]:6.2f}")

# ----------------------------------------------- optimizacion cartera 3 activos
print("\n\nCARTERAS QQQ + DIVERSIFICADORES (rebalanceo mensual, ventana comun 2016-11 -> 2026-08)\n")
def perf(w, tickers):
    r = sum(wi*series[t]["ret"] for wi, t in zip(w, tickers))
    v = r.std(ddof=1)*np.sqrt(12); g = cagr(r, n_ret/12)
    return g, v, (g-RF)/v, maxdd(np.cumprod(1+r))

combos = [
    (("QQQ",), (1.0,), "100% Nasdaq (referencia)"),
    (("QQQ","GLD"), (.70,.30), "70 Nasdaq / 30 oro"),
    (("QQQ","GDX"), (.80,.20), "80 Nasdaq / 20 mineras oro"),
    (("QQQ","GLD","GDX"), (.70,.20,.10), "70 / 20 oro / 10 mineras"),
    (("QQQ","GLD","GDX"), (.60,.25,.15), "60 / 25 oro / 15 mineras"),
    (("QQQ","GLD","GDX","GREK"), (.55,.20,.10,.15), "55 / 20 oro / 10 mineras / 15 Grecia"),
    (("QQQ","GLD","GDX","GREK","EWP"), (.50,.20,.10,.10,.10), "50 / 20 oro / 10 min / 10 GR / 10 ES"),
    (("QQQ","GLD","GDX","COPX"), (.55,.20,.15,.10), "55 / 20 oro / 15 min oro / 10 cobre"),
    (("QQQ","GLD","ITA"), (.60,.25,.15), "60 / 25 oro / 15 defensa"),
]
print(f"{'Cartera':42} {'CAGR':>7} {'Vol':>7} {'Sharpe':>7} {'MaxDD':>8}")
print("-"*76)
for tks, w, nom in combos:
    g, v, s, d = perf(w, tks)
    print(f"{nom:42} {g:6.1%} {v:6.1%} {s:7.2f} {d:7.1%}")

# ---- frontera: mejor Sharpe con QQQ + hasta 3 diversificadores en pasos de 5%
print("\n\nBUSQUEDA: mejor Sharpe posible con QQQ + 2 diversificadores (pasos de 5%)\n")
cands = [t for t in series if t != "QQQ"]
best = []
for a, b in itertools.combinations(cands, 2):
    for wa in np.arange(0, .55, .05):
        for wb in np.arange(0, .55-wa+1e-9, .05):
            wq = 1-wa-wb
            if wq < .40: continue
            g, v, s, d = perf((wq, wa, wb), ("QQQ", a, b))
            best.append((s, g, v, d, f"{wq:.0%} QQQ / {wa:.0%} {a} / {wb:.0%} {b}"))
best.sort(reverse=True)
print(f"{'Cartera':44} {'CAGR':>7} {'Vol':>7} {'Sharpe':>7} {'MaxDD':>8}")
print("-"*78)
for s, g, v, d, nom in best[:12]:
    print(f"{nom:44} {g:6.1%} {v:6.1%} {s:7.2f} {d:7.1%}")

print("\n\nRestriccion: misma busqueda exigiendo CAGR >= 18% (no renunciar a rentabilidad)\n")
print(f"{'Cartera':44} {'CAGR':>7} {'Vol':>7} {'Sharpe':>7} {'MaxDD':>8}")
print("-"*78)
for s, g, v, d, nom in [x for x in best if x[1] >= .18][:10]:
    print(f"{nom:44} {g:6.1%} {v:6.1%} {s:7.2f} {d:7.1%}")
