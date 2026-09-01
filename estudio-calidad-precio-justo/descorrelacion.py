# Criterio: DESCORRELACION + RENTABILIDAD. La volatilidad no penaliza.
# Clave: la correlacion baja con pocos nombres es en gran parte ruido idiosincratico,
# no exposicion diferenciada. Se compara cada variante con carteras ALEATORIAS del mismo
# tamanho y del mismo pool (300 simulaciones por tamanho, orden determinista via md5).
import math, statistics as st

# --- benchmarks aleatorios: corr media con el Nasdaq de una cartera aleatoria de N nombres
ALEA = {
 'todo': {3:0.654, 5:0.735, 12:0.825, 25:0.866, 40:0.883},
 'def':  {3:0.563, 5:0.642, 12:0.768, 25:0.828, 40:0.833},
 'cic':  {3:0.697, 5:0.767, 12:0.842, 15:0.854, 25:0.878},
}
P05 = {'todo':{3:0.446,5:0.561,12:0.724,25:0.802,40:0.840},
       'def': {3:0.337,5:0.414,12:0.643,25:0.792,40:0.833},
       'cic': {3:0.506,5:0.634,12:0.763,15:0.794,25:0.837}}
def interp(tab, n):
    ks = sorted(tab)
    if n <= ks[0]: return tab[ks[0]]
    if n >= ks[-1]: return tab[ks[-1]]
    for a, b in zip(ks, ks[1:]):
        if a <= n <= b:
            t = (math.log(n)-math.log(a))/(math.log(b)-math.log(a))
            return tab[a] + t*(tab[b]-tab[a])

def load(fn, idx):
    rows=[l.split(';') for l in open(fn).read().strip().split('\n')]
    q=[float(r[1]) for r in rows]
    v=[float(r[2+idx].split('|')[0]) for r in rows]
    n=sum(int(r[2+idx].split('|')[1]) for r in rows)/len(rows)
    return v, n, q
def corr(a,b):
    m=len(a); ma=sum(a)/m; mb=sum(b)/m
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/(math.sqrt(sum((x-ma)**2 for x in a))*math.sqrt(sum((y-mb)**2 for y in b)))
def beta(a,b):
    m=len(a); ma=sum(a)/m; mb=sum(b)/m
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/sum((y-mb)**2 for y in b)
def cagr(v):
    p=1.0
    for x in v: p*=(1+x/100)
    return (p**(1/len(v))-1)*100

V=[]  # (etiqueta, serie, n/anho, pool)
NOMB={1:("C4 completo",'todo'),2:("C4 solo ciclicos",'cic'),3:("C4 solo defensivos",'def'),
      4:("Ciclicos sin estabilidad",'cic'),5:("Ciclicos sin momento",'cic'),
      6:("Ciclicos momento invertido",'cic'),7:("Ciclicos + value (P/S bajo)",'cic'),
      8:("Ciclicos sin estab + value",'cic'),9:("Solo Energia+Materiales",'cic')}
for k,(nom,pool) in NOMB.items():
    v,n,q = load('rejilla_beta.txt', k); V.append((nom,v,n,pool))
NOMD={1:("Defensivos + momento",'def'),2:("Defensivos C4 equipond.",'def'),3:("Def regla40+mcap equipond.",'def'),
      4:("Def solo mcap",'def'),5:("Def+Energia+Materiales C4",'todo'),6:("Def+Ener+Mat regla40",'todo'),
      8:("Def estabilidad+mcap",'def')}
for k,(nom,pool) in NOMD.items():
    v,n,q = load('rejilla_def.txt', k); V.append((nom,v,n,pool))
_,_,qqq = load('rejilla_beta.txt',1)
cq=cagr(qqq); mq=sum(qqq)/len(qqq)

print("="*118)
print("DESCORRELACION REAL = correlacion observada - la que da el AZAR con ese numero de nombres")
print("="*118)
print(f"{'variante':30s} {'n':>4} {'CAGR':>7} {'corr':>6} {'azar':>6} {'p05':>6} {'REAL':>7} {'mezcla':>7} {'alfa':>6}")
res=[]
for nom,v,n,pool in V:
    c=corr(v,qqq); esp=interp(ALEA[pool],n); p5=interp(P05[pool],n)
    real=c-esp
    mix=[(x+y)/2 for x,y in zip(v,qqq)]
    cm=cagr(mix); am=sum(mix)/len(mix)-beta(mix,qqq)*mq
    flag=" *" if c < p5 else ""
    res.append((cm,nom,n,cagr(v),c,esp,p5,real,cm,am,flag))
    print(f"{nom:30s} {n:4.0f} {cagr(v):7.2f} {c:6.2f} {esp:6.2f} {p5:6.2f} {real:+7.2f} {cm:7.2f} {am:+6.1f}{flag}")
