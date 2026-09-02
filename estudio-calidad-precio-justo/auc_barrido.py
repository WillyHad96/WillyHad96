# Barrido de AUC contra el decil superior de retorno, dentro de cada anho.
# Separado pares/impares desde el principio: solo interesa lo que REPLICA.
# AUC>0.5 = valor alto predice cola alta. AUC<0.5 = valor BAJO la predice.
import numpy as np, collections
H=open('ciclicas_ampliado.csv').read().splitlines()
cols=H[0].split(',')
ev=[]
for l in H[1:]:
    p=l.split(',')
    d={}
    ok=True
    for c,v in zip(cols,p):
        if c=='ticker': d[c]=v
        else:
            try: d[c]=float(v) if v!='' else None
            except: d[c]=None
    ev.append(d)
yrs=sorted({e['yr'] for e in ev})
PARES=[y for y in yrs if y%2==0]; IMPARES=[y for y in yrs if y%2==1]

def auc_var(var, anos):
    A=[];B=[]
    for y in anos:
        E=[e for e in ev if e['yr']==y and e[var] is not None]
        if len(E)<25: continue
        u=np.percentile([e['ret'] for e in E],90)
        A+=[e[var] for e in E if e['ret']>=u]; B+=[e[var] for e in E if e['ret']<u]
    if len(A)<20 or len(B)<20: return float('nan'),0
    a=np.array(A); b=np.array(B)
    return float((a[:,None]>b[None,:]).mean()+0.5*(a[:,None]==b[None,:]).mean()), len(A)

VARS=[('mom','momento 12m'),('acel','aceleracion ingresos'),('magn','magnitud relativa'),
      ('racha','racha de crecimiento'),('sorp','sorpresa vs estimado'),('guia','guia implicita'),
      ('desg','desaceleracion de guia'),('mop','margen operativo (nivel)'),
      ('reinv','reinversion'),('reac','reaccion al resultado'),('ps','multiplo P/S (nivel)'),
      ('dil','dilucion yoy'),('dmop','delta margen operativo'),
      ('pos_mop','POSICION margen op (0=suelo)'),('pos_mb','POSICION margen bruto'),
      ('pos_cr','POSICION crecimiento'),('pos_ps','POSICION multiplo P/S'),
      ('mop_vs_media','margen op / su media 5a')]

print("="*94)
print("BARRIDO DE AUC — decil superior de retorno, dentro de anho, sector ciclico")
print("="*94)
print(f"  {'variable':<32}{'AUC pares':>11}{'AUC impares':>13}{'|des| min':>11}{'replica?':>12}")
print("  "+"-"*88)
res=[]
for v,nom in VARS:
    ap,_=auc_var(v,PARES); ai,_=auc_var(v,IMPARES)
    if np.isnan(ap) or np.isnan(ai):
        print(f"  {nom:<32}{'—':>11}{'—':>13}{'datos insuf.':>23}"); continue
    dp,di=ap-0.5,ai-0.5
    mismo = (dp>0)==(di>0)
    mn=min(abs(dp),abs(di))
    marca = 'SI' if (mismo and mn>=0.03) else ('signo ok' if mismo else 'NO')
    if mismo and mn>=0.05: marca='SI, fuerte'
    print(f"  {nom:<32}{ap:>11.3f}{ai:>13.3f}{mn:>11.3f}{marca:>12}")
    res.append((nom,v,ap,ai,mismo,mn))
print()
print("  Referencia: |AUC-0,5| de 0,03 es debil, 0,06 es notable, 0,10 es fuerte.")
print("  Criterio declarado en ESTUDIO-COLAS.md: AUC > 0,60 (o < 0,40) replicado.")
print()
buenos=[r for r in res if r[4] and r[5]>=0.05]
print("  SUPERAN el umbral de replicacion fuerte (|des|>=0,05 en AMBAS mitades):")
if buenos:
    for nom,v,ap,ai,_,mn in sorted(buenos,key=lambda r:-r[5]):
        d='valor BAJO predice la cola' if ap<0.5 else 'valor ALTO predice la cola'
        print(f"    {nom:<32} pares {ap:.3f}  impares {ai:.3f}   -> {d}")
else:
    print("    ninguna")
