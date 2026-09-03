# ¿"Ciclicas" es un saco de cuatro cosas distintas? Y dentro, ¿donde estan las hundidas?
# Descriptivo sobre los 17 anhos. Une sector (universo_sectorizado) con variables (ciclicas_ampliado).
import numpy as np, collections
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
    if d['sec']: ev.append(d)
NOM={'Cons':'Consumer Cyclical','Indu':'Industrials','Basi':'Basic Materials','Ener':'Energy'}
yrs=sorted({e['yr'] for e in ev})
cagr=lambda r: np.prod(1+np.asarray(r))**(1/len(r))-1
QQQ=np.array([np.mean([e['qqq'] for e in ev if e['yr']==y])/100 for y in yrs])

print("="*96)
print(f"1. LOS CUATRO SUBTIPOS POR SEPARADO — {len(ev)} eventos, {len(yrs)} anhos")
print("="*96)
print(f"  {'sector':<20}{'n':>6}{'n/anho':>8}{'CAGR':>9}{'corr QQQ':>10}{'p10':>8}{'p50':>8}{'p90':>8}{'p99':>9}")
print("  "+"-"*90)
for s in ('Cons','Indu','Basi','Ener'):
    E=[e for e in ev if e['sec']==s]
    r=[];
    for y in yrs:
        v=[e['ret']/100 for e in E if e['yr']==y]
        r.append(np.mean(v) if v else 0.0)
    v=np.array([e['ret'] for e in E])
    print(f"  {NOM[s]:<20}{len(E):>6}{len(E)/len(yrs):>8.0f}{100*cagr(r):>8.2f}%{np.corrcoef(r,QQQ)[0,1]:>10.3f}"
          f"{np.percentile(v,10):>8.1f}{np.percentile(v,50):>8.1f}{np.percentile(v,90):>8.1f}{np.percentile(v,99):>9.1f}")
allr=[]
for y in yrs:
    v=[e['ret']/100 for e in ev if e['yr']==y]; allr.append(np.mean(v))
v=np.array([e['ret'] for e in ev])
print(f"  {'TODAS juntas':<20}{len(ev):>6}{len(ev)/len(yrs):>8.0f}{100*cagr(allr):>8.2f}%{np.corrcoef(allr,QQQ)[0,1]:>10.3f}"
      f"{np.percentile(v,10):>8.1f}{np.percentile(v,50):>8.1f}{np.percentile(v,90):>8.1f}{np.percentile(v,99):>9.1f}")
print(f"  Nasdaq: {100*cagr(QQQ):.2f}%")

print()
print("="*96)
print("2. ¿SE MUEVEN JUNTOS? — correlacion entre subtipos (si es baja, son animales distintos)")
print("="*96)
S={}
for s in ('Cons','Indu','Basi','Ener'):
    S[s]=np.array([np.mean([e['ret']/100 for e in ev if e['sec']==s and e['yr']==y] or [0]) for y in yrs])
print(f"  {'':<20}"+"".join(f"{NOM[x][:12]:>14}" for x in ('Cons','Indu','Basi','Ener')))
for a in ('Cons','Indu','Basi','Ener'):
    print(f"  {NOM[a]:<20}"+"".join(f"{np.corrcoef(S[a],S[b])[0,1]:>14.3f}" for b in ('Cons','Indu','Basi','Ener')))

print()
print("="*96)
print("3. LA SENHAL QUE REPLICA (barato vs su propia historia) — ¿funciona igual en los cuatro?")
print("="*96)
def auc(E,var,q=90):
    A=[];B=[]
    for y in yrs:
        Y=[e for e in E if e['yr']==y and e.get(var) is not None]
        if len(Y)<12: continue
        u=np.percentile([e['ret'] for e in Y],q)
        A+=[e[var] for e in Y if e['ret']>=u]; B+=[e[var] for e in Y if e['ret']<u]
    if len(A)<15 or len(B)<15: return None,len(A)
    a=np.array(A);b=np.array(B)
    return float((a[:,None]>b[None,:]).mean()+0.5*(a[:,None]==b[None,:]).mean()),len(A)
PAR=[y for y in yrs if y%2==0]; IMP=[y for y in yrs if y%2==1]
def auc_sub(E,var,anos,q=90):
    return auc([e for e in E if e['yr'] in anos],var,q)
print(f"  {'sector':<20}{'AUC pos_ps pares':>18}{'impares':>10}{'AUC ps nivel pares':>20}{'impares':>10}")
for s in ('Cons','Indu','Basi','Ener'):
    E=[e for e in ev if e['sec']==s]
    a1,_=auc_sub(E,'pos_ps',PAR); a2,_=auc_sub(E,'pos_ps',IMP)
    b1,_=auc_sub(E,'ps',PAR); b2,_=auc_sub(E,'ps',IMP)
    f=lambda x: f"{x:.3f}" if x is not None else "  n/d"
    print(f"  {NOM[s]:<20}{f(a1):>18}{f(a2):>10}{f(b1):>20}{f(b2):>10}")
