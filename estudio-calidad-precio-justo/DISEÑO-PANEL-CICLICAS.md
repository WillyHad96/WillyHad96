# Diseño del panel de cíclicas: variables que sí pueden acotar

Motivo: `hypergrowth_panel` está construido para cazar hipercrecimiento. Sus variables son de
**nivel de crecimiento**; una cíclica no se explica por su crecimiento, se explica por
**dónde está dentro de su ciclo**. El barrido de AUC lo confirma (`auc_barrido.py`).

## 1. Lo que dice el barrido del panel actual

AUC contra el decil superior de retorno, dentro de año, sector cíclico. 0,5 = nada.

| variable | pares | impares | ¿replica? |
|---|---|---|---|
| **múltiplo P/S (nivel)** | 0,449 | 0,463 | **sí** — barato predice la cola |
| **posición del P/S en su historia** | 0,451 | 0,464 | **sí** — barato vs sí misma |
| margen operativo (nivel) | 0,435 | 0,471 | signo sí — margen deprimido |
| momento 12m | 0,485 | 0,495 | **nada** |
| aceleración de ingresos | 0,510 | 0,530 | nada |
| racha de crecimiento | 0,510 | 0,517 | nada |
| sorpresa vs estimado | 0,494 | 0,556 | **no replica** |
| guía implícita | 0,481 | 0,475 | nada |
| regla 40 | 0,470 | 0,500 | **nada** |
| posición del margen op. en su ciclo | 0,483 | 0,527 | no replica |

**Ninguna llega a 0,55.** Las cuatro variables de hipercrecimiento (aceleración, racha,
sorpresa, guía) dan exactamente cero. **Lo único que asoma es valoración barata y margen
deprimido: el manual de cíclicas, insinuado y sin poder medirse bien.**

## 2. Corrección de disponibilidad de datos

`AGENDA-ESTUDIOS.md` dice: *"`period=quarter` en `statements`: el bloqueo importante"*.
**Ya no es cierto.** La cuenta está en plan **Premium** y los trimestrales funcionan.

**Verificado con NUE: 80 trimestres continuos hasta 2006-09-30.** Cubre entera la ventana
2007–2023 a frecuencia trimestral.

## 3. El cambio conceptual

El panel actual pregunta **"¿cuánto crece y cuánto margen tiene?"**. Para cíclicas hay que
preguntar **"¿dónde está esto dentro de SU propio ciclo, y sobrevive al suelo?"**.

Regla de diseño: **casi ninguna variable entra como nivel; entra como posición dentro del
rango propio de 20–40 trimestres.** Es la diferencia entre "margen del 8%" (no dice nada) y
"margen en el percentil 5 de su propia década" (dice que está en el suelo).

## 4. Las variables, por bloque y con su tesis

### A. Posición en el ciclo — ¿estamos en el suelo?

| variable | fuente | tesis |
|---|---|---|
| **`capexToDepreciation`** (y su media 8T) | key-metrics Q | **La mejor variable cíclica que existe.** <1 sostenido = el sector se está comiendo su capacidad; la escasez futura de oferta es lo que hace el siguiente ciclo |
| **`daysOfInventoryOutstanding`** vs rango propio | key-metrics Q | ciclo de inventarios: desabastecimiento terminado = suelo |
| `inventoryTurnover` vs rango propio | metrics-ratios Q | lo mismo por el otro lado |
| **`assetTurnover`, `fixedAssetTurnover`** vs rango propio | metrics-ratios Q | proxy de utilización de capacidad. Bajo = trough |
| **`returnOnCapitalEmployed`** vs rango propio | key-metrics Q | la medida más limpia de "dónde estoy en el ciclo" |
| `ebitdaMargin` vs rango propio 40T | metrics-ratios Q | margen deprimido = suelo (el panel ya lo insinúa) |

### B. Valoración de cíclica — el P/E no sirve en el suelo

| variable | fuente | tesis |
|---|---|---|
| **`priceToBookRatio`** | metrics-ratios Q | el clásico. En el suelo los beneficios tienden a cero y el P/E explota; el valor contable no |
| **`evToSales`** vs rango propio | key-metrics Q | las ventas son más estables que el beneficio |
| **EV / EBITDA de mitad de ciclo** (construida) | key-metrics Q | **la que usan los inversores de cíclicas de verdad**: EBITDA promediado sobre 20–40T, no el actual |
| `evToEBITDA` actual | key-metrics Q | control, para ver cuánto añade la versión de mitad de ciclo |

