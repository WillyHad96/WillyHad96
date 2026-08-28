import csv, statistics as st
deu={}
for r in csv.DictReader(open('deuda.csv')):
    deu[(r['ticker'],int(r['yr']))]=(float(r['deuda']),float(r['caja']))
FIN={'AAT','CTRE','DCOM','LSI','MAC','PECO','PNFP','UCB'}   # REITs y bancos
ev=[]
for r in csv.DictReader(open('panel_muestra.csv')):
    k=(r['ticker'],int(r['yr']))
    if k not in deu: continue
    d,c=deu[k]; v=float(r['ventas_M'])*1e6; m=float(r['mcap_M'])*1e6
    ev.append(dict(tk=r['ticker'], yr=int(r['yr']),
                   nd=(d-c), ndv=(d-c)/v, ndm=(d-c)/m,
                   ret=float(r['ret'])/100, qqq=float(r['qqq'])/100,
                   mop=float(r['mop'])/100, fin=r['ticker'] in FIN))
print(f"Eventos emparejados: {len(ev)}   (de los cuales REIT/banco: {sum(1 for e in ev if e['fin'])})")
op=[e for e in ev if not e['fin']]
print(f"Muestra operativa (sin REITs ni bancos): {len(op)} eventos, {len(set(e['tk'] for e in op))} empresas\n")

def tabla(rows, key, etiqueta, nq=3):
    rows=sorted(rows, key=lambda e:e[key]); n=len(rows); cortes=[]
    for q in range(nq):
        a=n*q//nq; b=n*(q+1)//nq; cortes.append(rows[a:b])
    print(f"=== {etiqueta} ===")
    print(f"{'Tercil':<8}{'n':>4}{'rango':>20}{'ret medio':>12}{'ret mediana':>13}{'<-30%':>8}{'<-45%':>8}{'vs QQQ':>9}")
    for i,g in enumerate(cortes):
        vals=[e[key] for e in g]; rets=[e['ret'] for e in g]
        cat30=100*sum(1 for x in rets if x<-0.30)/len(g)
        cat45=100*sum(1 for x in rets if x<-0.45)/len(g)
        exc=st.mean([e['ret']-e['qqq'] for e in g])
        rng=f"{min(vals):.2f} a {max(vals):.2f}"
        print(f"{'T'+str(i+1):<8}{len(g):>4}{rng:>20}{100*st.mean(rets):>11.1f}%{100*st.median(rets):>12.1f}%{cat30:>7.0f}%{cat45:>7.0f}%{100*exc:>8.1f}")
    print()

tabla(op,'ndv','DEUDA NETA / VENTAS')
tabla(op,'ndm','DEUDA NETA / CAPITALIZACION')

# caja neta vs deuda
cn=[e for e in op if e['nd']<0]; cd=[e for e in op if e['nd']>=0]
print("=== CAJA NETA frente a DEUDA NETA ===")
for g,lab in [(cn,'Con caja neta'),(cd,'Con deuda neta')]:
    rets=[e['ret'] for e in g]
    print(f"  {lab:<16} n={len(g):>3}  medio {100*st.mean(rets):>6.1f}%  mediana {100*st.median(rets):>6.1f}%  "
          f"peor {100*min(rets):>6.1f}%  <-30%: {100*sum(1 for x in rets if x<-0.30)/len(g):.0f}%")

# los peores desenlaces
print("\n=== LOS 8 PEORES DESENLACES: cuanta deuda tenian ===")
peor=sorted(op,key=lambda e:e['ret'])[:8]
print(f"{'Ticker':<8}{'Ano':>6}{'Retorno':>10}{'DN/Ventas':>12}{'DN/Cap':>10}{'MgOp':>8}")
for e in peor:
    print(f"{e['tk']:<8}{e['yr']:>6}{100*e['ret']:>9.1f}%{e['ndv']:>12.2f}{e['ndm']:>10.2f}{100*e['mop']:>7.1f}%")
mediana_todos=st.median([e['ndv'] for e in op])
print(f"\n  Mediana de DN/Ventas en toda la muestra: {mediana_todos:.2f}")
print(f"  Mediana de DN/Ventas en los 8 peores   : {st.median([e['ndv'] for e in peor]):.2f}")

