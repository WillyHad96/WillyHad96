# Construye las variables CICLICAS a partir de key-metrics trimestral de FMP
# y las une a las decisiones de febrero del panel, con desfase anti-look-ahead.
import json, glob, os, datetime as dt, statistics as st

def pos(x, ventana):
    v=[a for a in ventana if a is not None]
    if x is None or len(v)<8: return None
    lo,hi=min(v),max(v)
    return None if hi==lo else (x-lo)/(hi-lo)

def media(ventana):
    v=[a for a in ventana if a is not None]
    return sum(v)/len(v) if len(v)>=8 else None

OUT=[]
for f in sorted(glob.glob('fmp_raw/*.json')):
    rows=json.load(open(f))
    rows=[r for r in rows if r.get('date')]
    rows.sort(key=lambda r:r['date'])
    sym=rows[0]['symbol']
    # EBITDA derivado y deuda neta
    for r in rows:
        ev=r.get('enterpriseValue'); ee=r.get('evToEBITDA'); mc=r.get('marketCap')
        r['_ebitda']= ev/ee if (ev and ee and abs(ee)>1e-9) else None
        r['_netdebt']= (ev-mc) if (ev is not None and mc is not None) else None
    for i,r in enumerate(rows):
        w20=rows[max(0,i-19):i+1]; w8=rows[max(0,i-7):i+1]
        if len(w20)<12: continue
        ebit_mid=media([q['_ebitda'] for q in w20])
        ev=r.get('enterpriseValue'); nd=r.get('_netdebt')
        d={'ticker':sym,'date':r['date'],
           'roce':r.get('returnOnCapitalEmployed'),
           'capexdep':r.get('capexToDepreciation'),
           'dio':r.get('daysOfInventoryOutstanding'),
           'evsales':r.get('evToSales'),
           'evebitda':r.get('evToEBITDA'),
           'ndebitda':r.get('netDebtToEBITDA'),
           'curratio':r.get('currentRatio'),
           'fcfy':r.get('freeCashFlowYield'),
           'iq':r.get('incomeQuality'),
           'ccc':r.get('cashConversionCycle'),
           # --- POSICION EN EL CICLO (0 = suelo de su propia historia de 20T) ---
           'pos_roce':   pos(r.get('returnOnCapitalEmployed'), [q.get('returnOnCapitalEmployed') for q in w20]),
           'pos_capexdep':pos(r.get('capexToDepreciation'),    [q.get('capexToDepreciation') for q in w20]),
           'pos_dio':    pos(r.get('daysOfInventoryOutstanding'),[q.get('daysOfInventoryOutstanding') for q in w20]),
           'pos_evsales':pos(r.get('evToSales'),               [q.get('evToSales') for q in w20]),
           'pos_fcfy':   pos(r.get('freeCashFlowYield'),       [q.get('freeCashFlowYield') for q in w20]),
           # --- MEDIAS Y METRICAS DE MITAD DE CICLO ---
           'capexdep_ma8': media([q.get('capexToDepreciation') for q in w8]),
           'ev_mid_ebitda': (ev/ebit_mid) if (ev and ebit_mid and ebit_mid>0) else None,
           'nd_mid_ebitda': (nd/ebit_mid) if (nd is not None and ebit_mid and ebit_mid>0) else None,
           }
        # --- CONFIRMACION DEL GIRO: primera derivada a 4 trimestres ---
        if i>=4:
            p=rows[i-4]
            for k,src in (('d_roce','returnOnCapitalEmployed'),('d_dio','daysOfInventoryOutstanding'),
                          ('d_capexdep','capexToDepreciation')):
                a,b=r.get(src),p.get(src)
                d[k]= (a-b) if (a is not None and b is not None) else None
        OUT.append(d)

print(f"filas trimestrales construidas: {len(OUT)}  tickers: {len({d['ticker'] for d in OUT})}")

# --- union con las decisiones de febrero del panel ---
P=[l.split(',') for l in open('ciclicas_ampliado.csv').read().splitlines()[1:]]
dec=[{'yr':int(p[0]),'ticker':p[1],'mom':p[2],'ret':p[3],'qqq':p[4]} for p in P]
por_tk={}
for d in OUT: por_tk.setdefault(d['ticker'],[]).append(d)
for k in por_tk: por_tk[k].sort(key=lambda d:d['date'])

VARS=['roce','capexdep','dio','evsales','evebitda','ndebitda','curratio','fcfy','iq','ccc',
      'pos_roce','pos_capexdep','pos_dio','pos_evsales','pos_fcfy',
      'capexdep_ma8','ev_mid_ebitda','nd_mid_ebitda','d_roce','d_dio','d_capexdep']
filas=[]; sin=0
for e in dec:
    hist=por_tk.get(e['ticker'])
    if not hist: sin+=1; continue
    # ANTI-LOOK-AHEAD: solo trimestres cerrados antes del 15-nov del anho anterior
    corte=f"{e['yr']-1}-11-15"
    prev=[d for d in hist if d['date']<=corte]
    if not prev: sin+=1; continue
    u=prev[-1]
    filas.append({**{k:e[k] for k in ('yr','ticker','mom','ret','qqq')},
                  'fdate':u['date'], **{v:u.get(v) for v in VARS}})
print(f"decisiones del panel unidas: {len(filas)}   sin datos FMP: {sin}")
cols=['yr','ticker','mom','ret','qqq','fdate']+VARS
with open('ciclicas_ciclo.csv','w') as f:
    f.write(','.join(cols)+'\n')
    for r in filas:
        f.write(','.join('' if r.get(c) is None else (f"{r[c]:.6g}" if isinstance(r[c],float) else str(r[c])) for c in cols)+'\n')
import collections
print("por anho:", dict(sorted(collections.Counter(r['yr'] for r in filas).items())))
cob={v:sum(1 for r in filas if r.get(v) is not None) for v in VARS}
print("cobertura:", {k:f"{100*v/len(filas):.0f}%" for k,v in cob.items()})
