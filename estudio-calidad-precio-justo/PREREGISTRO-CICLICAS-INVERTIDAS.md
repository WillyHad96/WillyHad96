# Pre-registro — Invertir los filtros que estaban quitando las cíclicas

**Escrito y comiteado ANTES de mirar los años impares.** Regla 1 de método. 2026-09-02.

## 1. De dónde sale

C2 estableció que los filtros de C4 seleccionan a los miembros **menos** cíclicos de los
sectores cíclicos (sd del margen 1,41 pp los que pasan, 4,76 pp los que fallan). C5 probó
**quitar** el filtro de estabilidad y no funcionó (real −0,07, CAGR 10,97%). **Nadie ha
probado invertirlo**, ni ha medido qué rinde el lado que cada filtro descarta.

## 2. El cribado de descubrimiento (años PARES 2008–2022, 8 años, 1.830 eventos)

`criba_ciclicas.py`. Nasdaq en esos años: 8,60%.

| variante | n/año | CAGR | corr | azar | real | vs QQQ |
|---|---|---|---|---|---|---|
| todas las cíclicas | 229 | 10,99% | 0,888 | 0,888 | +0,000 | +2,38 |
| estabilidad pasa | 91 | 11,67% | 0,851 | 0,883 | −0,032 | +3,07 |
| estabilidad invertida | 63 | 8,31% | 0,810 | 0,875 | −0,065 | −0,30 |
| r40 pasa / falla | 170/59 | 10,57/9,66% | | | +0,006/−0,016 | +1,96/+1,06 |
| **mcap pasa** | 182 | **9,38%** | 0,877 | 0,886 | −0,009 | +0,77 |
| **mcap FALLA (<p25)** | 46 | **16,16%** | 0,817 | 0,871 | −0,055 | **+7,56** |
| C4 cíclicas completo | 12 | 10,81% | 0,814 | 0,818 | −0,003 | +2,21 |
| **estab invertida + mom20, sin r40/mc** | 12 | **13,13%** | 0,675 | 0,818 | **−0,142** | **+4,53** |

**Se cribaron 13 variantes.** Con 13 pruebas, que la mejor luzca bien es lo esperable. Por eso
esto es descubrimiento y nada más.

## 3. Las reglas, cerradas y sin parámetros libres

Universo: los 4 sectores cíclicos (Consumer Cyclical, Industrials, Basic Materials, Energy),
banda 300 M$–5.000 M$, guardas de `consultas.sql` intactas. Percentiles calculados sobre el
universo completo del año, como en `c4_base.sql`. Pesos rank² por momento. Venta a 12 meses.

- **R-A — capitalización invertida.** `pr_mc <= 0,25` (el cuartil MÁS pequeño), más
  `pr_mb<0,5`, `pr_cr<0,5`, `pr_r40>0,25`, top 20% por momento.
- **R-B — estabilidad invertida.** `pr_mb > 0,5` **y** `pr_cr > 0,5` (los MÁS inestables),
  **sin** filtro de r40 ni de capitalización, top 20% por momento.
- **R-C — las dos juntas.** `pr_mb>0,5`, `pr_cr>0,5`, `pr_mc<=0,25`, top 20% por momento.
  **No cribada en descubrimiento**: se pre-registra a ciegas, que es más limpio.

Umbrales heredados de C4 (0,5 y 0,25) y del cribado. **No se ajusta nada en confirmación.**

## 4. Contraste

Null de B2 trasladado tal cual: **carteras aleatorias del mismo número de nombres, del mismo
pool cíclico, año a año.** 4.000 simulaciones, semilla 13.

- `p(CAGR)` = fracción de carteras aleatorias con CAGR ≥ el observado.
- `p(corr)` = fracción con correlación ≤ la observada.
- `p_conjunta` = fracción que cumple las dos.

## 5. Criterio de éxito, declarado por adelantado

Sobre los años **IMPARES** (2007–2023, 9 años), una regla sobrevive solo si cumple las tres:

1. `p_conjunta < 0,0167` (Bonferroni: 0,05 / 3 reglas).
2. CAGR ≥ el del Nasdaq en esos mismos años impares.
3. Descorrelación real < 0 (correlación observada por debajo del azar a igual tamaño).

Cualquier otro resultado se reporta como **no distinguible del ruido**, por bonito que sea el
número de descubrimiento.

## 6. Límite de potencia, reconocido antes de mirar

- La confirmación son **9 años**. B6 midió el SE del CAGR en 5,85 pp con 17 años; con 9 es
  peor todavía. **Un CAGR de confirmación no puede establecer nada por sí solo.**
- B8 midió que una ventana puede fabricar descorrelación de −0,40 a +0,10 por sí sola. Con 9
  años el riesgo de ventana es mayor, no menor.
- Por eso el criterio se apoya en la `p_conjunta` contra el azar a igual tamaño, que es lo
  único que controla las dos cosas a la vez, y aun así **el resultado será un indicio, no un
  efecto establecido.**

## 7. Qué falsaría la hipótesis

Que las tres reglas queden por encima de 0,0167 — es decir, que invertir los filtros no
aporte nada sobre elegir al azar el mismo número de nombres del mismo pool cíclico.

## 8. Aviso de implementabilidad, anotado ya

R-A y R-C seleccionan el cuartil más pequeño de la banda (≈300–700 M$). **Nunca se ha
aplicado un filtro de liquidez** (`METODOLOGIA-Y-PENDIENTES.md`, Factor 8). Con ~500 €/posición
el impacto de mercado es probablemente irrelevante, pero **no está medido**, y no debe darse
por bueno sin medirlo.
