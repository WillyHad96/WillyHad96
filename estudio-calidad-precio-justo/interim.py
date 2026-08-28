import csv, statistics as st, random
# eventos ciclicos nuevos
ev_new={}
for blk in open('ciclicas_eventos.txt').read().strip().split(';'):
    t,s,evs = blk.split('#')
    for e in evs.split(','):
        y,v,r,q = e.split(':')
        ev_new[(t,int(y))] = (float(v)*1e6, float(r)/100, float(q)/100, s)
deu={}
for f in ['deuda_cic.csv']:
    for r in csv.DictReader(open(f)):
        deu[(r['ticker'],int(r['yr']))]=(float(r['deuda']),float(r['caja']))
nuevos=[]
for k,(d,c) in deu.items():
    if k not in ev_new: continue
    v,ret,qqq,s = ev_new[k]
    nuevos.append(dict(tk=k[0], yr=k[1], ndv=(d-c)/v, ret=ret, qqq=qqq, s=s))

# eventos ciclicos del piloto anterior
sec={r['ticker']:r['sector'] for r in csv.DictReader(open('sectores.csv'))}
deu0={}
for r in csv.DictReader(open('deuda.csv')):
    deu0[(r['ticker'],int(r['yr']))]=(float(r['deuda']),float(r['caja']))
CIC={'Industrials','Consumer Cyclical','Basic Materials','Energy'}
viejos=[]
for r in csv.DictReader(open('panel_muestra.csv')):
    k=(r['ticker'],int(r['yr']))
    if k not in deu0: continue
    s=sec.get(r['ticker'],'?')
    if s not in CIC: continue
    d,c=deu0[k]; v=float(r['ventas_M'])*1e6
    viejos.append(dict(tk=r['ticker'], yr=int(r['yr']), ndv=(d-c)/v,
                       ret=float(r['ret'])/100, qqq=float(r['qqq'])/100, s=s))
ev = viejos + nuevos
print(f"Eventos ciclicos/industriales: {len(viejos)} del piloto + {len(nuevos)} nuevos = {len(ev)}")
print(f"(el test que fallo tenia n=38)\n")

ev.sort(key=lambda e:e['ndv']); n=len(ev)
t1,t3=ev[:n//3], ev[-(n//3):]
print(f"{'Tercil':<10}{'n':>4}{'rango DN/ventas':>22}{'ret medio':>12}{'ret mediana':>13}{'vs NASDAQ':>12}")
for lab,g in [('T1 poca',t1),('T2 medio',ev[n//3:-(n//3)]),('T3 mucha',t3)]:
    vals=[e['ndv'] for e in g]; rets=[e['ret'] for e in g]
    exc=st.mean([e['ret']-e['qqq'] for e in g])
    print(f"{lab:<10}{len(g):>4}{f'{min(vals):.2f} a {max(vals):.2f}':>22}"
          f"{100*st.mean(rets):>11.1f}%{100*st.median(rets):>12.1f}%{100*exc:>11.1f}")
obs=st.mean([e['ret']-e['qqq'] for e in t1])-st.mean([e['ret']-e['qqq'] for e in t3])
exc=[e['ret']-e['qqq'] for e in ev]; B=20000; cnt=0
for _ in range(B):
    s2=exc[:]; random.shuffle(s2)
    if st.mean(s2[:n//3])-st.mean(s2[-(n//3):]) >= obs: cnt+=1
print(f"\n  Diferencia T1-T3: {100*obs:+.1f} pp     permutacion p={cnt/B:.4f}")
print(f"  (en el piloto con n=38 era: +5,7 pp, p=0,27)")
