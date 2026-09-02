# Estudio del eje temporal. Reglas cerradas en PREREGISTRO-EJE-TEMPORAL.md.
# Null = permutar el vector de exposicion entre anhos (fija CUANTAS veces sale,
# pregunta solo si acierta CUANDO). 20.000 permutaciones, semilla 13.
import numpy as np, math

RF = 0.02
D = [l.split(',') for l in open('senal_regimen.csv').read().splitlines()[1:]]
yr    = np.array([int(r[0])   for r in D])
slv   = np.array([float(r[1]) for r in D])/100.0
qqq   = np.array([float(r[2]) for r in D])/100.0
qprev = np.array([float(r[3]) for r in D])/100.0   # senal R1: Nasdaq 12m previos
mmom  = np.array([float(r[4]) for r in D])/100.0   # senal R2: mediana mom12 universo
n = len(yr)

cagr = lambda r: np.prod(1+r)**(1/len(r))-1
def corr(a,b): return np.corrcoef(a,b)[0,1]
def beta(a,b): return np.cov(a,b,ddof=1)[0,1]/np.var(b,ddof=1)

BASE_C, BASE_R, QQQ_C = cagr(slv), corr(slv,qqq), cagr(qqq)

def evalua(e, rf=RF):
    p = e*slv + (1-e)*rf
    return cagr(p), corr(p,qqq), beta(p,qqq), p

def permuta(e, rf=RF, IT=20000, seed=13):
    obs_c, obs_r, _, _ = evalua(e, rf)
    rng = np.random.default_rng(seed)
    E = np.array([rng.permutation(e) for _ in range(IT)])
    P = E*slv + (1-E)*rf
    cg = np.prod(1+P, axis=1)**(1/n)-1
    pm = P - P.mean(axis=1, keepdims=True); qm = qqq - qqq.mean()
    cr = (pm@qm)/np.sqrt((pm**2).sum(axis=1)*(qm**2).sum())
    p_c = (np.sum(cg >= obs_c)+1)/(IT+1)
    p_r = (np.sum(cr <= obs_r)+1)/(IT+1)
    p_j = (np.sum((cg >= obs_c) & (cr <= obs_r))+1)/(IT+1)
    return p_c, p_r, p_j, cr.mean(), cg.mean()

print("="*80)
print(f"BASE: C4 siempre invertido — CAGR {100*BASE_C:.2f}%  corr {BASE_R:.3f}  "
      f"beta {beta(slv,qqq):.2f}  ·  Nasdaq CAGR {100*QQQ_C:.2f}%")
print("="*80)

reglas = [("R1 momento del indice  (qqq 12m previos > 0)", (qprev > 0).astype(float)),
          ("R2 momento del universo (mediana mom12 > 0)",  (mmom  > 0).astype(float))]

resultados = {}
for nombre, e in reglas:
    c, r, b, p = evalua(e)
    p_c, p_r, p_j, cr_null, cg_null = permuta(e)
    dentro = int(e.sum())
    resultados[nombre] = dict(e=e, c=c, r=r, b=b, p_j=p_j)
    print()
    print(f"--- {nombre}")
    print(f"    dentro {dentro}/{n} anhos  ·  fuera en: "
          f"{', '.join(str(y) for y,x in zip(yr,e) if x==0) or '(ninguno)'}")
    print(f"    CAGR        {100*c:6.2f}%   (base {100*BASE_C:.2f}%, Nasdaq {100*QQQ_C:.2f}%)")
    print(f"    correlacion {r:6.3f}    (base {BASE_R:.3f})")
    print(f"    beta        {b:6.2f}     vol {100*p.std(ddof=1):.1f}%  (base {100*slv.std(ddof=1):.1f}%)")
    print(f"    peor anho   {100*p.min():6.1f}%   (base {100*slv.min():.1f}%, Nasdaq {100*qqq.min():.1f}%)")
    print(f"    --- contra el null de permutacion (mismo numero de salidas, al azar) ---")
    print(f"    corr media del azar con {dentro}/{n} dentro: {cr_null:.3f}   "
          f"CAGR medio del azar: {100*cg_null:.2f}%")
    print(f"    DESCORRELACION REAL = {r:.3f} - {cr_null:.3f} = {r-cr_null:+.3f}")
    print(f"    p(CAGR)={p_c:.4f}   p(corr)={p_r:.4f}   p_CONJUNTA={p_j:.4f}   "
          f"[criterio pre-registrado: < 0,025]")

print()
print("="*80)
print("CRITERIO PRE-REGISTRADO (seccion 5): las tres condiciones")
print("="*80)
for nombre, d in resultados.items():
    e = d['e']
    c1 = d['p_j'] < 0.025
    c2 = d['c'] >= QQQ_C
    par = np.array([y % 2 == 0 for y in yr]); imp = ~par
    def sub(m):
        ee = e[m]; pp = ee*slv[m]+(1-ee)*RF
        return cagr(pp)-cagr(slv[m]), corr(pp,qqq[m])-corr(slv[m],qqq[m])
    dpc, dpr = sub(par); dic, dir_ = sub(imp)
    c3 = (np.sign(dpc) == np.sign(dic)) and (np.sign(dpr) == np.sign(dir_))
    print(f"\n  {nombre}")
    print(f"    1. p_conjunta < 0,025        : {d['p_j']:.4f}   -> {'SI' if c1 else 'NO'}")
    print(f"    2. CAGR >= Nasdaq (13,89%)   : {100*d['c']:.2f}%  -> {'SI' if c2 else 'NO'}")
    print(f"    3. mismo signo pares/impares : dCAGR {100*dpc:+.1f}/{100*dic:+.1f} pp, "
          f"dcorr {dpr:+.3f}/{dir_:+.3f} -> {'SI' if c3 else 'NO'}")
    print(f"    VEREDICTO: {'SUPERVIVIENTE' if (c1 and c2 and c3) else 'NO DISTINGUIBLE DEL RUIDO'}")

print()
print("="*80)
print("LOS DOS ALFAS (regla B4) — el overlay vs siempre-invertido es el interno")
print("="*80)
for nombre, d in resultados.items():
    e = d['e']; p = e*slv+(1-e)*RF
    dif = p - slv                      # pareado: mismos anhos, misma seleccion
    t = dif.mean()/(dif.std(ddof=1)/math.sqrt(n)) if dif.std(ddof=1) > 0 else 0.0
    dq = p - qqq
    tq = dq.mean()/(dq.std(ddof=1)/math.sqrt(n))
    print(f"\n  {nombre}")
    print(f"    contra el Nasdaq  (contaminado): {100*dq.mean():+6.2f} pp/anho  t={tq:+.2f}")
    print(f"    overlay vs siempre-invertido (INMUNE): {100*dif.mean():+6.2f} pp/anho  t={t:+.2f}")
    print(f"    -> SE de la diferencia pareada: {100*dif.std(ddof=1)/math.sqrt(n):.2f} pp "
          f"(vs {100*slv.std(ddof=1)/math.sqrt(n):.2f} pp del nivel)")