print(f"\n  (*) correlacion por debajo del percentil 5 de las carteras aleatorias del mismo pool y tamanho")
print(f"  Nasdaq solo: CAGR {cq:.2f}. 'mezcla' = 50/50 con Nasdaq rebalanceado cada anho.")

print("\n" + "="*118)
print("RANKING POR EL CRITERIO REAL: CAGR de la cartera combinada (descorrelacion Y rentabilidad juntas)")
print("="*118)
print(f"{'variante':30s} {'CAGR mezcla':>12} {'vs Nasdaq':>10} {'alfa mezcla':>12} {'descorr real':>13}")
for cm,nom,n,cv,c,esp,p5,real,_,am,flag in sorted(res,reverse=True):
    print(f"{nom:30s} {cm:12.2f} {cm-cq:+10.2f} {am:+12.1f} {real:+13.2f}{flag}")

print("\n" + "="*118)
print("LA TRAMPA: la correlacion cae sola al reducir nombres, sin ganar nada")
print("="*118)
print(f"  {'nombres':>8} {'corr aleatoria (universo entero)':>34}")
for n in [3,5,12,25,40]:
    print(f"  {n:>8} {ALEA['todo'][n]:>34.3f}")
print("  Una cartera de 3 nombres AL AZAR ya da 0,65 de correlacion. Eso no es descorrelacion:")
print("  es varianza idiosincratica, que anhade riesgo sin anhadir rentabilidad esperada.")

print("\n" + "="*118)
print("AVISO sobre los (*): para las variantes con 30+ nombres el pool defensivo (~40) se agota")
print("y el contrafactual aleatorio degenera. Los unicos (*) validos son los de pocos nombres:")
print("  Solo Energia+Materiales (3) y Defensivos + momento (12).")

print("\n" + "="*118)
print("TEST: 'Ciclicos + value' gana la mezcla. Pero es beta, no descorrelacion?")
print("="*118)
v7,_,_ = load('rejilla_beta.txt', 7)
mix7=[(x+y)/2 for x,y in zip(v7,qqq)]
b7=beta(mix7,qqq)
print(f"  Mezcla 50/50 Nasdaq + ciclicos-value:  CAGR {cagr(mix7):.2f}   beta {b7:.2f}")
for k in [1.00,1.05,b7,1.10]:
    lev=[k*x for x in qqq]
    print(f"  Nasdaq escalado x{k:.2f} (sin coste de financiacion): CAGR {cagr(lev):.2f}")
print("  -> practicamente todo el +1,26 pp se replica subiendo la exposicion al Nasdaq.")
print("     No es una fuente de rentabilidad nueva, es la misma con mas tamanho.")

print("\n" + "="*118)
print("PESO OPTIMO de cada sleeve en una cartera con Nasdaq (maximiza el CAGR combinado)")
print("="*118)
print(f"{'variante':30s} {'peso opt':>9} {'CAGR':>7} {'vs Nasdaq':>10} {'descorr real':>13}")
out=[]
for nom,v,n,pool in V:
    c=corr(v,qqq); esp=interp(ALEA[pool],n); real=c-esp
    best=(-9,0)
    for i in range(0,101,5):
        w=i/100
        m=[w*x+(1-w)*y for x,y in zip(v,qqq)]
        if cagr(m)>best[0]: best=(cagr(m),w)
    out.append((best[0],nom,best[1],real))
for cg,nom,w,real in sorted(out,reverse=True)[:8]:
    print(f"{nom:30s} {w:9.0%} {cg:7.2f} {cg-cq:+10.2f} {real:+13.2f}")
print("\n  Nota: el peso optimo esta ajustado sobre la MISMA muestra que lo mide. Sobreajustado")
print("  por construccion. Sirve para ver la forma, no para fijar un peso de cartera.")
