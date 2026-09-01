# Test de permutacion estratificado: dentro de cada celda (anho, sector),
# permuta la etiqueta "desconocido" y recalcula la diferencia media de excesos.
import random, collections, statistics

celdas = collections.defaultdict(list)
for r in open('celdas.txt').read().replace('\n','').split(';'):
    if not r.strip(): continue
    yr, sec, d, x = r.split('~')
    celdas[(yr, sec)].append((int(d), float(x)))

celdas = {k: v for k, v in celdas.items()
          if any(d for d, _ in v) and any(not d for d, _ in v)}

def estad(asig):
    """media, sobre celdas, de (media desconocidos - media clasificados)"""
    difs = []
    for k, vals in celdas.items():
        et = asig[k]
        a = [x for e, (_, x) in zip(et, vals) if e]
        b = [x for e, (_, x) in zip(et, vals) if not e]
        difs.append(sum(a)/len(a) - sum(b)/len(b))
    return sum(difs)/len(difs), difs

obs_asig = {k: [d for d, _ in v] for k, v in celdas.items()}
obs, difs_obs = estad(obs_asig)

n = sum(len(v) for v in celdas.values())
nd = sum(sum(d for d, _ in v) for v in celdas.values())
print(f"celdas={len(celdas)}  n={n}  desconocidos={nd}  clasificados={n-nd}")
print(f"diferencia observada (media de celdas) = {100*obs:+.2f} pp")
print(f"celdas donde desconocido rinde peor: {sum(1 for d in difs_obs if d<0)}/{len(difs_obs)}")

rng = random.Random(13)
IT = 20000
peor = 0
for _ in range(IT):
    asig = {}
    for k, v in celdas.items():
        et = [d for d, _ in v]
        rng.shuffle(et)
        asig[k] = et
    s, _ = estad(asig)
    if abs(s) >= abs(obs): peor += 1
print(f"p (permutacion bilateral, {IT} it, semilla 13) = {peor/IT:.4f}")

# version ponderada por tamanho de celda
def estad_pond(asig):
    num = den = 0.0
    for k, vals in celdas.items():
        et = asig[k]
        a = [x for e, (_, x) in zip(et, vals) if e]
        b = [x for e, (_, x) in zip(et, vals) if not e]
        w = len(vals)
        num += w*(sum(a)/len(a) - sum(b)/len(b)); den += w
    return num/den
obsp = estad_pond(obs_asig)
rng = random.Random(13)
peor = 0
for _ in range(IT):
    asig = {}
    for k, v in celdas.items():
        et = [d for d, _ in v]; rng.shuffle(et); asig[k] = et
    if abs(estad_pond(asig)) >= abs(obsp): peor += 1
print(f"diferencia ponderada por celda = {100*obsp:+.2f} pp   p = {peor/IT:.4f}")
