# EL FACTOR DE INVERSION (Cooper-Gulen-Schill 2008) sobre Industrials.
# Crecimiento del capital invertido / activos tangibles, medido ANTES de la decision.
# Tesis: bajo crecimiento de activos -> retornos altos. Es la disciplina de capacidad.
import json,glob,os,collections,numpy as np
SEC={}
for l in open('universo_sectorizado.csv').read().splitlines()[1:]:
    p=l.split(','); SEC.setdefault(p[1],p[3])
KM={}
for f in glob.glob('fmp_raw/*.json'):
    sym=os.path.basename(f)[:-5]
    if SEC.get(sym)!='Indu': continue
    rows=[r for r in json.load(open(f)) if r.get('date')]
    rows.sort(key=lambda r:r['date']); KM[sym]=rows
print(f"Industrials con key-metrics: {len(KM)}")

MET={}
for sym,rows in KM.items():
    out=[]
    for i,r in enumerate(rows):
        d={'date':r['date']}
        for campo,nom in [('investedCapital','cap_inv'),('tangibleAssetValue','act_tang'),
                          ('workingCapital','circ')]:
            a=r.get(campo); b=rows[i-4].get(campo) if i>=4 else None
            c=rows[i-8].get(campo) if i>=8 else None
            d[nom+'_g1']= (a/b-1) if (a is not None and b and b>0) else None
            d[nom+'_g2']= ((a/c)**0.5-1) if (a is not None and c and c>0 and a>0) else None
        # activos implicitos via ROA
        ni=r.get('returnOnAssets'); 
        d['roic']=r.get('returnOnInvestedCapital')
        d['capexrev']=r.get('capexToRevenue')
        d['capexdep']=r.get('capexToDepreciation')
        out.append(d)
    MET[sym]=out

H=open('ciclicas_ampliado.csv').read().splitlines(); cols=H[0].split(',')
ev=[]
for l in H[1:]:
    p=l.split(','); e={}
    for c,v in zip(cols,p):
        if c=='ticker': e[c]=v
        else:
            try: e[c]=float(v) if v!='' else None
            except: e[c]=None
    if SEC.get(e['ticker'])!='Indu' or e['ticker'] not in MET: continue
    corte=f"{int(e['yr'])-1}-11-15"
    prev=[d for d in MET[e['ticker']] if d['date']<=corte]
    if not prev: continue
    ev.append({**e, **{k:v for k,v in prev[-1].items() if k!='date'}})
print(f"decisiones unidas: {len(ev)}")
yrs=sorted({e['yr'] for e in ev}); PAR=[y for y in yrs if y%2==0]; IMP=[y for y in yrs if y%2==1]

def auc(var,anos,q=90):
    A=[];B=[]
    for y in anos:
        E=[e for e in ev if e['yr']==y and e.get(var) is not None]
        if len(E)<10: continue
        u=np.percentile([e['ret'] for e in E],q)
        A+=[e[var] for e in E if e['ret']>=u]; B+=[e[var] for e in E if e['ret']<u]
    if len(A)<12 or len(B)<12: return None
    a=np.array(A,float); b=np.array(B,float)
    return float((a[:,None]>b[None,:]).mean()+0.5*(a[:,None]==b[None,:]).mean())

print()
print("="*96)
print("FACTOR DE INVERSION — AUC contra el decil superior. <0,5 = BAJO crecimiento predice")
print("="*96)
print(f"  {'variable':<44}{'pares':>9}{'impares':>10}{'|des| min':>11}{'veredicto':>13}")
print("  "+"-"*92)
VARS=[('cap_inv_g1','crec. capital invertido 1 anho'),
      ('cap_inv_g2','crec. capital invertido 2 anhos (anualiz.)'),
      ('act_tang_g1','crec. activos tangibles 1 anho'),
      ('act_tang_g2','crec. activos tangibles 2 anhos (anualiz.)'),
      ('circ_g1','crec. circulante 1 anho'),
      ('capexrev','capex / ventas'),
      ('capexdep','capex / depreciacion'),
      ('roic','ROIC (nivel)'),
      ('dil','dilucion yoy (emision neta)'),
      ('ps','(control) P/S del panel')]
res=[]
for v,nom in VARS:
    ap=auc(v,PAR); ai=auc(v,IMP)
    if ap is None or ai is None: print(f"  {nom:<44}{'insuficiente':>43}"); continue
    dp,di=ap-0.5,ai-0.5; mismo=(dp>0)==(di>0); mn=min(abs(dp),abs(di))
    ver='PASA' if (mismo and mn>=0.10) else ('replica' if (mismo and mn>=0.05) else ('signo ok' if mismo else 'NO'))
    print(f"  {nom:<44}{ap:>9.3f}{ai:>10.3f}{mn:>11.3f}{ver:>13}")
    res.append((nom,v,ap,ai,mismo,mn))
print()
buenos=[r for r in res if r[4] and r[5]>=0.05]
print("  Replican con tamanho (|des|>=0,05 en AMBAS mitades):")
for nom,v,ap,ai,_,mn in sorted(buenos,key=lambda r:-r[5]):
    print(f"    {nom:<44} {ap:.3f} / {ai:.3f}   -> {'BAJO predice la cola' if ap<0.5 else 'ALTO predice la cola'}")
if not buenos: print("    ninguna")
