# ¿Hay charco donde pescar? Distribucion completa de retornos anuales por evento,
# ciclicas vs no ciclicas, y comportamiento de las COLAS frente al Nasdaq.
# Descriptivo: no prueba ninguna regla, mide el premio disponible.
import numpy as np, collections
R=[l.split(',') for l in open('universo_sectorizado.csv').read().splitlines()[1:]]
ev=[dict(yr=int(r[0]),tk=r[1],g=r[2],mc=float(r[7]),mom=float(r[8])/100,
         ret=float(r[9])/100,qqq=float(r[10])/100) for r in R]
yrs=sorted({e['yr'] for e in ev})
by=collections.defaultdict(list)
for e in ev: by[(e['yr'],e['g'])].append(e['ret'])
QQQ=np.array([np.mean([e['qqq'] for e in ev if e['yr']==y]) for y in yrs])
PS=[1,5,10,25,50,75,90,95,99]

print("="*92)
print("1. DISTRIBUCION AGRUPADA DE LOS 17 ANHOS (retorno anual por evento, %)")
print("="*92)
print(f"  {'grupo':<8}{'n':>6}" + "".join(f"{'p'+str(p):>8}" for p in PS) + f"{'media':>8}{'>0':>7}")
for g,et in [('CIC','ciclicas'),('NOC','no cic.')]:
    v=np.array([e['ret'] for e in ev if e['g']==g])
    print(f"  {et:<8}{len(v):>6}" + "".join(f"{100*np.percentile(v,p):>8.1f}" for p in PS)
          + f"{100*v.mean():>8.1f}{100*np.mean(v>0):>6.0f}%")
print()
for g,et in [('CIC','ciclicas'),('NOC','no cic.')]:
    v=np.array([e['ret'] for e in ev if e['g']==g])
    print(f"  {et}: cola alta p90-p50 = {100*(np.percentile(v,90)-np.percentile(v,50)):>5.1f} pp   "
          f"cola baja p50-p10 = {100*(np.percentile(v,50)-np.percentile(v,10)):>5.1f} pp   "
          f"asimetria = {float(((v-v.mean())**3).mean()/v.std()**3):>5.2f}")

print()
print("="*92)
print("2. LA PREGUNTA QUE DECIDE — ¿la cola alta paga cuando el Nasdaq NO paga?")
print("="*92)
print(f"  {'anho':>5}{'Nasdaq':>9}" + "".join(f"{'CIC p'+str(p):>10}" for p in [10,50,90,95])
      + "".join(f"{'NOC p'+str(p):>10}" for p in [50,90]))
S={}
for g in ('CIC','NOC'):
    for p in PS: S[(g,p)]=np.array([np.percentile(by[(y,g)],p) for y in yrs])
for i,y in enumerate(yrs):
    mala=' <<<' if QQQ[i]<0 else ''
    print(f"  {y:>5}{100*QQQ[i]:>8.1f}%" + "".join(f"{100*S[('CIC',p)][i]:>10.1f}" for p in [10,50,90,95])
          + "".join(f"{100*S[('NOC',p)][i]:>10.1f}" for p in [50,90]) + mala)

print()
print("="*92)
print("3. CORRELACION DE CADA PERCENTIL CON EL NASDAQ")
print("="*92)
print("  Si la cola alta correlaciona MENOS que la mediana, hay algo que pescar ahi.")
print()
print(f"  {'percentil':<12}" + "".join(f"{'p'+str(p):>9}" for p in PS))
for g,et in [('CIC','ciclicas'),('NOC','no cic.')]:
    print(f"  {et:<12}" + "".join(f"{np.corrcoef(S[(g,p)],QQQ)[0,1]:>9.3f}" for p in PS))
print()
print(f"  {'exceso medio sobre el Nasdaq (pp/anho)':<40}")
for g,et in [('CIC','ciclicas'),('NOC','no cic.')]:
    print(f"  {et:<12}" + "".join(f"{100*np.mean(S[(g,p)]-QQQ):>9.1f}" for p in PS))
print()
print(f"  {'anhos (de 17) en que el percentil bate al Nasdaq':<40}")
for g,et in [('CIC','ciclicas'),('NOC','no cic.')]:
    print(f"  {et:<12}" + "".join(f"{int(np.sum(S[(g,p)]>QQQ)):>9d}" for p in PS))

print()
print("="*92)
print("4. AMPLITUD — ¿que fraccion del pool bate al Nasdaq cada anho?")
print("="*92)
for g,et in [('CIC','ciclicas'),('NOC','no cic.')]:
    fr=np.array([np.mean(np.array(by[(y,g)])>QQQ[i]) for i,y in enumerate(yrs)])
    print(f"  {et:<10} media {100*fr.mean():>5.1f}%   rango [{100*fr.min():.0f}%, {100*fr.max():.0f}%]"
          f"   corr con el Nasdaq {np.corrcoef(fr,QQQ)[0,1]:+.3f}")
