#!/usr/bin/env python3
"""
Estudio: activos invertibles en IBKR descorrelacionados del Nasdaq-100 (QQQ)
con rentabilidad comparable.

Datos:
  data/<TICKER>.txt  -> cierres mensuales (split-adjusted, SIN dividendos), fuente IBKR
                        linea 1: start=YYYY-MM  (mes del primer cierre)
                        linea 2: cierres separados por comas
  DIV_ANCHOR         -> cierre ajustado por dividendos a 30-nov-2016 (FMP).
                        La serie ajustada de FMP esta retro-ajustada (ultimo = precio actual),
                        asi que precio_hoy / adj(2016-11-30) = retorno TOTAL del periodo.

Con eso derivamos la tasa de dividendo implicita de cada fondo y construimos
series de RETORNO TOTAL mensuales.
"""
import numpy as np, os, json
from datetime import date

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# adjClose 30-nov-2016 (FMP, ajustado por dividendos) y precio actual 03-sep-2026
DIV_ANCHOR = {  # ticker: (adjClose_2016_11_30, precio_hoy)
    "QQQ": (109.75, 717.67), "GLD": (111.75, 410.22), "GDX": (18.89, 101.49),
    "SIL": (29.96, 101.36),  "COPX": (17.47, 91.25),  "XME": (27.57, 118.38),
    "URA": (8.94, 45.70),    "GREK": (17.99, 86.46),  "ARGT": (20.61, 96.80),
    "EWP": (18.25, 62.59),   "EWI": (15.65, 62.02),   "EPOL": (13.03, 44.55),
    "EWY": (44.10, 180.56),  "EWT": (18.40, 110.13),  "EWZ": (20.01, 38.13),
    "ITA": (65.00, 225.98),
}

NOMBRES = {
    "QQQ":"Nasdaq-100 (benchmark)", "GLD":"Oro fisico", "GDX":"Mineras de oro",
    "SIL":"Mineras de plata", "COPX":"Mineras de cobre", "XME":"Metales y mineria US",
    "URA":"Uranio", "GREK":"Grecia", "ARGT":"Argentina", "EWP":"Espana",
    "EWI":"Italia", "EPOL":"Polonia", "EWY":"Corea del Sur", "EWT":"Taiwan",
    "EWZ":"Brasil", "ITA":"Defensa y aeroespacial US",
}

RF = 0.02          # tipo sin riesgo medio aproximado del periodo
BASE = (2016, 11)  # mes base comun
END  = (2026, 8)   # ultimo mes completo
YEARS = (date(2026,9,3) - date(2016,11,30)).days / 365.25

def midx(y, m):        return y*12 + (m-1)
def mlabel(i):         return f"{i//12}-{i%12+1:02d}"

def load(tk):
    """Devuelve dict {indice_mes: precio} con la serie de precios."""
    with open(os.path.join(DATA, f"{tk}.txt")) as f:
        head, body = f.read().strip().split("\n")
    y, m = map(int, head.split("=")[1].split("-"))
    vals = [float(x) for x in body.split(",") if x]
    return {midx(y, m) + k: v for k, v in enumerate(vals)}

def maxdd(curve):
    peak, dd = curve[0], 0.0
    for v in curve:
        peak = max(peak, v)
        dd = min(dd, v/peak - 1)
    return dd

def cagr(rets, years):
    return float(np.prod(1 + rets)) ** (1/years) - 1

# ---------------------------------------------------------------- construccion
i0, i1 = midx(*BASE), midx(*END)
n_ret = i1 - i0                     # 117 retornos mensuales

series = {}
for tk in DIV_ANCHOR:
    px = load(tk)
    assert i0 in px and i1 in px, tk
    # tasa de dividendo implicita: TR total / PR total sobre el periodo completo
    adj0, hoy = DIV_ANCHOR[tk]
    tr_factor = hoy / adj0                       # retorno total 2016-11-30 -> hoy
    pr_factor = px[max(px)] / px[i0]             # retorno de precio, mismo tramo
    div_yr = (tr_factor/pr_factor) ** (1/YEARS) - 1
    div_m  = (1 + div_yr) ** (1/12) - 1
    p = np.array([px[i] for i in range(i0, i1+1)])
    r = p[1:]/p[:-1] - 1 + div_m                 # retorno total mensual aprox.
    series[tk] = dict(ret=r, div=div_yr, tr_factor=tr_factor,
                      curve=np.concatenate([[1.0], np.cumprod(1+r)]))

q = series["QQQ"]["ret"]
neg = q < 0                     # meses malos del Nasdaq
pos = q > 0
tail = q < np.percentile(q, 10) # decil peor del Nasdaq

def stats(tk):
    s = series[tk]; r = s["ret"]
    vol = r.std(ddof=1) * np.sqrt(12)
    g   = cagr(r, n_ret/12)
    beta = np.cov(r, q, ddof=1)[0,1] / q.var(ddof=1)
    # carteras mixtas con QQQ (rebalanceo mensual)
    mix = {}
    for w in (0.20, 0.35, 0.50):
        rm = (1-w)*q + w*r
        mix[w] = dict(cagr=cagr(rm, n_ret/12),
                      vol=rm.std(ddof=1)*np.sqrt(12),
                      dd=maxdd(np.cumprod(1+rm)),
                      sharpe=(cagr(rm, n_ret/12)-RF)/(rm.std(ddof=1)*np.sqrt(12)))
    return dict(
        ticker=tk, nombre=NOMBRES[tk], cagr=g, vol=vol, sharpe=(g-RF)/vol,
        maxdd=maxdd(s["curve"]), corr=float(np.corrcoef(r, q)[0,1]), beta=beta,
        div=s["div"], mult=float(np.prod(1+r)),
        corr_neg=float(np.corrcoef(r[neg], q[neg])[0,1]),
        capt_down=float(r[neg].mean()/q[neg].mean()),
        capt_up=float(r[pos].mean()/q[pos].mean()),
        tail_mean=float(r[tail].mean()), tail_qqq=float(q[tail].mean()),
        mix=mix,
    )