### C. Supervivencia al suelo — evitar la cola IZQUIERDA

| variable | fuente | tesis |
|---|---|---|
| **`netDebtToEBITDA`** (sobre EBITDA de mitad de ciclo) | key-metrics Q | **probablemente el filtro más importante de todos.** Una cíclica apalancada en el suelo no rebota: quiebra. Es lo que separa el +200% del −100% |
| **`interestCoverageRatio`** | metrics-ratios Q | lo mismo, más directo |
| `currentRatio`, `quickRatio` | metrics-ratios Q | liquidez para aguantar el trough |
| `debtToEquityRatio` | metrics-ratios Q | |

### D. Apalancamiento operativo — el amplificador

| variable | fuente | tesis |
|---|---|---|
| **beta de margen** (construida): pendiente de `ebitdaMargin` sobre `revenue` en 20T | derivada | mide cuánto amplifica cada punto de ventas. **Es lo que convierte una recuperación en un x3** |
| `salesGeneralAndAdministrativeToRevenue` | key-metrics Q | proxy de estructura fija |

### E. Confirmación del giro — ¿ya pasó el suelo?

| variable | fuente | tesis |
|---|---|---|
| **Δ de `returnOnCapitalEmployed`** (2 y 4 trimestres) | derivada | primera derivada girando: el suelo ya pasó |
| **Δ de `daysOfInventoryOutstanding`** | derivada | inventarios cayendo = demanda volviendo |
| revisiones de analistas | `analyst/historical-grades` (mensual) | no está en el panel; es la variable clásica de cola alta |
| **compras de insiders** | `insiderTrades` (trimestral desde 1997) | management comprando en el suelo. Clásico y disponible |

## 5. La hipótesis central, escrita para poder fallar

**La cola alta cíclica no la produce ninguna variable sola, sino una interacción de tres:**

> **suelo del ciclo** (capex/depreciación bajo, ROCE en el percentil bajo de su historia)
> **+ valoración de suelo** (P/B bajo, EV/EBITDA de mitad de ciclo bajo)
> **+ balance que sobrevive** (netDebt/EBITDA de mitad de ciclo bajo)

Las dos primeras dan el x3; la tercera evita el −100%. Por eso ninguna univariante ha
llegado a 0,55: **el efecto, si existe, es de interacción**, y el barrido univariante no
puede verlo.

## 6. Plan de trabajo — piloto antes de construir

No tiene sentido bajar 705 tickers × 4 endpoints (~2.800 llamadas) antes de saber si hay
señal. Secuencia:

1. **Piloto (~80 tickers cíclicos, muestra aleatoria de los 705).** Bajar key-metrics y
   metrics-ratios trimestrales 2006–2024. ~160 llamadas.
2. **Medir AUC** de cada variable del bloque A–E, y de la interacción de §5, contra el decil
   superior. Pares/impares desde el principio.
3. **Umbral de continuación, declarado ahora: AUC ≥ 0,60 replicado en ambas mitades**, en
   alguna variable o en la interacción. Nada del panel actual pasa de 0,57.
4. Solo si pasa: construir la tabla completa `ciclicas_panel` en Supabase con los 705
   tickers, con el script de descarga masiva (la clave de FMP como variable de entorno; vía
   MCP es inviable por volumen).
5. Solo entonces: filtros, cartera, pre-registro, confirmación.

## 7. Lo que hay que llevar puesto

- **Sigue siendo un universo sin muertes antes de 2015** (A1). El bloque C (supervivencia)
  es precisamente el que menos se puede validar con este panel, porque **las que quebraron no
  están**. Esto no lo arregla FMP trimestral: exige delistings o un universo point-in-time.
- **El criterio de la cola es el correcto** (C15–C17): el 87% del retorno está en el decil
  superior y concentrar sin poder predecirlo es lotería. Sin AUC ≥ 0,60 no hay estrategia,
  solo dispersión.
- **`sector` solo cubre el 27% del panel** (A3). El universo cíclico real es mayor que los
  705 tickers identificados.
