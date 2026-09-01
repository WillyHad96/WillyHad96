# Relacion entre el alfa anual y cuanta cobertura de muertes tiene el panel ese anho.
import math, random, statistics as st

# yr, alfa vs QQQ (pp), filtro-vs-no-filtro (pp), tasa de muerte registrada en el panel (%)
D = [(2007,-1.5,7.6,0.06),(2008,-13.7,9.9,0.14),(2009,-15.7,-8.7,0.07),(2010,3.7,-3.6,0.02),
     (2011,3.8,9.2,0.04),(2012,3.5,5.5,0.08),(2013,6.2,2.8,0.10),(2014,-8.3,7.7,0.09),
     (2015,-2.8,7.3,0.32),(2016,8.5,-4.1,1.00),(2017,-4.3,2.0,0.56),(2018,10.8,5.9,0.32),
     (2019,-1.3,5.3,0.13),(2020,8.1,-11.8,0.43),(2021,-10.3,-1.3,1.59),(2022,21.4,7.9,2.54),
     (2023,6.0,9.0,3.76)]

def pearson(a,b):
    n=len(a); ma=sum(a)/n; mb=sum(b)/n
    num=sum((x-ma)*(y-mb) for x,y in zip(a,b))
    da=math.sqrt(sum((x-ma)**2 for x in a)); db=math.sqrt(sum((y-mb)**2 for y in b))
    return num/(da*db)

def perm_p(a,b,it=20000,seed=13):
    r0=abs(pearson(a,b)); rng=random.Random(seed); bb=list(b); c=0
    for _ in range(it):
        rng.shuffle(bb)
        if abs(pearson(a,bb))>=r0: c+=1
    return c/it

alfa=[d[1] for d in D]; filt=[d[2] for d in D]; mort=[d[3] for d in D]

print("=== Correlacion con la tasa de muerte registrada (proxy de 'dato limpio') ===")
for nom,v in [("alfa vs QQQ",alfa),("filtro vs no-filtro",filt)]:
    r=pearson(v,mort); print(f"  {nom:22s} r = {r:+.3f}   p(perm) = {perm_p(v,mort):.4f}")

print("\n=== Por tramos de cobertura de muertes ===")
tramos=[("sucio  (<0.20%)",lambda m:m<0.20),("medio  (0.20-1.0%)",lambda m:0.20<=m<=1.0),("limpio (>1.0%)",lambda m:m>1.0)]
print(f"  {'tramo':20s} {'anhos':>5s} {'alfa vs QQQ':>13s} {'filtro vs no':>14s}")
for nom,f in tramos:
    sub=[d for d in D if f(d[3])]
    a=[d[1] for d in sub]; g=[d[2] for d in sub]
    print(f"  {nom:20s} {len(sub):5d} {sum(a)/len(a):+12.1f} {sum(g)/len(g):+13.1f}")

print("\n=== Estabilidad de las dos medidas ===")
for nom,v in [("alfa vs QQQ",alfa),("filtro vs no-filtro",filt)]:
    m=sum(v)/len(v); s=st.stdev(v); t=m/(s/math.sqrt(len(v)))
    print(f"  {nom:22s} media {m:+6.2f} pp  desv {s:5.2f}  t = {t:+.2f}  anhos positivos {sum(1 for x in v if x>0)}/{len(v)}")
