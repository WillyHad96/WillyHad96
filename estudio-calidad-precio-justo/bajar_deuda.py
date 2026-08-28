#!/usr/bin/env python3
"""Descarga enterprise-values (anual) de FMP para los 905 tickers del pool.
Uso:  FMP_KEY=xxxx python3 bajar_deuda.py
Salida: deuda_full.csv  (ticker,fecha,deuda,caja,acciones,mcap)
"""
import os, sys, json, time, urllib.request, urllib.error, csv

KEY = os.environ.get('FMP_KEY','').strip()
if not KEY:
    sys.exit("Falta FMP_KEY en el entorno")

pares = []
for tok in open('tickers_pool.txt').read().replace('\n','').split(','):
    tok = tok.strip()
    if ':' in tok:
        t, l = tok.split(':'); pares.append((t, int(l)))

def pedir(url):
    req = urllib.request.Request(url, headers={'User-Agent':'research/1.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def bajar(tk, lim):
    urls = [
      f"https://financialmodelingprep.com/stable/enterprise-values?symbol={tk}&period=annual&limit={lim}&apikey={KEY}",
      f"https://financialmodelingprep.com/api/v3/enterprise-values/{tk}?period=annual&limit={lim}&apikey={KEY}",
    ]
    for u in urls:
        for intento in range(3):
            try:
                d = pedir(u)
                if isinstance(d, list) and d: return d
                if isinstance(d, dict) and d.get('Error Message'): break
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 502, 503):
                    time.sleep(2*(intento+1)); continue
                break
            except Exception:
                time.sleep(1); continue
    return None

out = open('deuda_full.csv','w', newline='')
w = csv.writer(out); w.writerow(['ticker','fecha','deuda','caja','acciones','mcap'])
ok = fallo = filas = 0
for i,(tk,lim) in enumerate(pares,1):
    d = bajar(tk, lim)
    if not d:
        fallo += 1; print(f"  FALLO {tk}", file=sys.stderr)
    else:
        ok += 1
        for r in d:
            w.writerow([tk, r.get('date'), r.get('addTotalDebt'),
                        r.get('minusCashAndCashEquivalents'),
                        r.get('numberOfShares'), r.get('marketCapitalization')])
            filas += 1
    if i % 50 == 0:
        out.flush(); print(f"{i}/{len(pares)}  ok={ok} fallo={fallo} filas={filas}", flush=True)
    time.sleep(0.12)
out.close()
print(f"\nTERMINADO: {ok} tickers ok, {fallo} fallidos, {filas} filas -> deuda_full.csv")
