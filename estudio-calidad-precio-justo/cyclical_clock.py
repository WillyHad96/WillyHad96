# TEST DEL PROTOCOLO /cyclical_clock — sus metricas C1-C5 como SENAL PREDICTIVA.
# Traduce el protocolo a variables medibles en cada decision de febrero y mide
# su AUC contra el decil superior de retorno, partido en pares/impares.
# Desfase anti-look-ahead: ultimo trimestre cerrado antes del 15-nov del anho anterior.
import json,glob,os,collections,numpy as np
SEC={}
for l in open('universo_sectorizado.csv').read().splitlines()[1:]:
    p=l.split(','); SEC.setdefault(p[1],p[3])
IS={}
for f in glob.glob('fmp_is/*.json'):
    sym=os.path.basename(f)[:-5]
    if SEC.get(sym)!='Indu': continue
    rows=[r for r in json.load(open(f)) if r.get('date') and r.get('revenue')]
    rows.sort(key=lambda r:r['date']); IS[sym]=rows
print(f"Industrials con income-statement trimestral: {len(IS)}")

def ttm(rows,i,campo):
    if i<3: return None
    v=[rows[j].get(campo) for j in range(i-3,i+1)]
    return sum(v) if all(x is not None for x in v) else None

# --- construir metricas del protocolo por trimestre ---
MET={}
for sym,rows in IS.items():
    out=[]
    for i,r in enumerate(rows):
        rev=ttm(rows,i,'revenue'); oi=ttm(rows,i,'operatingIncome'); da=ttm(rows,i,'depreciationAndAmortization')
        if not rev or oi is None or da is None or rev<=0: out.append(None); continue
        m=(oi+da)/rev                                  # C2: margen EBITDA TTM
        hist=[]
        for j in range(max(0,i-39),i+1):               # C1: 10 anhos de margen TTM
            rv=ttm(rows,j,'revenue'); o=ttm(rows,j,'operatingIncome'); d=ttm(rows,j,'depreciationAndAmortization')
            if rv and o is not None and d is not None and rv>0: hist.append((o+d)/rv)
        if len(hist)<12: out.append(None); continue
        med=float(np.mean(hist)); pico=max(hist[:-1]) if len(hist)>1 else m; suelo=min(hist)
        d={'date':r['date'],
           'C2_margen':m,
           'C3_vs_media': m/med if med>0 else None,
           'C3_posicion': (m-suelo)/(pico-suelo) if pico>suelo else None,
           'C3_sobre_pico': 1.0 if m>pico else 0.0,
           'C4_ebitda_riesgo': (1-med/m) if m>0 else None}
        # C5 incremental: version SECUENCIAL (la del protocolo) y version INTERANUAL
        if i>=3:
            dr=rows[i]['revenue']-rows[i-3]['revenue']; do=rows[i]['operatingIncome']-rows[i-3]['operatingIncome']
            d['C5_seq']= (do/dr) if dr and abs(dr)>1e6 else None
        if i>=4:
            dr=rows[i]['revenue']-rows[i-4]['revenue']; do=rows[i]['operatingIncome']-rows[i-4]['operatingIncome']
            d['C5_yoy']= (do/dr) if dr and abs(dr)>1e6 else None
        mop = (oi/rev) if rev>0 else None
        d['margen_op']=mop
        for k in ('C5_seq','C5_yoy'):
            d[k+'_vs_margen']= (d[k]-mop) if (d.get(k) is not None and mop is not None) else None
        rev4=ttm(rows,i-4,'revenue') if i>=7 else None
        d['C6_crec']= (rev/rev4-1) if rev4 and rev4>0 else None
        out.append(d)
    MET[sym]=out

# --- unir con las decisiones del panel ---
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
    prev=[d for d in MET[e['ticker']] if d and d['date']<=corte]
    if not prev: continue
    ev.append({**e, **{k:v for k,v in prev[-1].items() if k!='date'}})
print(f"decisiones unidas: {len(ev)}   tickers: {len({e['ticker'] for e in ev})}")
yrs=sorted({e['yr'] for e in ev}); PAR=[y for y in yrs if y%2==0]; IMP=[y for y in yrs if y%2==1]

def auc(var,anos,q=90):
    A=[];B=[]
    for y in anos:
        E=[e for e in ev if e['yr']==y and e.get(var) is not None]
        if len(E)<10: continue
        u=np.percentile([e['ret'] for e in E],q)
        A+=[e[var] for e in E if e['ret']>=u]; B+=[e[var] for e in E if e['ret']<u]
    if len(A)<12 or len(B)<12: return None,0
    a=np.array(A,float); b=np.array(B,float)
    return float((a[:,None]>b[None,:]).mean()+0.5*(a[:,None]==b[None,:]).mean()), len(A)

print()
print("="*100)
print("AUC DE LAS METRICAS DEL PROTOCOLO contra el decil superior — Industrials")
print("="*100)
print(f"  {'metrica del protocolo':<40}{'AUC pares':>11}{'AUC impares':>13}{'|des| min':>11}{'replica?':>12}")
print("  "+"-"*96)
VARS=[('C2_margen','C2 margen EBITDA (nivel)'),
      ('C3_vs_media','C3 margen / media del ciclo'),
      ('C3_posicion','C3 posicion en el rango (0=suelo)'),
      ('C3_sobre_pico','C3 supera el pico previo (0/1)'),
      ('C4_ebitda_riesgo','C4 EBITDA en riesgo'),
      ('C5_seq','C5 incremental SECUENCIAL'),
      ('C5_seq_vs_margen','C5 incremental seq - margen op'),
      ('C5_yoy','C5 incremental INTERANUAL'),
      ('C5_yoy_vs_margen','C5 incremental yoy - margen op'),
      ('C6_crec','C6 crecimiento de ventas TTM'),
      ('ps','(control) P/S del panel')]
for v,nom in VARS:
    ap,na=auc(v,PAR); ai,_=auc(v,IMP)
    if ap is None or ai is None: print(f"  {nom:<40}{'datos insuficientes':>47}"); continue
    dp,di=ap-0.5,ai-0.5; mismo=(dp>0)==(di>0); mn=min(abs(dp),abs(di))
    ver='PASA' if (mismo and mn>=0.10) else ('replica' if (mismo and mn>=0.05) else ('signo ok' if mismo else 'NO'))
    print(f"  {nom:<40}{ap:>11.3f}{ai:>13.3f}{mn:>11.3f}{ver:>12}")
print()
print("  Umbral del piloto: AUC >= 0,60 (o <= 0,40) replicado en ambas mitades.")
