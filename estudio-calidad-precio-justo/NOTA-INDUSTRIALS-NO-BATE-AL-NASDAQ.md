# Industrials baratas: el alfa interno es sólido, el externo no. Y en Sharpe pierde.

Chequeo de rigor sobre el candidato de C23, antes de construir nada encima.
Script: `rigor_industrials.py`.

## 1. Los números completos

| medida | Industrials baratas | Nasdaq | |
|---|---|---|---|
| CAGR | **15,40%** | 13,26% | +2,14 pp |
| **alfa Jensen** | **+2,86%** | — | **SE 5,97% → t = +0,48** |
| IC95% del alfa | **[−8,85%, +14,56%]** | | contiene el cero de sobra |
| beta | 1,11 (SE 0,24) | 1,00 | IC [0,65, 1,57] |
| volatilidad | **31,7%** | 22,0% | **+9,7 pp** |
| **peor año** | **−45,8%** | −32,9% | **12,9 pp peor** |
| **Sharpe (rf 2%)** | **0,423** | **0,512** | **peor que el índice** |
| años batiendo al Nasdaq | 9/17 | | casi una moneda |

**Corrección a lo que se dijo antes:** el alfa Jensen que reporté como +1,71% sale +2,86% al
calcularlo sobre Industrials aislado con su propia regresión, pero **su t es 0,48**. No está
establecido. Y donde dije "cae menos que el índice en años malos" me refería a la **media** de
los 4 años malos (−10,9% vs −12,3%); **el peor año concreto es −45,8% frente a −32,9%**, o
sea, bastante peor. Las dos cosas son ciertas y la segunda es la que importa para una cartera.

## 2. Falla el control que mató seis efectos anteriores

Leave-one-year-out sobre el alfa Jensen:

| se quita | alfa | beta |
|---|---|---|
| — (completo) | +2,86% | 1,11 |
| 2008 | +5,52% | 0,99 |
| **2022** | **−3,39%** | 1,34 |
| resto | +1,45% a +4,66% | ~1,10 |

**El signo cambia al quitar 2022.** Rango [−3,39%, +5,52%]. Es exactamente el patrón de B6:
el resultado vive en una o dos observaciones.

Y el contrafactual aleatorio (B2) con 22 nombres de Industrials da un alfa medio de +0,03% y
p95 de +3,13%. **El observado (+2,86%) queda en el percentil 93,6, p = 0,0638.** Marginal, no
significativo.

## 3. Lo que SÍ queda establecido

| medida | valor | t |
|---|---|---|
| **alfa interno (baratas − su propia familia Industrials)** | **+6,73 pp** | **+2,31** |

10 de 17 años positivos. **Esto sí aguanta**, y es lo único de toda la serie con |t| > 2.

## 4. Por qué una cosa tiene t=2,31 y la otra t=0,48

No es contradicción, es la regla B4 funcionando:

- **La comparación interna es pareada**: mismos años, mismo universo, misma exposición de
  mercado. El ruido del mercado se cancela y queda la señal. SE de 2,91 pp.
- **La comparación contra el Nasdaq no lo es**: la cartera tiene 31,7% de volatilidad y el
  índice 22,0%. Ese ruido se lo come todo. SE de 5,97 pp, el doble.

**Traducción práctica: "barato bate a caro dentro de Industrials" está demostrado. "Industrials
barato bate al Nasdaq" no lo está, y ajustando por riesgo (Sharpe 0,423 vs 0,512) lo pierde.**

## 5. Qué significa para el compartimento

No es un sustituto superior del Nasdaq. Es un **sesgo de valor dentro de Industriales** que:

- aporta +6,7 pp anuales **frente a comprar Industriales al azar** (demostrado),
- y no aporta nada demostrable **frente a comprar el Nasdaq** (t = 0,48, Sharpe peor).

Sirve para **elegir qué Industriales comprar**, no para decidir si comprar Industriales en vez
de Nasdaq. Es una herramienta de selección dentro de un sector, no una tesis de cartera.

## 6. Lo que puede cambiar el veredicto

Las dos cosas ya en marcha, y ahora con criterio afinado:

1. **Supervivencia**: el alfa interno es inmune por construcción (B4), pero el CAGR de 15,40%
   no lo es. Recuperar el sector de las bajas dirá cuánto de ese 15,40% es supervivencia.
2. **Mejor métrica de valoración**: `evToSales` y `priceToBook` en vez del P/S del panel. El
   objetivo ya no es subir el CAGR, es **subir el alfa interno y bajar la beta**. Si el alfa
   interno sube de 6,7 pp y la beta baja de 1,11, entonces sí habría una tesis de cartera.

**Criterio declarado ahora: para que esto sea una alternativa al Nasdaq y no solo un
selector, hace falta alfa Jensen con t ≥ 2 y Sharpe ≥ 0,512.** Hoy está en t = 0,48 y 0,423.
