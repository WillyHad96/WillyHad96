# Recuperar alfa después de la corrección: la regla del 40

Partimos del escenario C corregido (sin el filtro look-ahead de sector, con las empresas
desaparecidas dentro): **11,90% de CAGR frente a 13,16% del NASDAQ**. Es decir, tras corregir el
sesgo ya **no** batíamos al NASDAQ: le perdíamos por 0,85 pp.

Este documento encuentra 3 puntos. Y de paso desmonta la premisa de partida.

---

## 1. Primero: los delistings no son lo que parecen

Desenlace de las 1.315 empresas del panel que desaparecen entre 2007 y 2026, medido por lo que
hace su precio en su último año de vida:

| Desenlace | Empresas | % |
|---|---|---|
| **A. Sube más del 20%** (compra probable) | 416 | **31,6%** |
| B. Sube 0–20% | 226 | 17,2% |
| C. Baja 0–30% | 343 | 26,1% |
| D. Baja 30–60% | 141 | 10,7% |
| **E. Baja más del 60%** (fracaso probable) | 189 | **14,4%** |

**Casi la mitad (48,8%) acaba plana o al alza.** Sólo una de cada cuatro acaba mal. Entre las
seleccionadas por la estrategia, las que mueren rinden **+8,64%** frente a +14,79% de las
supervivientes: un lastre, no un desastre.

**Conclusión incómoda para el planteamiento inicial: "evitar delistings" no es el objetivo
correcto.** La mayoría son adquisiciones, y a una adquisición no quieres esquivarla.

---

## 2. Qué se puede saber en el momento de comprar

Probé seis factores del panel, todos disponibles en la fecha de selección, partiendo cada uno en
cuartiles. Retorno a 12 meses de las seleccionadas (escenario C):

| Factor | Cuartil 1 | Cuartil 2 | Cuartil 3 | Cuartil 4 | ¿Sirve? |
|---|---|---|---|---|---|
| **Regla del 40** (mediana) | **3,2%** | 10,5% | 10,5% | 6,3% | **sí, Q1 es malo** |
| Regla del 40 (mortalidad) | **4,1%** | 2,1% | 1,2% | 1,3% | |
| **Capitalización** (mediana) | **2,4%** | 14,4% | 8,7% | 6,0% | **sí, Q1 es malo** |
| Capitalización (mortalidad) | **4,6%** | 2,5% | 0,8% | 0,8% | |
| Delta margen operativo (media) | 10,7% | 12,6% | 16,8% | 19,1% | débil |
| Margen operativo (mediana) | 8,1% | 7,2% | 15,3% | 6,3% | no monótono |
| Múltiplo P/S (mediana) | 12,2% | 3,9% | 6,3% | 8,5% | forma de U |
| **Dilución** (mediana) | 11,9% | 5,6% | 9,6% | 6,3% | **no sirve** |

Que la dilución no sirva es contraintuitivo — emitir acciones se lee como señal de apuro — pero
en estos datos no separa nada.

Los dos que sí funcionan tienen el cuartil bajo peor **en las cuatro métricas a la vez**: peor
media, peor mediana, más catástrofes y más mortalidad.

### Qué es exactamente la regla del 40

Verificado en el panel: `regla40 = crecimiento + margen_operativo`, exacto (correlación 1,0000,
el 100% de las filas idénticas). El percentil 25 está en **0,025**.

Traducido: **el filtro descarta a las empresas cuya suma de crecimiento y margen operativo no
llega al 2,5%.** O sea, las que ni crecen ni ganan dinero. Es un filtro de viabilidad, y se
entiende sin estadística.

---

## 3. Los resultados

Umbrales calculados **por año** sobre el universo elegible, sin look-ahead. Ponderación `rank²`.

| Configuración | CAGR | S&P 500 | NASDAQ | **vs NASDAQ** | n | Mortalidad |
|---|---|---|---|---|---|---|
| C0. Escenario C corregido | 12,31% | 7,50% | 13,16% | **−0,85** | 57 | 1,79% |
| C1. + regla del 40 > p25 | 14,64% | 7,45% | 13,17% | +1,46 | 46 | 1,16% |
| C2. + capitalización > p25 | 13,26% | 7,20% | 12,99% | +0,27 | 45 | 1,27% |
| C3. + delta margen op > p25 | 12,89% | 7,63% | 13,18% | −0,29 | 48 | 1,71% |
| **C4. + regla 40 Y capitalización** | **15,42%** | 7,17% | 13,07% | **+2,35** | 38 | **0,75%** |
| C5. + los tres | 15,33% | 7,49% | 13,28% | +2,05 | 34 | 0,69% |

**C4 recupera 3,11 pp y vuelve a batir al NASDAQ.** Y reduce la mortalidad a menos de la mitad.

