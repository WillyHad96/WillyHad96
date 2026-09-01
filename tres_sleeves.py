# (1) Confirmacion pares/impares de la variante defensiva D1.
# (2) Correlaciones cruzadas entre sleeves y libro de renta variable a tres patas.
import math, statistics as st
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
rows=[l.split(';') for l in open('rejilla_def.txt').read().strip().split('\n')]
yrs=[int(r[0]) for r in rows]; qqq=[float(r[1]) for r in rows]; spy=[float(r[2]) for r in rows]
D1=[float(r[3].split('|')[0]) for r in rows]
# C4 completo y C4 mitad ciclica, mismas ventanas (de correlacion.py y dos_mitades_c4.py)
C4=[-2.27,-42.47,27.18,30.65,13.55,11.52,39.03,8.98,-7.29,34.39,22.79,14.76,29.30,56.52,-3.40,1.59,51.93]
C4C=[1.81,-49.88,28.73,26.96,22.45,3.81,38.39,3.69,-7.09,35.03,19.34,-9.74,31.71,40.30,14.59,15.63,44.05]

print("=== (1) D1 'defensivos + momento' por mitades ===")
print(f"{'mitad':22s} {'n':>2} {'CAGR':>7} {'corrQ':>6} {'betaQ':>6} {'alfaQ':>7} {'peor':>6}")
for nom,sel in [("pares (descubrimiento)",[i for i,y in enumerate(yrs) if y%2==0]),
                ("impares (confirmacion)",[i for i,y in enumerate(yrs) if y%2==1]),
                ("todos",list(range(len(yrs))))]:
    d=[D1[i] for i in sel]; q=[qqq[i] for i in sel]
    alfa=sum(d)/len(d)-beta(d,q)*sum(q)/len(q)
    print(f"{nom:22s} {len(d):>2} {cagr(d):7.2f} {corr(d,q):+6.2f} {beta(d,q):6.2f} {alfa:+7.1f} {min(d):6.1f}")

print("\n=== (2) Correlaciones cruzadas entre sleeves (anual, 17 obs) ===")
S={"Nasdaq":qqq,"S&P":spy,"C4 completo":C4,"C4 ciclicos":C4C,"Def+momento":D1}
ks=list(S)
print(f"{'':14s}"+"".join(f"{k:>13s}" for k in ks))
for a in ks:
    print(f"{a:14s}"+"".join(f"{corr(S[a],S[b]):+13.2f}" for b in ks))

print("\n=== (3) Libros de renta variable, equiponderados y rebalanceados cada anho ===")
def mix(*vs): return [sum(x)/len(x) for x in zip(*vs)]
libros=[("Nasdaq solo",qqq),("Nasdaq + C4",mix(qqq,C4)),("Nasdaq + Def",mix(qqq,D1)),
        ("Nasdaq + C4 + Def",mix(qqq,C4,D1)),("Nasdaq + C4cic + Def",mix(qqq,C4C,D1)),
        ("C4 + Def (sin Nasdaq)",mix(C4,D1))]
print(f"{'libro':24s} {'CAGR':>7} {'desv':>5} {'peor':>6} {'CAGR/desv':>9} {'betaQ':>6} {'2008':>6} {'2022':>6}")
for nom,v in libros:
    print(f"{nom:24s} {cagr(v):7.2f} {st.stdev(v):5.1f} {min(v):6.1f} {cagr(v)/st.stdev(v):9.3f} {beta(v,qqq):6.2f} {v[1]:6.1f} {v[15]:6.1f}")
