# Rejilla de variantes para buscar beta descorrelacionada del Nasdaq.
# Fuente: rejilla_beta.txt (SQL sobre hypergrowth_panel, feb-feb 2007-2023).
# Benchmark comun: media del QQQ / SPY sobre todo el universo filtrado de cada anho.
import math, statistics as st
NOM={1:"C4 completo (todos los sectores)",2:"C4 solo sectores ciclicos",3:"C4 solo defensivos (ConsDef+Salud+Util)",
     4:"Ciclicos SIN filtro de estabilidad",5:"Ciclicos C4 SIN momento (equiponderado)",6:"Ciclicos C4 momento INVERTIDO (peor 20%)",
     7:"Ciclicos C4 + VALUE (P/S mas bajo 20%)",8:"Ciclicos sin estabilidad + VALUE",9:"Solo Energia+Materiales C4"}
rows=[l.split(';') for l in open('rejilla_beta.txt').read().strip().split('\n')]
yrs=[int(r[0]) for r in rows]; qqq=[float(r[1]) for r in rows]; spy=[float(r[2]) for r in rows]
V={}; N={}
for k in range(1,10):
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
cq=cagr(qqq); cs=cagr(spy)
print(f"Benchmarks: Nasdaq CAGR {cq:.2f}%  desv {st.stdev(qqq):.1f}  |  S&P CAGR {cs:.2f}%  desv {st.stdev(spy):.1f}")
print(f"Mezcla 50/50 Nasdaq+S&P: CAGR {cagr(mezcla(qqq,spy)):.2f}%  desv {st.stdev(mezcla(qqq,spy)):.1f}  peor {min(mezcla(qqq,spy)):.1f}\n")
print("=== Cada variante sola ===")
print(f"{'#':>2} {'variante':42s} {'n/anho':>6} {'CAGR':>7} {'desv':>5} {'peor':>6} {'corrQ':>6} {'betaQ':>6} {'corrS':>6} {'betaS':>6} {'alfaQ':>6}")
for k in range(1,10):
    v=V[k]; n=sum(N[k])/len(N[k])
    alfa=(sum(v)/len(v)) - beta(v,qqq)*(sum(qqq)/len(qqq))   # Jensen anual, media aritmetica
    print(f"{k:>2} {NOM[k]:42s} {n:6.0f} {cagr(v):7.2f} {st.stdev(v):5.1f} {min(v):6.1f} {corr(v,qqq):+6.2f} {beta(v,qqq):6.2f} {corr(v,spy):+6.2f} {beta(v,spy):6.2f} {alfa:+6.1f}")
print("\n=== Lo que importa: mezcla 50/50 con el Nasdaq, rebalanceada cada anho ===")
print("  (referencia: Nasdaq solo  CAGR %.2f  desv %.1f  peor %.1f)" % (cq, st.stdev(qqq), min(qqq)))
print(f"{'#':>2} {'variante':42s} {'CAGR':>7} {'desv':>5} {'peor':>6} {'CAGR/desv':>9} {'vs Nasdaq solo':>15}")
res=[]
for k in range(1,10):
    m=mezcla(V[k],qqq); c=cagr(m); s=st.stdev(m)
    res.append((c/s,k,c,s,min(m)))
for ratio,k,c,s,peor in sorted(res,reverse=True):
    print(f"{k:>2} {NOM[k]:42s} {c:7.2f} {s:5.1f} {peor:6.1f} {ratio:9.3f} {c-cq:+8.2f} pp, desv {s-st.stdev(qqq):+.1f}")
print("\n=== Anhos con Nasdaq en negativo: que hizo cada variante ===")
neg=[i for i,q in enumerate(qqq) if q<0]
print(f"{'':44s}"+"".join(f"{yrs[i]:>8}" for i in neg)+"   media")
print(f"{'Nasdaq':44s}"+"".join(f"{qqq[i]:8.1f}" for i in neg)+f"{sum(qqq[i] for i in neg)/len(neg):8.1f}")
for k in range(1,10):
    print(f"{k:>2} {NOM[k]:41s}"+"".join(f"{V[k][i]:8.1f}" for i in neg)+f"{sum(V[k][i] for i in neg)/len(neg):8.1f}")
print("\nAVISO: 17 observaciones. Error tipico de una correlacion ~0,15; de un CAGR ~6 pp.")
print("       Variantes 3 y 9 tienen 2-7 nombres por anho: no son carteras, son anecdotas.")
