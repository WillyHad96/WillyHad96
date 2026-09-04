#!/usr/bin/env python3
"""
Quien se parece de verdad al Nasdaq EN RENTABILIDAD.
Mide la distancia en CAGR frente a QQQ en varias ventanas y en ventanas
moviles, para no depender de la fecha de inicio.
"""
import numpy as np
from analisis import series, load, midx, cagr, maxdd, RF, NOMBRES

VENT = [("comun 2016-11 -> 2026-08", (2016,11), (2026,8)),
        ("largo 2014-03 -> 2026-08", (2014,3),  (2026,8)),
        ("reciente 2021-09 -> 2026-08", (2021,9), (2026,8)),
        ("sin el rally 2016-11 -> 2024-12", (2016,11), (2024,12))]

def serie(tk, a, b):
    px = load(tk); ja, jb = midx(*a), midx(*b)
    if ja not in px or jb not in px: return None
    dm = (1+series[tk]["div"])**(1/12)-1
    p = np.array([px[i] for i in range(ja, jb+1)])
    return p[1:]/p[:-1]-1+dm

orden = [t for t in series if t != "QQQ"]

print("="*96)
print("1. CAGR Y DISTANCIA AL NASDAQ EN CADA VENTANA (retorno total)")
print("="*96)
tab = {}
for nom, a, b in VENT:
    yrs = (midx(*b)-midx(*a))/12
    q = cagr(serie("QQQ", a, b), yrs)
    tab[nom] = {"QQQ": q}
    for tk in orden:
        s = serie(tk, a, b)
        tab[nom][tk] = cagr(s, yrs) if s is not None else None

ETIQ = ["comun 9,8a","largo 12,4a","reciente 5a","sin rally 8,1a"]
hdr = f"{'Tick':5} " + "".join(f"{e:>17}" for e in ETIQ) + f"{'brecha media':>15}{'ventanas':>10}"
print(hdr); print("-"*len(hdr))
print(f"{'QQQ':5} " + "".join(f"{tab[n]['QQQ']:16.1%} " for n,_,_ in VENT) + f"{'—':>15}{'—':>10}")
print("-"*len(hdr))

res = []
for tk in orden:
    gaps = [tab[n][tk]-tab[n]["QQQ"] for n,_,_ in VENT if tab[n][tk] is not None]
    nv = len(gaps)
    res.append((np.mean(gaps), tk, gaps, nv))
res.sort(reverse=True)
for media, tk, gaps, nv in res:
    fila = f"{tk:5} "
    for n,_,_ in VENT:
        v = tab[n][tk]
        fila += f"{v:16.1%} " if v is not None else f"{'n/d':>16} "
    fila += f"{media*100:+13.1f}pp{nv:10d}"
    print(fila)

print("\n(brecha media = puntos porcentuales anuales frente al QQQ, promedio de las ventanas con datos)")

print("\n" + "="*96)
print("2. VENTANAS MOVILES DE 3 ANOS: cuantas veces se acerca de verdad")
print("="*96)
i0, i1 = midx(2016,11), midx(2026,8)
q3 = None
roll = {}
for tk in ["QQQ"]+orden:
    r = series[tk]["ret"]; n = len(r); W = 36
    v = np.array([np.prod(1+r[i:i+W])**(1/3)-1 for i in range(n-W+1)])
    roll[tk] = v
q3 = roll["QQQ"]; N = len(q3)
print(f"{N} ventanas moviles de 36 meses (nov-2016 -> ago-2026)\n")
h2 = f"{'Tick':5} {'gana al QQQ':>13} {'a menos de 3pp':>16} {'a menos de 5pp':>16} {'peor por >10pp':>16} {'brecha mediana':>16}"
print(h2); print("-"*len(h2))
r2 = []
for tk in orden:
    d = roll[tk]-q3
    r2.append((( np.abs(d)<0.05).mean(), tk, (d>0).mean(), (np.abs(d)<0.03).mean(),
               (np.abs(d)<0.05).mean(), (d<-0.10).mean(), np.median(d)))
r2.sort(reverse=True)
for _, tk, gana, p3, p5, mal, med in r2:
    print(f"{tk:5} {gana:12.0%} {p3:15.0%} {p5:15.0%} {mal:15.0%} {med:15.1%}")

print("\n" + "="*96)
print("3. LOS QUE MAS SE PARECEN, CRUZANDO RENTABILIDAD Y CORRELACION")
print("="*96)
print(f"{'Tick':5} {'Nombre':24} {'brecha media':>13} {'Corr':>6} {'Capt.bajista':>13} {'Veredicto'}")
print("-"*96)
for media, tk, gaps, nv in res[:8]:
    s = series[tk]
    from analisis import res as R
    c, cb = R[tk]["corr"], R[tk]["capt_down"]
    if c >= 0.6:   ver = "es Nasdaq con otro nombre"
    elif c >= 0.4: ver = "rentable, pero acompana en las caidas"
    elif nv < 4:   ver = "poco historico para juzgarlo"
    else:          ver = "rentable Y de verdad independiente"
    print(f"{tk:5} {NOMBRES[tk][:24]:24} {media*100:12.1f}pp {c:6.2f} {cb:13.2f} {ver}")
