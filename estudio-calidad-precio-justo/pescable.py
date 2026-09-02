# ¿La cola alta es PESCABLE? Que aspecto tenian, ANTES, los que acabaron en la cola.
# Si sus caracteristicas previas son indistinguibles del resto, no hay nada que acotar.
import numpy as np, collections
R=[l.split(',') for l in open('universo_sectorizado.csv').read().splitlines()[1:]]
ev=[dict(yr=int(r[0]),tk=r[1],g=r[2],mb=float(r[4]),cr=float(r[5]),r40=float(r[6]),
         mc=float(r[7]),mom=float(r[8])/100,ret=float(r[9])/100,qqq=float(r[10])/100) for r in R]
yrs=sorted({e['yr'] for e in ev})

def auc(pos,neg):
    """P(un evento de la cola tenga la variable mas alta que uno del resto). 0,5 = nada."""
    a=np.asarray(pos); b=np.asarray(neg)
    if len(a)==0 or len(b)==0: return float('nan')
    return float((a[:,None]>b[None,:]).mean() + 0.5*(a[:,None]==b[None,:]).mean())

for g,et in [('CIC','CICLICAS'),('NOC','NO CICLICAS')]:
    print("="*88)
    print(f"{et} — perfil PREVIO del decil superior de retorno frente al resto")
    print("="*88)
    print(f"  {'variable':<28}{'cola alta':>11}{'resto':>10}{'AUC':>8}   interpretacion")
    print("  "+"-"*82)
    for var,nom in [('mom','momento 12m previo'),('mc','percentil de capitalizacion'),
                    ('mb','pctl sd margen (alto=inestable)'),('cr','pctl sd crecimiento'),
                    ('r40','percentil regla 40')]:
        A=[];B=[]
        for y in yrs:
            E=[e for e in ev if e['yr']==y and e['g']==g]
            if len(E)<20: continue
            u=np.percentile([e['ret'] for e in E],90)
            A+= [e[var] for e in E if e['ret']>=u]
            B+= [e[var] for e in E if e['ret']< u]
        a=auc(A,B)
        señal = 'nada' if abs(a-0.5)<0.03 else ('DEBIL' if abs(a-0.5)<0.06 else 'algo')
        m=100 if var=='mom' else 1
        print(f"  {nom:<28}{m*np.mean(A):>11.2f}{m*np.mean(B):>10.2f}{a:>8.3f}   {señal}")
    print()

print("="*88)
print("CUANTO SE PUEDE CAPTURAR — deciles por MOMENTO previo (variable de seleccion real)")
print("="*88)
QQQ=np.array([np.mean([e['qqq'] for e in ev if e['yr']==y]) for y in yrs])
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
for g,et in [('CIC','ciclicas'),('NOC','no cic.')]:
    print(f"  {et}:")
    print(f"    {'decil de momento':<20}{'CAGR':>9}{'corr QQQ':>10}{'ret medio':>11}{'p90 del decil':>14}")
    for d in range(10):
        rr=[];p90=[]
        for y in yrs:
            E=sorted([e for e in ev if e['yr']==y and e['g']==g],key=lambda e:e['mom'])
            k=len(E)//10
            if k<2: continue
            sl=E[d*k:(d+1)*k]
            rr.append(np.mean([e['ret'] for e in sl])); p90.append(np.percentile([e['ret'] for e in sl],90))
        print(f"    {'D'+str(d+1)+(' (menor mom)' if d==0 else ' (mayor mom)' if d==9 else ''):<20}"
              f"{100*cagr(rr):>8.1f}%{np.corrcoef(rr,QQQ)[0,1]:>10.3f}{100*np.mean(rr):>10.1f}%{100*np.mean(p90):>13.1f}%")
    print()
