# Estudio 2: ninguna métrica de FMP mejora al P/S del panel

Objetivo declarado en `NOTA-INDUSTRIALS-NO-BATE-AL-NASDAQ.md` §6: **subir el alfa interno y
bajar la beta de 1,11**, que es lo único que podría cruzar el listón (alfa Jensen t ≥ 2 y
Sharpe ≥ 0,512). Script: `estudio2_valoracion.py`.

## 1. Los datos

60 tickers de Industrials con `key-metrics` trimestral de FMP (de 99 con ≥8 años de panel),
**772 decisiones**, 2007–2023, 45/año. Mismo desfase anti-look-ahead que el piloto: último
trimestre cerrado antes del 15 de noviembre del año anterior.

Métricas comparadas, todas como cuartil más barato dentro de Industrials:

## 2. El resultado

| métrica | CAGR | corr | **beta** | alfa Jensen | **alfa interno** | **t** | pares | impares |
|---|---|---|---|---|---|---|---|---|
| **P/S del panel (base)** | **16,55%** | 0,761 | **0,99** | **4,96%** | **7,31 pp** | **2,17** | **+7,9** | **+6,8** |
| EV/ventas | 13,25% | 0,782 | 0,96 | 1,70% | 3,74 | 1,09 | +6,5 | +1,3 |
| EV/EBITDA | 12,35% | 0,779 | 0,86 | 1,65% | 2,34 | 0,76 | −0,6 | +5,0 |
| P/valor tangible | 9,15% | 0,761 | 0,91 | −1,50% | **0,12** | 0,04 | −4,2 | +4,0 |
| earnings yield | 11,86% | 0,657 | 0,72 | 3,03% | 1,94 | 0,58 | −3,9 | +7,1 |
| **FCF yield** | 14,36% | 0,724 | **0,72** | **5,14%** | 4,07 | 1,54 | **−1,5** | **+9,0** |
| familia Industrials | 10,75% | 0,804 | 0,69 | | | | | |
| Nasdaq | 12,69% | 1,000 | 1,00 | | | | | |

## 3. Veredicto: el objetivo no se cumple

**Ninguna métrica de FMP sube el alfa interno.** El P/S del panel da **7,31 pp con t = 2,17**
y es la única que **replica en las dos mitades** (+7,9 / +6,8). Todas las demás quedan por
debajo, y ninguna replica.

**Y mi hipótesis queda refutada.** El diseño argumentaba que para cíclicas hay que usar EV
(incluye la deuda) y P/B (no explota cuando el beneficio se va a cero en el suelo). Los datos
dicen lo contrario:

- **EV/ventas rinde peor que P/S** (3,74 vs 7,31 de alfa interno) pese a ser teóricamente
  superior. Añadir la deuda al numerador **empeora** la señal aquí.
- **P/valor tangible da 0,12 pp de alfa interno**, t = 0,04. **Literalmente nada.** Era la
  métrica que la teoría de cíclicas pone en primer lugar.

## 4. La trampa que el split evitó

**FCF yield es el caso de libro.** Tiene el mejor alfa Jensen de la tabla (**5,14%**) y la
beta más baja (**0,72**): exactamente lo que el objetivo pedía. Si me quedo ahí, es el
hallazgo del día.

Pero su alfa interno es **−1,5 pp en años pares y +9,0 pp en impares**. **No replica.** El
número agregado (4,07, t = 1,54) es el promedio de dos mitades que dicen cosas opuestas.

Lo mismo con *earnings yield* (−3,9 / +7,1) y con P/valor tangible (−4,2 / +4,0). **Tres de
las seis métricas habrían pasado por buenas mirando solo el agregado.**

## 5. Qué queda

El candidato sigue siendo **el mismo de antes y con la misma métrica**: cuartil más barato
por **P/S dentro de Industrials**. No se ha conseguido ni subir el alfa ni bajar la beta.

Sigue sin cruzar el listón declarado: el alfa Jensen aquí sale 4,96%, pero sobre 17
observaciones su error típico ronda los 5–6 pp, así que **el t sigue por debajo de 2**. Lo
único con t > 2 continúa siendo el **alfa interno**, que es un selector, no una tesis de
cartera (C24).

## 6. Nota de alcance

60 de los 99 Industrials con historia suficiente. La muestra cubre 772 decisiones y 17 años,
pero **no es el universo completo**, y las cifras absolutas siguen sin corregir por
supervivencia (C25 estimó ~5 pp de inflación en el nivel).
