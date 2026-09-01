# Defensivos con filtros relajados: buscan una cartera REAL (>=15 nombres) con beta baja.
import math, statistics as st
NOM={1:"Def, regla40+mcap, top20% momento (rank2)",2:"Def, C4 completo, todos equiponderados",
     3:"Def, regla40+mcap, todos equiponderados",4:"Def, solo mcap>p25, todos",
     5:"Def+Energia+Materiales, C4 completo, todos",6:"Def+Energia+Materiales, regla40+mcap, todos",
     7:"ConsDef+Utilities (sin Salud), solo mcap>p25",8:"Def, estabilidad+mcap (sin regla40), todos"}
rows=[l.split(';') for l in open('rejilla_def.txt').read().strip().split('\n')]
yrs=[int(r[0]) for r in rows]; qqq=[float(r[1]) for r in rows]; spy=[float(r[2]) for r in rows]
V={}; N={}
for k in range(1,9):
    V[k]=[float(r[2+k].split('|')[0]) for r in rows]; N[k]=[int(r[2+k].split('|')[1]) for r in rows]
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
def mezcla(a,b,wa=0.5): return [wa*x+(1-wa)*y for x,y in zip(a,b)]
cq=cagr(qqq); sq=st.stdev(qqq)
print("=== Defensivos: cada variante sola ===")
print(f"{'#':>2} {'variante':46s} {'n/anho':>6} {'CAGR':>7} {'desv':>5} {'peor':>6} {'corrQ':>6} {'betaQ':>6} {'corrS':>6} {'betaS':>6} {'alfaQ':>6}")
for k in range(1,9):
    v=V[k]; n=sum(N[k])/len(N[k])
    alfa=(sum(v)/len(v)) - beta(v,qqq)*(sum(qqq)/len(qqq))
    print(f"{k:>2} {NOM[k]:46s} {n:6.0f} {cagr(v):7.2f} {st.stdev(v):5.1f} {min(v):6.1f} {corr(v,qqq):+6.2f} {beta(v,qqq):6.2f} {corr(v,spy):+6.2f} {beta(v,spy):6.2f} {alfa:+6.1f}")
print(f"\n=== Mezcla 50/50 con el Nasdaq (referencia Nasdaq solo: CAGR {cq:.2f}  desv {sq:.1f}  peor {min(qqq):.1f}) ===")
print(f"{'#':>2} {'variante':46s} {'CAGR':>7} {'desv':>5} {'peor':>6} {'CAGR/desv':>9} {'vs Nasdaq solo':>15}")
res=[]
for k in range(1,9):
    m=mezcla(V[k],qqq); c=cagr(m); s=st.stdev(m); res.append((c/s,k,c,s,min(m)))
for ratio,k,c,s,peor in sorted(res,reverse=True):
    print(f"{k:>2} {NOM[k]:46s} {c:7.2f} {s:5.1f} {peor:6.1f} {ratio:9.3f} {c-cq:+8.2f} pp, desv {s-sq:+.1f}")
print("\n=== Anhos con Nasdaq en negativo ===")
neg=[i for i,q in enumerate(qqq) if q<0]
print(f"{'':48s}"+"".join(f"{yrs[i]:>8}" for i in neg)+"   media")
print(f"{'Nasdaq':48s}"+"".join(f"{qqq[i]:8.1f}" for i in neg)+f"{sum(qqq[i] for i in neg)/len(neg):8.1f}")
for k in range(1,9):
    print(f"{k:>2} {NOM[k]:45s}"+"".join(f"{V[k][i]:8.1f}" for i in neg)+f"{sum(V[k][i] for i in neg)/len(neg):8.1f}")
