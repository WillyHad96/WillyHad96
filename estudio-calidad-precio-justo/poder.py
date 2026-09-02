# Potencia disponible en el eje temporal y contrafactual de overlay ALEATORIO.
# Analogo temporal de la regla 2 (contrafactual aleatorio) de HALLAZGOS.md.
# No evalua ninguna regla: solo fija el liston. Ejecutable antes del pre-registro.
import numpy as np, math

RF = 0.02
D = [l.split(',') for l in open('serie_anual_c4.csv').read().splitlines()[1:]]
yr   = np.array([int(r[0])   for r in D])
slv  = np.array([float(r[3]) for r in D])/100.0   # C4 ponderado rank^2
qqq  = np.array([float(r[5]) for r in D])/100.0
n    = len(yr)

cagr = lambda r: np.prod(1+r)**(1/len(r))-1
def fisher_ci(r, m, conf=1.96):
    z = np.arctanh(r); se = 1/math.sqrt(m-3)
    return np.tanh(z-conf*se), np.tanh(z+conf*se), se

print("="*78)
print("1. RECONSTRUCCION — contraste con HALLAZGOS C3/C9")
print("="*78)
r_obs = np.corrcoef(slv, qqq)[0,1]
print(f"  CAGR C4 (rank^2)   {100*cagr(slv):6.2f}%     [HALLAZGOS C9: 14,16% base]")
print(f"  CAGR Nasdaq        {100*cagr(qqq):6.2f}%     [HALLAZGOS C9: 13,82%]")
print(f"  correlacion        {r_obs:6.3f}      [HALLAZGOS C3: 0,918]")
print(f"  vol sleeve {100*slv.std(ddof=1):.1f}%   vol qqq {100*qqq.std(ddof=1):.1f}%   n={n}")

print()
print("="*78)
print("2. POTENCIA — que se puede distinguir con n=17, y con n=8/9 tras el split")
print("="*78)
for m,lab in [(n,'serie completa'),(9,'pares (descubrimiento)'),(8,'impares (confirmacion)')]:
    lo,hi,se = fisher_ci(r_obs, m)
    print(f"  {lab:<26} n={m:2d}  IC95% de r={r_obs:.3f}: [{lo:.3f}, {hi:.3f}]  ancho={hi-lo:.3f}")
print()
print("  -> Para AFIRMAR descorrelacion hay que separar r=0,92 de un objetivo r=0,70.")
for m in (n,9,8):
    dz = abs(np.arctanh(0.918)-np.arctanh(0.70)); se_d = math.sqrt(2/(m-3))
    print(f"     n={m:2d}: |dz|={dz:.3f} vs SE(dif)={se_d:.3f}  ->  {'DETECTABLE' if dz>1.96*se_d else 'NO detectable'} (hace falta {1.96*se_d:.3f})")

print()
se_cagr = slv.std(ddof=1)/math.sqrt(n)
print(f"  SE del CAGR con n={n}: {100*se_cagr:.2f} pp   -> IC95% de ±{100*1.96*se_cagr:.1f} pp")
print(f"  Diferencia CAGR sleeve-Nasdaq observada: {100*(cagr(slv)-cagr(qqq)):+.2f} pp")
print(f"  ... es {abs(cagr(slv)-cagr(qqq))/se_cagr:.2f} SE  ->  indistinguible de cero")

print()
print("  CLAVE: la comparacion overlay-vs-base es PAREADA (mismos anhos).")
print("  Su SE la fija la vol de la DIFERENCIA, no la del nivel. Es el unico")
print("  contraste con potencia real, y coincide con la regla B4 (alfa interno).")

print()
print("="*78)
print("3. CONTRAFACTUAL DE OVERLAY ALEATORIO — el liston del azar en el eje temporal")
print("="*78)
print("  Un overlay entra/sale del mercado cada febrero. Si lo hace AL AZAR,")
print("  ¿cuanta 'descorrelacion' y cuanto 'alfa' aparecen solos?")
print()
rng = np.random.default_rng(13)
IT = 20000
print(f"  {'p(dentro)':>10} {'CAGR medio':>11} {'p5':>7} {'p95':>7} {'corr media':>11} {'p5':>7} {'p95':>7} {'%corr<0.80':>11}")
for p in (0.5, 0.6, 0.7, 0.8, 0.9):
    e = (rng.random((IT, n)) < p).astype(float)
    port = e*slv + (1-e)*RF
    cg = np.prod(1+port, axis=1)**(1/n)-1
    pm = port - port.mean(axis=1, keepdims=True)
    qm = qqq - qqq.mean()
    cr = (pm@qm)/np.sqrt((pm**2).sum(axis=1)*(qm**2).sum())
    print(f"  {p:>10.1f} {100*cg.mean():>10.2f}% {100*np.percentile(cg,5):>6.1f}% {100*np.percentile(cg,95):>6.1f}%"
          f" {cr.mean():>11.3f} {np.percentile(cr,5):>7.3f} {np.percentile(cr,95):>7.3f} {100*np.mean(cr<0.80):>10.1f}%")

print()
e = (rng.random((IT, n)) < 0.7).astype(float)
port = e*slv + (1-e)*RF
cg = np.prod(1+port, axis=1)**(1/n)-1
pm = port - port.mean(axis=1, keepdims=True); qm = qqq - qqq.mean()
cr = (pm@qm)/np.sqrt((pm**2).sum(axis=1)*(qm**2).sum())
base_c, base_q = cagr(slv), cagr(qqq)
ambas = np.mean((cr < 0.80) & (cg > base_q))
print(f"  Con p=0,7 (dentro 12 de 17 anhos), POR PURO AZAR:")
print(f"    correlacion < 0,80             : {100*np.mean(cr<0.80):.1f}% de los overlays")
print(f"    CAGR > Nasdaq ({100*base_q:.1f}%)          : {100*np.mean(cg>base_q):.1f}% de los overlays")
print(f"    LAS DOS COSAS A LA VEZ         : {100*ambas:.1f}% de los overlays")
print(f"    -> 1 de cada {1/max(ambas,1e-9):.0f} overlays aleatorios 'cumple' lo que pide el usuario.")
print()
print("  Probar ~10-20 variantes de regla de tendencia y quedarse con la mejor")
print(f"  produce un exito aparente con probabilidad ~{100*(1-(1-ambas)**15):.0f}% SIN NINGUNA SENAL.")
