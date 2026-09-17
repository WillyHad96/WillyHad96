# AUDITORIA INDEPENDIENTE DE LA BARRA DE MEDIR:
# comparar el 'ret' del panel contra precios de FMP (fuente distinta), feb->feb.
import json,glob,os,bisect,collections
TR='/root/.claude/projects/-home-user-FMPDatablock/392c8eb2-5ddc-59ef-aa23-228ad4043af8/tool-results/'
PX={}
for f in glob.glob(TR+'mcp-FMP_MCP_Server-chart-*.txt'):
    txt=open(f).read()
    try:
        s=json.loads(txt); s=s['result'] if isinstance(s,dict) and 'result' in s else txt
    except Exception: s=txt
    try: rows=json.loads(s[s.index('['):s.rindex(']')+1])
    except Exception: continue
    if not rows or 'symbol' not in rows[0]: continue
    sym=rows[0]['symbol']
    d={r['date']:(r.get('price') or r.get('adjClose')) for r in rows if (r.get('price') or r.get('adjClose'))}
    if sym in PX: PX[sym].update(d)
    else: PX[sym]=d
PAN={}
H=open('ciclicas_ampliado.csv').read().splitlines(); cols=H[0].split(',')
for l in H[1:]:
    p=dict(zip(cols,l.split(',')))
    try: PAN[(p['ticker'],int(float(p['yr'])))]=float(p['ret'])
    except: pass
def px(sym,t):
    ds=sorted(PX[sym]); i=bisect.bisect_right(ds,t)-1
    return (ds[i],PX[sym][ds[i]]) if i>=0 else (None,None)
print("  ticker anho   panel    FMP feb->feb   diferencia   fechas usadas")
print("  ---------------------------------------------------------------------------")
difs=[]
for sym in sorted(PX):
    for y in (2022,2023):
        if (sym,y) not in PAN: continue
        d0,a=px(sym,f"{y}-02-15"); d1,b=px(sym,f"{y+1}-02-15")
        if not a or not b or d0<f"{y}-01-01": continue
        r=(b/a-1)*100; pan=PAN[(sym,y)]
        difs.append(r-pan)
        print(f"  {sym:<6} {y}  {pan:>7.1f}%  {r:>10.1f}%  {r-pan:>+9.1f} pp   {d0} -> {d1}")
if difs:
    import statistics as st
    print()
    print(f"  n={len(difs)}   diferencia media {st.mean(difs):+.1f} pp   mediana {st.median(difs):+.1f} pp   |max| {max(abs(x) for x in difs):.1f} pp")
