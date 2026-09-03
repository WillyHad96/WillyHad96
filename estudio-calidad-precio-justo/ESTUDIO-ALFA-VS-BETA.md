# CAGR y correlación no están atados: lo que los ata es la beta

Pregunta del usuario: los cuatro subtipos ordenan igual por CAGR y por correlación, y eso
"no debería pasar". Tiene razón en que es incómodo, y el porqué cambia qué hay que buscar.
Scripts: `desacople.py`, `barato_por_subtipo.py`.

## 1. La proporcionalidad es aritmética de mercado alcista

CAGR ≈ rf + β·(prima de mercado) + α, y β = correlación × volatilidad relativa. En 17 años
con el Nasdaq al +14,29% anual, **más correlación = más beta = más CAGR**, sin que haya
ninguna habilidad de por medio.

Sobre las 6 carteras medidas:

- **corr(CAGR, correlación con el Nasdaq) = +0,704** ← lo que se ve a simple vista
- **corr(ALFA, correlación con el Nasdaq) = +0,195** ← lo que importa

**El ranking de CAGR es beta, no habilidad. El alfa no está atado a la correlación**, así que
sí se puede buscar alfa a correlación baja. Lo que no se puede es buscar CAGR bruto a
correlación baja, porque el CAGR bruto *es* mayormente beta.

Y se invierte en años malos, como debe ser si es beta: en los 4 años en que el Nasdaq cayó,
Consumer Cyclical (β 1,35) hizo **−19,2%** y Industrials (β 0,80) **−10,4%**, frente al
−12,3% del Nasdaq. **El subtipo con más CAGR es el peor cuando el mercado cae.**

## 2. Corrección a C21

`ESTUDIO-SUBTIPOS-CICLICOS.md` reportó el cuartil barato de **Industrials + Basic Materials**
con +6,76 pp de alfa interno y t = 2,38. Eso sigue siendo cierto **frente a su propio pool**.
Pero descompuesto contra el mercado:

| cartera | CAGR | corr | **beta** | **alfa Jensen** | vol |
|---|---|---|---|---|---|
| BARATAS Indu+Basi (C21) | 17,79% | 0,790 | **1,46** | **+0,87%** | 41,7% |

**Su alfa Jensen es solo +0,87%, y su beta 1,46.** Casi todo el 17,79% era beta. C21 estaba
mezclando dos cosas distintas, y separarlas mejora el hallazgo.

## 3. Separado por subtipo: el efecto valor es un efecto de INDUSTRIALS

Cuartil barato **dentro de cada subtipo**:

| cartera | n/año | CAGR | corr | **beta** | **ALFA** | vol | años malos | alfa pares | impares |
|---|---|---|---|---|---|---|---|---|---|
| Consumer Cyclical | 57 | 15,64% | 0,925 | 1,35 | −1,47% | 33,0% | −19,2% | | |
| → baratas | 14 | 13,46% | 0,909 | 1,72 | **−5,62%** | 42,8% | −28,3% | +1,2 | +1,1 |
| **Industrials** | 89 | 10,95% | 0,849 | **0,80** | −0,60% | 21,4% | **−10,4%** | | |
| **→ BARATAS** | **22** | **15,40%** | **0,792** | **1,11** | **+1,71%** | 31,7% | **−10,9%** | **+8,1** | **+5,5** |
| Basic Materials | 42 | 10,00% | 0,764 | 1,29 | −5,50% | 38,1% | −14,6% | | |
| → baratas | 10 | **20,99%** | 0,731 | **2,38** | −1,72% | **73,5%** | −15,8% | +17,3 | +21,5 |
| Energy | 32 | 5,71% | 0,529 | 0,81 | −2,13% | 34,8% | −14,2% | | |
| → baratas | 8 | 4,57% | 0,534 | 1,00 | −3,38% | 42,1% | −15,0% | +6,4 | **−3,1** |
| Nasdaq | | 14,29% | 1,000 | 1,00 | 0,00% | 22,6% | −12,3% | | |

**Industrials baratas es la única cartera de todo el estudio con alfa Jensen positivo.**

- CAGR **15,40%** frente al 14,29% del Nasdaq
- **Beta 1,11** — no es una apuesta apalancada
- **Alfa +1,71%**, el único positivo de la tabla
- En los años malos del Nasdaq: **−10,9% frente a −12,3%** — cae menos que el índice
- El alfa replica: **+8,1 pp en pares, +5,5 pp en impares**

Y los contrastes enseñan más que el propio hallazgo:

- **Basic Materials baratas es la trampa exacta que preocupaba al usuario**: CAGR **20,99%**,
  el más alto de la tabla, con **beta 2,38 y volatilidad 73,5%**. Alfa **−1,72%**. Es el
  Nasdaq apalancado ×2,4, no una estrategia.
- **En Consumer Cyclical, barato NO funciona**: alfa −5,62%, el peor de la tabla. Ahí la
  trampa de valor sí muerde.
- **En Energy no replica**: +6,4 pp en pares, −3,1 pp en impares.

## 4. La respuesta a "¿cómo desacoplamos?"

**Dejando de mirar el CAGR y mirando el alfa a beta controlada.** El CAGR bruto ordena por
beta; el alfa no. Concretamente:

1. **La métrica de selección debe ser alfa Jensen, no CAGR.** Si no, se elige siempre lo de
   más beta, que es lo que estaba pasando al mirar Consumer Cyclical y Basic Materials.
2. **Y hay que exigir beta ≤ ~1,2.** Basic Materials baratas tiene el mejor CAGR de la tabla
   y es la peor idea: 73,5% de volatilidad para un alfa negativo.
3. **El candidato real es Industrials baratas**, no Indu+Basi: menos CAGR que la mezcla
   (15,40 vs 17,79) pero **alfa positivo en vez de nulo, beta 1,11 en vez de 1,46, y
   volatilidad 31,7% en vez de 41,7%**.

## 5. Lo que sigue sin resolverse

**El alfa tampoco es un diversificador limpio.** La serie del alfa de C21 (baratas menos su
familia) correlaciona **+0,641** con el Nasdaq y tiene beta +0,498. Paga sobre todo cuando el
mercado sube. Los años sueltos son mejores que la media (2022: alfa +11 con el Nasdaq −18),
pero el conjunto no es neutral al mercado.

Así que sigue en pie: **esto resuelve rentabilidad ajustada por riesgo, no diversificación.**
La diversificación de verdad, si existe, está en Energy (correlación 0,529) — pero ahí el
efecto valor no replica y el CAGR es 5,71%.
