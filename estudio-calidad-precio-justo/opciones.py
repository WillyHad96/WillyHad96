# ¿Comprar CALLS sobre la cartera en vez de acciones daria mas alfa?
# No hay historico de opciones en FMP, asi que se valoran con Black-Scholes usando la
# volatilidad REALIZADA del propio universo. Eso es GENEROSO: la implicita suele estar
# por encima de la realizada, asi que el resultado real seria peor que este.
import numpy as np, collections, bisect, math
RF=0.02
SEC={}
for l in open('universo_sectorizado.csv').read().splitlines()[1:]:
    p=l.split(','); SEC[(p[0],p[1])]=p[3]
H=open('ciclicas_ampliado.csv').read().splitlines(); cols=H[0].split(',')
ev=[]
for l in H[1:]:
    p=l.split(','); d={}
    for c,v in zip(cols,p):
        if c=='ticker': d[c]=v
        else:
            try: d[c]=float(v) if v!='' else None
            except: d[c]=None
    d['sec']=SEC.get((str(int(d['yr'])),d['ticker']))
    if d['sec']=='Indu' and d.get('ps') is not None: ev.append(d)
yrs=sorted({e['yr'] for e in ev}); by=collections.defaultdict(list)
for e in ev: by[e['yr']].append(e)
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1

def N(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
def bs_call(S,K,T,r,sig):
    if sig<=0 or T<=0: return max(S-K,0)
    d1=(math.log(S/K)+(r+sig*sig/2)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*N(d1)-K*math.exp(-r*T)*N(d2)

# cartera: cuartil barato de Industrials
sel=[]
for y in yrs:
    pool=by[y]; v=sorted(x['ps'] for x in pool)
    u=v[max(0,int(len(v)*0.25)-1)]
    sel.append([e for e in pool if e['ps']<=u])
rets_ac = np.array([np.mean([e['ret'] for e in c])/100 for c in sel])

# volatilidad IDIOSINCRATICA por nombre (la que paga la opcion), no la de la cartera
todos=np.array([e['ret'] for e in ev])/100
sig_nombre = todos.std(ddof=1)
print("="*92)
print("COMPRAR CALLS SOBRE INDUSTRIALS BARATAS EN VEZ DE ACCIONES")
print("="*92)
print(f"  volatilidad de un nombre suelto (realizada, 17 anhos): {100*sig_nombre:.1f}%")
print(f"  esa es la sigma con la que se valoran las opciones. La IMPLICITA real seria mayor.")
print()
print(f"  {'estrategia':<40}{'CAGR':>9}{'peor anho':>12}{'anhos +':>10}{'prima/spot':>13}")
print("  "+"-"*88)
print(f"  {'ACCIONES (cuartil barato)':<40}{100*cagr(rets_ac):>8.2f}%{100*rets_ac.min():>11.1f}%"
      f"{int(np.sum(rets_ac>0)):>7}/17{'':>13}")
for moneyness,etq in [(1.00,'CALL ATM (strike = spot)'),(1.10,'CALL 10% OTM'),(1.25,'CALL 25% OTM')]:
    prima = bs_call(1.0, moneyness, 1.0, RF, sig_nombre)
    r_op=[]
    for c in sel:
        # payoff medio de la cesta de calls, un contrato por nombre, equiponderado
        pay = np.mean([max((1+e['ret']/100) - moneyness, 0.0) for e in c])
        r_op.append(pay/prima - 1.0)   # todo el capital en primas cada anho
    r_op=np.array(r_op)
    print(f"  {etq:<40}{100*cagr(r_op):>8.2f}%{100*r_op.min():>11.1f}%"
          f"{int(np.sum(r_op>0)):>7}/17{100*prima:>12.1f}%")
print()
print("="*92)
print("¿Y SI SOLO EJECUTAMOS LOS PERCENTILES QUE NOS INTERESAN? — el oraculo")
print("="*92)
print("  Suponiendo que supieramos de antemano que nombres acaban en la cola (imposible,")
print("  AUC medido 0,41-0,57), ¿cuanto pagaria una call sobre SOLO esos?")
prima=bs_call(1.0,1.0,1.0,RF,sig_nombre)
for q,etq in [(75,'top 25% por retorno realizado'),(90,'top 10%'),(95,'top 5%')]:
    r_op=[]
    for c in sel:
        v=[e['ret'] for e in c]
        if len(v)<4: r_op.append(0.0); continue
        u=np.percentile(v,q); top=[x for x in v if x>=u]
        pay=np.mean([max((1+x/100)-1.0,0.0) for x in top])
        r_op.append(pay/prima-1.0)
    r_op=np.array(r_op)
    print(f"  ORACULO calls ATM sobre {etq:<32}{100*cagr(r_op):>8.2f}%  peor {100*r_op.min():>6.1f}%")
print()
print("  Referencia: el oraculo comprando ACCIONES del top 10% daba CAGR ~101% (ESTUDIO-COLAS).")
