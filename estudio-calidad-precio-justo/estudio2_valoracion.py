# ESTUDIO 2: ¿que metrica de valoracion da MAS alfa interno y MENOS beta en Industrials?
# Compara el P/S del panel contra las de FMP (EV/ventas, EV/EBITDA, P/tangible book,
# earnings yield, FCF yield). Desfase anti-look-ahead identico al piloto.
import json,glob,os,collections,numpy as np,bisect
RF=0.02
SEC={}
for l in open('universo_sectorizado.csv').read().splitlines()[1:]:
    p=l.split(','); SEC.setdefault(p[1],p[3])
# --- serie trimestral FMP por ticker ---
FMP={}
for f in glob.glob('fmp_raw/*.json'):
    sym=os.path.basename(f)[:-5]
    if SEC.get(sym)!='Indu': continue
    rows=[r for r in json.load(open(f)) if r.get('date')]
    rows.sort(key=lambda r:r['date'])
    FMP[sym]=rows
print(f"Industrials con datos FMP: {len(FMP)}")
# --- panel ---
H=open('ciclicas_ampliado.csv').read().splitlines(); cols=H[0].split(',')
ev=[]
for l in H[1:]:
    p=l.split(','); d={}
    for c,v in zip(cols,p):
        if c=='ticker': d[c]=v
        else:
            try: d[c]=float(v) if v!='' else None
            except: d[c]=None
    if SEC.get(d['ticker'])=='Indu' and d['ticker'] in FMP: ev.append(d)
# --- unir con desfase: ultimo trimestre cerrado antes del 15-nov del anho anterior ---
for e in ev:
    corte=f"{int(e['yr'])-1}-11-15"
    prev=[r for r in FMP[e['ticker']] if r['date']<=corte]
    if not prev: continue
    u=prev[-1]
    mc=u.get('marketCap'); tb=u.get('tangibleAssetValue')
    e['evs']=u.get('evToSales'); e['eve']=u.get('evToEBITDA')
    e['ptb']=(mc/tb) if (mc and tb and tb>0) else None
    e['ey']=u.get('earningsYield'); e['fcfy']=u.get('freeCashFlowYield')
ev=[e for e in ev if e.get('evs') is not None]
yrs=sorted({e['yr'] for e in ev}); by=collections.defaultdict(list)
for e in ev: by[e['yr']].append(e)
Q=np.array([np.mean([e['qqq'] for e in by[y]])/100 for y in yrs])
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
print(f"eventos unidos: {len(ev)}   anhos: {len(yrs)} ({yrs[0]}-{yrs[-1]})   n/anho: {len(ev)/len(yrs):.0f}")
PAR=[i for i,y in enumerate(yrs) if y%2==0]; IMP=[i for i,y in enumerate(yrs) if y%2==1]

def prueba(var, barato_es_bajo=True):
    bar=[];fam=[]
    for y in yrs:
        pool=[e for e in by[y] if e.get(var) is not None]
        if len(pool)<8: bar.append(0.0); fam.append(0.0); continue
        v=sorted(x[var] for x in pool)
        if barato_es_bajo:
            u=v[max(0,int(len(v)*0.25)-1)]; c=[e for e in pool if e[var]<=u]
        else:
            u=v[min(len(v)-1,int(len(v)*0.75))]; c=[e for e in pool if e[var]>=u]
        bar.append(np.mean([e['ret'] for e in c])/100)
        fam.append(np.mean([e['ret'] for e in pool])/100)
    bar=np.array(bar); fam=np.array(fam); sp=bar-fam
    b=np.cov(bar,Q,ddof=1)[0,1]/np.var(Q,ddof=1)
    alfa=(bar.mean()-RF)-b*(Q.mean()-RF)
    t=sp.mean()/(sp.std(ddof=1)/np.sqrt(len(sp))) if sp.std(ddof=1)>0 else 0
    return cagr(bar), np.corrcoef(bar,Q)[0,1], b, alfa, sp.mean(), t, sp[PAR].mean(), sp[IMP].mean()

print()
print("="*104)
print("ESTUDIO 2 — que metrica de valoracion da mas ALFA INTERNO y menos BETA")
print("="*104)
print(f"  {'metrica':<28}{'CAGR':>9}{'corr':>7}{'beta':>7}{'alfaJ':>8}{'alfa int':>10}{'t':>7}{'pares':>8}{'impares':>9}")
print("  "+"-"*100)
for var,nom,bajo in [('ps','P/S del panel (base)',True),('evs','EV/ventas (FMP)',True),
                     ('eve','EV/EBITDA (FMP)',True),('ptb','P/valor tangible (FMP)',True),
                     ('ey','earnings yield (alto=barato)',False),('fcfy','FCF yield (alto=barato)',False)]:
    try:
        cg,c,b,aj,ai,t,pa,im=prueba(var,bajo)
        print(f"  {nom:<28}{100*cg:>8.2f}%{c:>7.3f}{b:>7.2f}{100*aj:>7.2f}%{100*ai:>9.2f}{t:>7.2f}{100*pa:>7.1f}{100*im:>8.1f}")
    except Exception as ex:
        print(f"  {nom:<28} error: {ex}")
famr=np.array([np.mean([e['ret'] for e in by[y]])/100 for y in yrs])
print(f"  {'(familia Industrials)':<28}{100*cagr(famr):>8.2f}%{np.corrcoef(famr,Q)[0,1]:>7.3f}"
      f"{np.cov(famr,Q,ddof=1)[0,1]/np.var(Q,ddof=1):>7.2f}")
print(f"  {'(Nasdaq)':<28}{100*cagr(Q):>8.2f}%{1.0:>7.3f}{1.0:>7.2f}")
print()
print("  alfa int = media anual de (cuartil barato - su familia). t sobre esa diferencia pareada.")
print("  Objetivo declarado: SUBIR el alfa interno y BAJAR la beta de 1,11.")
