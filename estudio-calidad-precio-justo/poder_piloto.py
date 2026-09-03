# ¿Podia el piloto haber pasado su propio umbral? Potencia del AUC.
import numpy as np, math
H=open('ciclicas_ciclo.csv').read().splitlines(); cols=H[0].split(',')
ev=[dict(zip(cols,l.split(','))) for l in H[1:]]
yrs=sorted({int(e['yr']) for e in ev})
n=len(ev)
for q,et in [(80,'quintil'),(90,'decil')]:
    na=int(round(n*(100-q)/100)); nb=n-na
    se=0.5/math.sqrt(min(na,nb)/2)   # aprox de Hanley-McNeil por mitad (pares/impares)
    print(f"  {et:<8} n cola ~{na:>4}  ({na//2} por mitad)   SE(AUC) por mitad ~ {se:.3f}   IC95% ~ +-{1.96*se:.3f}")
print()
print("  El umbral pedia |AUC-0,5| >= 0,10 replicado en AMBAS mitades.")
print("  Con SE ~0,10, un efecto real de 0,10 se observa por encima de 0,10 solo el ~50% de")
print("  las veces en cada mitad -> ~25% de que replique en las dos. **El umbral era")
print("  inalcanzable con 50 tickers, aunque la senhal existiera.** Error mio de calibracion.")
print()
print("="*84)
print("QUE HARIA FALTA — tamanho de muestra para resolver AUC 0,60")
print("="*84)
print(f"  {'tickers':>8}{'decisiones':>12}{'n cola (decil)':>16}{'SE(AUC)/mitad':>16}{'IC95%':>10}")
for tk in (50,150,300,468,705):
    dec=int(n*tk/50); na=int(dec*0.10)
    se=0.5/math.sqrt(max(na,1)/2)
    print(f"  {tk:>8}{dec:>12}{na:>16}{se:>16.3f}{1.96*se:>10.3f}")
print()
print("  Con el universo ciclico completo (468 tickers con >=8 anhos) el SE baja a ~0,03:")
print("  ahi si se distingue 0,60 de 0,50. **La pregunta es resoluble, el piloto no la resolvia.**")