print("\n\n=== COMPROBACION 1: PERMUTACION sobre el exceso vs NASDAQ ===")
import random
obs_t1=st.mean([e['ret']-e['qqq'] for e in sorted(op,key=lambda x:x['ndv'])[:23]])
obs_t3=st.mean([e['ret']-e['qqq'] for e in sorted(op,key=lambda x:x['ndv'])[46:]])
obs=obs_t1-obs_t3
exc=[e['ret']-e['qqq'] for e in op]
B=20000; cnt=0
for _ in range(B):
    s=exc[:]; random.shuffle(s)
    if (st.mean(s[:23])-st.mean(s[46:])) >= obs: cnt+=1
print(f"  Diferencia observada T1-T3: {100*obs:+.1f} pp")
print(f"  p (permutacion, 20.000): {cnt/B:.4f}")

print("\n=== COMPROBACION 2: ¿es deuda o es el tipo de empresa? ===")
t1=sorted(op,key=lambda x:x['ndv'])[:23]; t3=sorted(op,key=lambda x:x['ndv'])[46:]
print(f"  T1 (poca deuda): {', '.join(sorted(set(e['tk'] for e in t1)))}")
print(f"  T3 (mucha deuda): {', '.join(sorted(set(e['tk'] for e in t3)))}")
print(f"\n  Margen operativo medio  T1 {100*st.mean([e['mop'] for e in t1]):.1f}%   T3 {100*st.mean([e['mop'] for e in t3]):.1f}%")
print(f"  Ano medio de entrada    T1 {st.mean([e['yr'] for e in t1]):.1f}     T3 {st.mean([e['yr'] for e in t3]):.1f}")

print("\n=== COMPROBACION 3: ¿predice la deuda las catastrofes? ===")
cat=[e for e in op if e['ret']<-0.30]; nocat=[e for e in op if e['ret']>=-0.30]
print(f"  DN/Ventas mediana en los {len(cat)} desastres (<-30%): {st.median([e['ndv'] for e in cat]):.2f}")
print(f"  DN/Ventas mediana en los {len(nocat)} restantes        : {st.median([e['ndv'] for e in nocat]):.2f}")
obs2=st.median([e['ndv'] for e in cat])-st.median([e['ndv'] for e in nocat])
allv=[e['ndv'] for e in op]; cnt2=0
for _ in range(B):
    s=allv[:]; random.shuffle(s)
    if (st.median(s[:len(cat)])-st.median(s[len(cat):])) >= obs2: cnt2+=1
print(f"  p (permutacion): {cnt2/B:.4f}  ->  {'predice' if cnt2/B<0.05 else 'NO predice'}")

print("\n=== COMPROBACION 4: la MISMA empresa en momentos distintos ===")
from collections import defaultdict
g=defaultdict(list)
for e in op: g[e['tk']].append(e)
pares=[(k,v) for k,v in g.items() if len(v)>1 and max(x['ndv'] for x in v)-min(x['ndv'] for x in v)>0.10]
print(f"  {len(pares)} empresas aparecen con niveles de deuda muy distintos:")
difs=[]
for k,v in sorted(pares):
    v=sorted(v,key=lambda x:x['ndv'])
    baja,alta=v[0],v[-1]
    d=(baja['ret']-baja['qqq'])-(alta['ret']-alta['qqq']); difs.append(d)
    print(f"    {k:<6} deuda baja {baja['ndv']:>5.2f} ({baja['yr']}) exc {100*(baja['ret']-baja['qqq']):>6.1f}  |  "
          f"alta {alta['ndv']:>5.2f} ({alta['yr']}) exc {100*(alta['ret']-alta['qqq']):>6.1f}  |  dif {100*d:>+6.1f}")
print(f"\n  Media de la diferencia intra-empresa: {100*st.mean(difs):+.1f} pp  "
      f"(a favor de la version con menos deuda en {sum(1 for d in difs if d>0)}/{len(difs)})")

print("\n=== ESTIMACION PRELIMINAR del filtro (NO es un backtest de cartera) ===")
med=st.median([e['ndv'] for e in op])
bajo=[e for e in op if e['ndv']<=med]; alto=[e for e in op if e['ndv']>med]
for g2,lab in [(op,'Sin filtro'),(bajo,'Solo DN/Ventas <= mediana')]:
    r=[e['ret'] for e in g2]; q=[e['qqq'] for e in g2]
    print(f"  {lab:<28} n={len(g2):>3}  ret medio {100*st.mean(r):>6.1f}%  "
          f"exceso vs NASDAQ {100*st.mean([a-b for a,b in zip(r,q)]):>+6.1f} pp")