res = {tk: stats(tk) for tk in series}
bench = res["QQQ"]

# --------------------------------------------------------------------- salida
print(f"VENTANA COMUN: {BASE[1]}/{BASE[0]} -> {END[1]}/{END[0]}  ({n_ret} meses, {n_ret/12:.2f} anos)")
print(f"Retorno TOTAL (dividendos reinvertidos). Tipo sin riesgo asumido: {RF:.1%}\n")
h = f"{'Tick':5} {'Nombre':26} {'CAGR':>7} {'Vol':>7} {'Sharpe':>7} {'MaxDD':>7} {'Corr':>6} {'Beta':>6} {'x':>6} {'Div':>6}"
print(h); print("-"*len(h))
for tk in sorted(res, key=lambda t: -res[t]["cagr"]):
    s = res[tk]
    print(f"{tk:5} {s['nombre'][:26]:26} {s['cagr']:6.1%} {s['vol']:6.1%} {s['sharpe']:7.2f} "
          f"{s['maxdd']:6.1%} {s['corr']:6.2f} {s['beta']:6.2f} {s['mult']:5.1f}x {s['div']:5.1%}")

print("\n\nCOMPORTAMIENTO EN LOS MESES MALOS DEL NASDAQ")
print(f"(meses con QQQ<0: {neg.sum()} de {n_ret}; decil peor: {tail.sum()} meses, QQQ medio {q[tail].mean():.1%})\n")
h2 = f"{'Tick':5} {'Corr en meses QQQ<0':>20} {'Captura bajista':>16} {'Captura alcista':>16} {'Media decil peor':>17}"
print(h2); print("-"*len(h2))
for tk in sorted(res, key=lambda t: res[t]["capt_down"]):
    s = res[tk]
    print(f"{tk:5} {s['corr_neg']:20.2f} {s['capt_down']:16.2f} {s['capt_up']:16.2f} {s['tail_mean']:16.1%}")

print("\n\nCARTERAS MIXTAS QQQ + ACTIVO (rebalanceo mensual)")
print(f"100% QQQ: CAGR {bench['cagr']:.1%} | Vol {bench['vol']:.1%} | Sharpe {bench['sharpe']:.2f} | MaxDD {bench['maxdd']:.1%}\n")
h3 = f"{'Tick':5} | {'80/20 CAGR':>10} {'Vol':>6} {'Sh':>5} {'MaxDD':>7} | {'65/35 CAGR':>10} {'Vol':>6} {'Sh':>5} {'MaxDD':>7} | {'50/50 CAGR':>10} {'Vol':>6} {'Sh':>5} {'MaxDD':>7}"
print(h3); print("-"*len(h3))
for tk in sorted(res, key=lambda t: -res[t]["mix"][0.35]["sharpe"]):
    if tk == "QQQ": continue
    m = res[tk]["mix"]
    print(f"{tk:5} | {m[0.20]['cagr']:9.1%} {m[0.20]['vol']:6.1%} {m[0.20]['sharpe']:5.2f} {m[0.20]['dd']:7.1%} "
          f"| {m[0.35]['cagr']:9.1%} {m[0.35]['vol']:6.1%} {m[0.35]['sharpe']:5.2f} {m[0.35]['dd']:7.1%} "
          f"| {m[0.50]['cagr']:9.1%} {m[0.50]['vol']:6.1%} {m[0.50]['sharpe']:5.2f} {m[0.50]['dd']:7.1%}")

# correlaciones por subperiodo
print("\n\nESTABILIDAD DE LA CORRELACION (vs QQQ)")
cortes = [((2016,12),(2019,12),"2017-2019"), ((2020,1),(2021,12),"2020-2021 (covid+burbuja)"),
          ((2022,1),(2022,12),"2022 (oso)"), ((2023,1),(2026,8),"2023-2026 (IA)")]
h4 = f"{'Tick':5} " + " ".join(f"{c[2][:24]:>25}" for c in cortes)
print(h4); print("-"*len(h4))
for tk in sorted(res, key=lambda t: res[t]["corr"]):
    if tk == "QQQ": continue
    row = f"{tk:5} "
    for (ya,ma),(yb,mb),_ in cortes:
        a, b = midx(ya,ma)-i0-1, midx(yb,mb)-i0
        rr, qq = series[tk]["ret"][a:b+1], q[a:b+1]
        row += f"{np.corrcoef(rr,qq)[0,1]:25.2f}"
    print(row)

json.dump({tk: {k: v for k, v in s.items() if k != "mix"} | {"mix": {str(w): m for w, m in s["mix"].items()}}
           for tk, s in res.items()}, open("resultados.json","w"), indent=1, default=float)
print("\n[resultados.json escrito]")
