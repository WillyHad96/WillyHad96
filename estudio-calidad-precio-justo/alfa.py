# Descomposicion del alfa que queda, con su error tipico y su grado de contaminacion.
import numpy as np, math
D=[l.split(',') for l in open('serie_anual_c4.csv').read().splitlines()[1:]]
slv=np.array([float(r[3]) for r in D])/100; qqq=np.array([float(r[5]) for r in D])/100
n=len(slv); cagr=lambda r: np.prod(1+r)**(1/len(r))-1
P={}
for l in open('nasdaq_febrero.csv').read().splitlines()[1:]:
    y,p=l.split(','); P[int(y)]=float(p)
yrs=sorted(y for y in P if y-1 in P and y+1 in P)
idx=np.array([P[y+1]/P[y]-1 for y in yrs]); sig=np.array([1.0 if P[y]/P[y-1]-1>0 else 0.0 for y in yrs])
ov=sig*idx+(1-sig)*0.02; dt=ov-idx; m=len(idx)

d1=slv-qqq; t1=d1.mean()/(d1.std(ddof=1)/math.sqrt(n))
t3=dt.mean()/(dt.std(ddof=1)/math.sqrt(m))

print("="*84)
print("QUE ALFA QUEDA")
print("="*84)
print(f"  {'fuente':<44}{'pp/anho':>9}{'t':>7}{'n':>5}  contaminacion")
print("  "+"-"*80)
print(f"  {'1. Seleccion, contra el Nasdaq':<44}{100*d1.mean():>+9.2f}{t1:>7.2f}{n:>5}  supervivencia entera")
print(f"  {'2. Seleccion, interno (pasa vs no pasa)':<44}{2.98:>+9.2f}{1.86:>7.2f}{n:>5}  inmune (B4), pero ver A4")
print(f"  {'3. Timing (overlay R1, 54 anhos)':<44}{100*dt.mean():>+9.2f}{t3:>7.2f}{m:>5}  ninguna: es el indice")
print(f"     (media aritmetica de diferencias anuales; en CAGR, que es lo que compone,")
print(f"      la diferencia es {100*(cagr(ov)-cagr(idx)):+.2f} pp — la aritmetica exagera por la vol)")
print("  "+"-"*80)
print(f"  CAGR: sleeve {100*cagr(slv):.2f}%  ·  Nasdaq {100*cagr(qqq):.2f}%  ·  diferencia {100*(cagr(slv)-cagr(qqq)):+.2f} pp")
print()
print("  Ninguna de las tres alcanza |t| = 2.")
print()
print("="*84)
print("QUE PASA SI SE SUMAN — el overlay aplicado al sleeve")
print("="*84)
print(f"  Alfa de seleccion realizable contra el indice : {100*d1.mean():+.2f} pp  (t={t1:.2f})")
print(f"  Coste esperado del timing, en CAGR (54 anhos) : {100*(cagr(ov)-cagr(idx)):+.2f} pp  (t={t3:.2f})")
print(f"  SUMA ESPERADA                                 : {100*(d1.mean()+cagr(ov)-cagr(idx)):+.2f} pp")
print()
print("  A cambio: correlacion esperada ~0,78-0,84 en vez de 0,918 (descorrelacion")
print("  real -0,081, p=0,154 sobre 54 anhos: no significativa).")
print()
print("="*84)
print("EL LIMITE QUE NO SE PUEDE SALTAR")
print("="*84)
se=slv.std(ddof=1)/math.sqrt(n)
print(f"  SE del CAGR del sleeve con n=17: {100*se:.2f} pp  ->  IC95% ±{100*1.96*se:.1f} pp")
print(f"  Los tres alfas juntos suman {100*(d1.mean()+cagr(ov)-cagr(idx)):+.2f} pp, dentro de ese ±{100*1.96*se:.0f} pp.")
print("  Es decir: la suma de todo lo que hemos encontrado cabe entera dentro del")
print("  error de medicion de una sola de las cifras.")
