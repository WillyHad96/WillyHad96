#!/usr/bin/env python3
"""Prueba de robustez: las mismas carteras en 3 ventanas distintas."""
import numpy as np
from analisis import series, load, midx, cagr, maxdd, RF, DIV_ANCHOR

VENTANAS = [("2014-03 -> 2026-08 (12,4a)", (2014,3), (2026,8)),
            ("2016-11 -> 2026-08 (9,8a)",  (2016,11),(2026,8)),
            ("2021-09 -> 2026-08 (5,0a)",  (2021,9), (2026,8)),
            ("2014-03 -> 2024-12 (excl. 2025-26)", (2014,3), (2024,12))]

def serie(tk, a, b):
    px = load(tk); ja, jb = midx(*a), midx(*b)
    if ja not in px: return None
    dm = (1+series[tk]["div"])**(1/12)-1
    p = np.array([px[i] for i in range(ja, jb+1)])
    return p[1:]/p[:-1]-1+dm

CARTERAS = [("100% Nasdaq",                   {"QQQ":1.0}),
            ("85 Nasdaq / 15 oro",            {"QQQ":.85,"GLD":.15}),
            ("75 Nasdaq / 25 oro",            {"QQQ":.75,"GLD":.25}),
            ("80 Nasdaq / 20 mineras oro",    {"QQQ":.80,"GDX":.20}),
            ("70 / 20 oro / 10 mineras",      {"QQQ":.70,"GLD":.20,"GDX":.10}),
            ("60 / 25 oro / 15 mineras",      {"QQQ":.60,"GLD":.25,"GDX":.15}),
            ("50 Nasdaq / 50 oro",            {"QQQ":.50,"GLD":.50}),
            ("70 / 15 oro / 10 min / 5 defensa", {"QQQ":.70,"GLD":.15,"GDX":.10,"ITA":.05})]

for nom, a, b in VENTANAS:
    yrs = (midx(*b)-midx(*a))/12
    print(f"\n=== {nom} ===")
    print(f"{'Cartera':36} {'CAGR':>7} {'Vol':>7} {'Sharpe':>7} {'MaxDD':>8}")
    print("-"*70)
    for cn, w in CARTERAS:
        ss = {t: serie(t, a, b) for t in w}
        if any(v is None for v in ss.values()): print(f"{cn:36}   (sin historico)"); continue
        r = sum(wi*ss[t] for t, wi in w.items())
        v = r.std(ddof=1)*np.sqrt(12); g = cagr(r, yrs)
        print(f"{cn:36} {g:6.1%} {v:6.1%} {(g-RF)/v:7.2f} {maxdd(np.cumprod(1+r)):7.1%}")

# cuanto pesa 2025 en el resultado de cada activo
print("\n\nPESO DEL ANO 2025 EN EL RESULTADO TOTAL (ventana 2016-11 -> 2026-08)")
print(f"{'Tick':5} {'CAGR con 2025':>14} {'CAGR sin 2025':>14} {'Diferencia':>12}")
print("-"*48)
i0 = midx(2016,11)
for tk in sorted(series, key=lambda t: -series[t]["ret"].sum()):
    r = series[tk]["ret"]; n = len(r)
    a25, b25 = midx(2025,1)-i0-1, midx(2025,12)-i0
    sin = np.concatenate([r[:a25], r[b25+1:]])
    c1, c2 = cagr(r, n/12), cagr(sin, len(sin)/12)
    print(f"{tk:5} {c1:13.1%} {c2:13.1%} {(c1-c2)*100:10.1f}pp")
