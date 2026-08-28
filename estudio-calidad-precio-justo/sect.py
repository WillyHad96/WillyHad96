import csv, statistics as st, random
sec={r['ticker']:r['sector'] for r in csv.DictReader(open('sectores.csv'))}
deu={}
for r in csv.DictReader(open('deuda.csv')):
    deu[(r['ticker'],int(r['yr']))]=(float(r['deuda']),float(r['caja']))
FIN={'AAT','CTRE','DCOM','LSI','CBRE'}
ev=[]
for r in csv.DictReader(open('panel_muestra.csv')):
    k=(r['ticker'],int(r['yr']))
    if k not in deu: continue
    d,c=deu[k]; v=float(r['ventas_M'])*1e6
    if r['ticker'] in FIN: continue
    ev.append(dict(tk=r['ticker'], yr=int(r['yr']), s=sec.get(r['ticker'],'?'),
                   ndv=(d-c)/v, ret=float(r['ret'])/100, qqq=float(r['qqq'])/100))
ev.sort(key=lambda e:e['ndv']); n=len(ev)
t1,t3=ev[:n//3], ev[-(n//3):]
print(f"Muestra sin REITs/bancos: {n} eventos\n")
print("=== COMPOSICION SECTORIAL DE LOS EXTREMOS ===")
from collections import Counter
c1,c3=Counter(e['s'] for e in t1),Counter(e['s'] for e in t3)
print(f"{'Sector':<24}{'T1 poca deuda':>15}{'T3 mucha deuda':>16}")
for s in sorted(set(c1)|set(c3)):
    print(f"{s:<24}{c1.get(s,0):>15}{c3.get(s,0):>16}")
print(f"\n  Tecnologia:  T1 {100*c1.get('Technology',0)/len(t1):.0f}%   T3 {100*c3.get('Technology',0)/len(t3):.0f}%")

print("\n=== EL TEST: repetir EXCLUYENDO tecnologia ===")
for lab, sub in [('Muestra completa', ev),
                 ('SIN Technology', [e for e in ev if e['s']!='Technology']),
                 ('Solo ciclicas/industriales', [e for e in ev if e['s'] in
                   ('Industrials','Consumer Cyclical','Basic Materials','Energy')])]:
    sub=sorted(sub,key=lambda e:e['ndv']); m=len(sub)
    if m<18: print(f"  {lab}: n={m}, insuficiente"); continue
    a,b=sub[:m//3], sub[-(m//3):]
    ea=st.mean([e['ret']-e['qqq'] for e in a]); eb=st.mean([e['ret']-e['qqq'] for e in b])
    obs=ea-eb
    exc=[e['ret']-e['qqq'] for e in sub]; B=20000; cnt=0
    for _ in range(B):
        s2=exc[:]; random.shuffle(s2)
        if st.mean(s2[:m//3])-st.mean(s2[-(m//3):]) >= obs: cnt+=1
    print(f"  {lab:<28} n={m:>3}  T1 {100*ea:>+6.1f}  T3 {100*eb:>+6.1f}  dif {100*obs:>+6.1f} pp   p={cnt/B:.4f}")