---

## 4. ¿Es real? Permutación

Sustituyo el filtro por uno **aleatorio del mismo tamaño** (se queda con el 56,25% al azar cada
año) y repito 400 veces:

| | Valor |
|---|---|
| CAGR medio con filtro aleatorio | 11,60% |
| Desviación típica | 1,23 pp |
| Percentil 95 | 13,63% |
| **Máximo en 400 simulaciones** | **14,87%** |
| **Observado con regla 40 + capitalización** | **15,42%** |
| **p** | **< 0,0025** |

Ninguna de las 400 simulaciones llegó al 15,42%. El filtro lleva información real: está a 3,1
desviaciones típicas. Incluso corrigiendo por las ~15 combinaciones que probé, p ≈ 0,04.

---

## 5. Pero la partición temporal recorta la euforia

| Configuración | 2007–2015 | NASDAQ | vs | 2016–2023 | NASDAQ | vs |
|---|---|---|---|---|---|---|
| **Pasa el filtro C4** | 7,52% | 9,20% | **−1,68** | 25,01% | 17,59% | **+7,42** |
| No pasa el filtro | 0,95% | 10,32% | −9,36 | 10,78% | 16,28% | −5,50 |

Dos lecturas, y hay que separarlas:

- **El filtro funciona en las dos mitades.** Pasar el filtro es mejor que no pasarlo por 7,7 pp
  en la primera mitad y por 12,9 pp en la segunda. Eso es sólido.
- **Batir al NASDAQ NO funciona en las dos mitades.** En 2007–2015 le perdemos por 1,68 pp. El
  +2,35 pp agregado viene **entero** de 2016–2023.

Ese segundo punto es el que hay que tener presente antes de emocionarse.

---

## 6. Y el filtro no funciona por esquivar delistings

Esto contradice la premisa con la que empezamos. La mortalidad baja del 1,79% al 0,75%, o sea
**1,04 puntos porcentuales de nombres al año**. Y las que mueren rinden +8,64% frente a +14,79%
de las supervivientes, un diferencial de ~6 pp.

Aportación de esquivar muertes al resultado: **1,04% × 6 pp ≈ 0,06 pp.**

La ganancia total del filtro es de **3,11 pp**. O sea que **evitar delistings explica menos del
2% de la mejora.** El resto es simplemente que "crecimiento + margen operativo" predice
retornos.

**La regla del 40 no es un detector de quiebras. Es un filtro de calidad, y funciona como tal.**

---

## 7. La configuración final y qué esperar de verdad

```
UNIVERSO   Bolsa estadounidense, capitalización 300 M$ – 5.000 M$
           Ingresos TTM ≥ 10 M$, precio ≥ 1 $
           SIN filtro de sector  (era look-ahead: excluía al 99,7% de las desaparecidas)

FILTROS    · Desviación típica del margen bruto en 8 trimestres < mediana del año
           · Desviación típica del crecimiento en 8 trimestres  < mediana del año
           · NUEVO: crecimiento + margen operativo > percentil 25 del año  (≈2,5%)
           · NUEVO: capitalización > percentil 25 del año dentro de la banda

SELECCIÓN  Top 20% por subida del precio en 12 meses   → ~38 nombres
PESOS      Proporcional al CUADRADO del puesto por momentum
VENTA      Todo a los 12 meses
```

### Expectativa honesta

| | vs S&P 500 | vs NASDAQ |
|---|---|---|
| Medido (2007–2023) | +8,25 pp | +2,35 pp |
| Descontando el sesgo de febrero (×0,74) | +6,11 | +1,74 |
| Descontando dividendos | −0,80 → **+5,31** | +0,50 → **+2,24** |
| Descontando comisiones a 20.000 € | **≈ +4,9 pp** | **≈ +1,8 pp** |

Frente al S&P 500 la ventaja es sólida y aparece en las dos mitades de la muestra. **Frente al
NASDAQ es de menos de dos puntos y sólo aparece en la segunda mitad.** Igualarlo sí; superarlo
de forma fiable, no está demostrado.

---

## 8. Lo que queda pendiente

1. **Recuperar el sector de las desaparecidas vía FMP** (`profile-symbol` funciona para tickers
   estadounidenses delistados) y poder así excluir Financials e inmobiliarias también entre los
   muertos. Ahora mismo el escenario C las incluye y la estrategia original no.
2. **Precio real de delisting** para las que mueren dentro del año, en vez del último precio del
   panel. Son ~15 eventos en la configuración C4, pero es el supuesto más frágil.
3. **Rehacer los documentos anteriores** sin el filtro de sector.
4. Revisar si hay más campos con enriquecimiento retroactivo, como lo tuvo `sector`.
