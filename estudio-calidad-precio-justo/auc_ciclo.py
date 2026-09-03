# TEST PILOTO. Umbral pre-declarado en DISENHO-PANEL-CICLICAS.md seccion 6:
# AUC >= 0,60 (o <= 0,40) replicado en pares e impares.
import numpy as np, collections
H=open('ciclicas_ciclo.csv').read().splitlines(); cols=H[0].split(',')
ev=[]
for l in H[1:]:
    p=l.split(','); d={}
    for c,v in zip(cols,p):
        if c=='ticker' or c=='fdate': d[c]=v
        else:
            try: d[c]=float(v) if v!='' else None
            except: d[c]=None
    ev.append(d)
yrs=sorted({e['yr'] for e in ev}); PAR=[y for y in yrs if y%2==0]; IMP=[y for y in yrs if y%2==1]

def auc(var,anos,q=80):
    A=[];B=[]
    for y in anos:
        E=[e for e in ev if e['yr']==y and e.get(var) is not None]
        if len(E)<12: continue
        u=np.percentile([e['ret'] for e in E],q)
        A+=[e[var] for e in E if e['ret']>=u]; B+=[e[var] for e in E if e['ret']<u]
    if len(A)<12 or len(B)<12: return None,0,0
    a=np.array(A,float); b=np.array(B,float)
    return float((a[:,None]>b[None,:]).mean()+0.5*(a[:,None]==b[None,:]).mean()), len(A), len(B)

VARS=[('pos_roce','POSICION ROCE (0=suelo)'),('pos_capexdep','POSICION capex/deprec.'),
      ('pos_dio','POSICION dias inventario'),('pos_evsales','POSICION EV/ventas'),
      ('pos_fcfy','POSICION FCF yield'),
      ('capexdep','capex/depreciacion (nivel)'),('capexdep_ma8','capex/deprec. media 8T'),
      ('ev_mid_ebitda','EV / EBITDA mitad de ciclo'),('nd_mid_ebitda','deuda neta / EBITDA m.c.'),
      ('evsales','EV/ventas (nivel)'),('evebitda','EV/EBITDA (nivel)'),('ndebitda','deuda neta/EBITDA'),
      ('roce','ROCE (nivel)'),('dio','dias de inventario (nivel)'),('curratio','current ratio'),
      ('fcfy','FCF yield'),('iq','calidad del beneficio'),('ccc','ciclo de conversion de caja'),
      ('d_roce','GIRO: delta ROCE 4T'),('d_dio','GIRO: delta dias invent. 4T'),
      ('d_capexdep','GIRO: delta capex/deprec. 4T'),('mom','momento 12m (control)')]

for q,et in [(80,'QUINTIL superior'),(90,'DECIL superior')]:
    print("="*92)
    print(f"AUC contra el {et} de retorno — piloto 50 tickers, {len(ev)} decisiones, {len(yrs)} anhos")
    print("="*92)
    print(f"  {'variable':<32}{'AUC pares':>11}{'AUC impares':>13}{'|des| min':>11}{'veredicto':>14}")
    print("  "+"-"*88)
    res=[]
    for v,nom in VARS:
        ap,na,nb=auc(v,PAR,q); ai,_,_=auc(v,IMP,q)
        if ap is None or ai is None: print(f"  {nom:<32}{'datos insuficientes':>49}"); continue
        dp,di=ap-0.5,ai-0.5; mismo=(dp>0)==(di>0); mn=min(abs(dp),abs(di))
        ver = 'PASA' if (mismo and mn>=0.10) else ('replica' if (mismo and mn>=0.05) else ('signo ok' if mismo else 'no replica'))
        print(f"  {nom:<32}{ap:>11.3f}{ai:>13.3f}{mn:>11.3f}{ver:>14}")
        res.append((nom,ap,ai,mismo,mn))
    print()

# ---- interaccion de la seccion 5 del disenho ----
print("="*92)
print("LA INTERACCION — suelo de ciclo + valoracion de suelo + balance que sobrevive")
print("="*92)
def rk(vals):
    o=sorted(range(len(vals)),key=lambda i:vals[i]); r=[0]*len(vals)
    for j,i in enumerate(o): r[i]=j/(len(vals)-1) if len(vals)>1 else 0.5
    return r
for e in ev: e['score']=None
for y in yrs:
    E=[e for e in ev if e['yr']==y and e.get('pos_roce') is not None
       and e.get('pos_evsales') is not None and e.get('nd_mid_ebitda') is not None]
    if len(E)<12: continue
    r1=rk([e['pos_roce'] for e in E]); r2=rk([e['pos_evsales'] for e in E]); r3=rk([e['nd_mid_ebitda'] for e in E])
    for e,a,b,c in zip(E,r1,r2,r3): e['score']=-(a+b+c)   # alto = suelo+barato+sano
ap,na,nb=auc('score',PAR,80); ai,_,_=auc('score',IMP,80)
print(f"  score compuesto (quintil sup.)   pares {ap:.3f}   impares {ai:.3f}   n={na}/{nb}")
ap9,_,_=auc('score',PAR,90); ai9,_,_=auc('score',IMP,90)
print(f"  score compuesto (decil sup.)     pares {ap9:.3f}   impares {ai9:.3f}")
print()
print("  Umbral pre-declarado: AUC >= 0,60 replicado en ambas mitades.")
