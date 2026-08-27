# Qué estamos midiendo realmente, y qué falta

Tu pregunta tiene dos respuestas distintas: **lo que está en la tabla y no habíamos usado** (poco,
y contaminado) y **lo que no está** (mucho, y ahora sí se puede traer).

---

## 1. Los 21 campos, y su cobertura real

Sobre el universo relevante (EEUU, 300 M$–5.000 M$, 2007–2024, 147.138 filas):

| Campo | Qué mide | Cobertura |
|---|---|---|
| `ingresos`, `ingresos_ttm` | Ventas del trimestre y TTM | 100% |
| `margen_bruto` | Margen bruto | 100% |
| `margen_operativo` | Margen operativo | 100% |
| `multiplo_ps` | Precio / ventas | 100% |
| `reinversion` | Reinversión sobre ventas | 100% |
| `racha` | Trimestres consecutivos acelerando | 100% |
| `precio_post` | Precio en la fecha de resultados | 100% |
| `crecimiento`, `regla40` | Crecimiento YoY; crecimiento + margen op. | 98,3% |
| `delta_margen_op` | Variación del margen operativo | 98,1% |
| `dilucion_yoy` | Emisión de acciones YoY | 98,0% |
| `aceleracion_pp` | Aceleración del crecimiento en pp | 96,8% |
| `magnitud_rel` | Tamaño del trimestre vs histórico | 93,0% |
| `precio_pre`, `reaccion` | Precio antes de resultados y reacción | **85,1%** |
| `guia_implicita`, `desaceleracion_guia` | Guía implícita y su deterioro | **57,0%** |
| `sorpresa` | Sorpresa frente a lo esperado | **37,6%** |
| `sector` | Sector | **36,9%** |

**Las métricas específicas de hipercrecimiento son justo las peor cubiertas.** La sorpresa de
resultados —la señal clásica de este tipo de estrategias— sólo existe en poco más de un tercio de
las filas.

---

## 2. Por qué esto acabó en cíclicas: el campo `grupo` lo explica

Nunca habíamos mirado `grupo`. Contiene el diseño original del panel:

| Grupo | Filas | Empresas |
|---|---|---|
| `W_completo` | 272.999 | 4.805 |
| `U_universo` | 132.255 | 1.808 |
| `E_antigua` | 684 | **7** |
| `A_sin_vuelta` | 500 | **10** |
| `C_barato` | 473 | **7** |
| `B_segunda_curva` | 466 | **8** |
| `D_unidades` | 328 | **7** |
| `G_otros` | 295 | **6** |
| `F_ciclico` | 263 | **4** |
| `H_control` | 155 | **3** |

El panel nació como un **estudio de casos**: ~52 empresas escogidas a mano y clasificadas en
categorías narrativas ("sin vuelta atrás", "segunda curva", "barato", "cíclico", "control"). El
universo amplio de 4.805 empresas se añadió después, encima.

Las métricas se diseñaron para **describir esas 52 historias**, no para cribar 6.700
observaciones estadísticamente. De ahí que aceleración, racha, sorpresa y guía implícita tengan
sentido narrativo pero cobertura pobre.

### Y la deriva es mecánica, no accidental

Nuestro filtro central selecciona **baja desviación típica del crecimiento y del margen bruto**.
En un panel construido alrededor del hipercrecimiento, "crecimiento poco variable" selecciona
**exactamente el extremo contrario** al que el panel perseguía: lo aburrido y regular.

Súmale la banda de 300 M$–5.000 M$ y que no exigimos rentabilidad, y el resultado sólo puede ser
industriales y cíclicas. **No nos desviamos del objetivo: el filtro invierte el objetivo.**

---

## 3. Probé los campos que no habíamos usado. No sobreviven

Ocho factores nunca testados, por cuartiles, sobre la configuración C4:

| Factor | Q1 | Q2 | Q3 | Q4 | Q4−Q1 |
|---|---|---|---|---|---|
| **desaceleracion_guia** | **26,5%** | 19,4% | 12,1% | 11,8% | **−14,6** |
| racha | 8,7% | 19,8% | 17,5% | 20,5% | +11,8 |
| reinversion | 17,8% | 9,2% | 14,1% | 25,8% | +8,0 (forma de U) |
| sorpresa | 12,8% | 20,8% | 10,5% | 18,8% | +6,0 (no monótono) |
| guia_implicita | 22,7% | 19,8% | 10,1% | 17,2% | −5,5 |
| reaccion al resultado | 14,4% | 22,8% | 17,3% | 12,0% | −2,4 |
| aceleracion_pp | 16,7% | 15,1% | 21,1% | 14,3% | −2,4 (n=162) |
| magnitud_rel | 15,4% | 11,0% | 21,8% | 14,8% | −0,6 |

`desaceleracion_guia` salía monótona en los cuatro cuartiles y con la mediana acompañando
(17,1% → 8,3%). Parecía el mejor hallazgo del día.

### El control lo desmonta

| Escenario | CAGR | vs NASDAQ | 2007–15 | 2016–23 | n |
|---|---|---|---|---|---|
| C4 (base) | 15,42% | +2,35 | −1,68 | +7,42 | 38 |
| C7 = C4 + racha > p25 | 16,72% | +3,35 | −0,50 | +8,17 | 33 |
| **C8 = C4 sólo exigiendo que EXISTA el dato de guía** | 16,49% | **+3,37** | −0,43 | +8,15 | 34 |
| C6 = C4 + guía no desacelera | 18,70% | +4,95 | −0,99 | +12,53 | **17** |

**C8 no filtra nada**: sólo se queda con las empresas que casualmente tienen dato de guía. Y ya
gana +1,02 pp sobre C4.

Del +2,60 pp que aportaba C6, **1,02 pp son simplemente tener el dato**, y sólo +1,58 pp son la
señal en sí — dentro del ruido que hemos medido en pruebas anteriores. Y el filtro deja la
cartera en **17 nombres**.

**Es el mismo problema que `sector`, por segunda vez**: la disponibilidad del dato es en sí misma
un indicador de calidad (empresa cubierta, establecida, seguida por analistas), y condicionar
sobre ella contamina el resultado. Con `sector` era look-ahead puro; con la guía es más
discutible, pero que FMP tenga hoy la guía de un trimestre de 2010 depende de su cobertura
actual, que correlaciona con que la empresa siga existiendo.

**Veredicto: en la tabla no queda nada aprovechable.** Y ninguno arregla el problema de fondo —
todos siguen perdiendo contra el NASDAQ en la primera mitad.

---

## 4. Lo que falta de verdad

El panel **no tiene ni un solo campo de balance ni de flujo de caja**. Todo son métricas
derivadas de la cuenta de resultados y del precio. Lo ausente, ordenado por lo que importa **a la
cartera que realmente tenemos**:

| Falta | Por qué importa aquí | Prioridad |
|---|---|---|
| **Deuda neta / EBITDA** | Tenemos ~50% de cíclicas. En una cíclica el apalancamiento **es** el riesgo: es lo que convierte una recesión en una quiebra. Es casi seguro donde viven nuestras caídas del −60% | **Máxima** |
| **Flujo de caja libre y su conversión** | Todo lo que medimos son ventas y márgenes contables. No sabemos si alguna genera caja | **Máxima** |
| **ROIC / ROCE** | Lo preguntaste al principio y nunca pudimos. Distingue crecimiento que crea valor del que lo destruye | **Alta** |
| **Ciclo de conversión de caja e inventarios** | En industriales y consumo cíclico, el inventario es el indicador adelantado del ciclo. Podría ser el "punto de inflexión" que buscabas | **Alta** |
| **Volumen / liquidez** | Sin esto no sabemos si es ejecutable (ya lo suplimos con FMP para los 43 actuales, pero no históricamente) | **Alta** |
| Beneficio por acción y su revisión | Sólo tenemos ingresos. Todo el factor "calidad de beneficios" está ausente | Media |
| Número de acciones en nivel | Sólo tenemos la variación interanual | Media |
| Valor contable, activos tangibles | Ni un solo múltiplo sobre balance | Media |
| Dividendos | `precio_post` es precio bruto; no podemos medir retorno total | Media |
| Industria (más fina que sector) | "Technology" agrupa cosas que no se parecen en nada | Media |
| Posiciones cortas, insiders | Señales de posicionamiento | Baja |

---

## 5. La buena noticia: con el plan nuevo ya se puede

Comprobado para tickers **estadounidenses** (`HLIO`, trimestral):

- `balance-sheet-statement` → ✅ incluye `totalDebt`, `netDebt`, inventarios, fondo de maniobra
- `key-metrics` → ✅ incluye `returnOnInvestedCapital`, `returnOnEquity`, `netDebtToEBITDA`,
  `freeCashFlowYield`, `incomeQuality`, `cashConversionCycle`, `daysOfInventoryOutstanding`,
  `capexToRevenue`, `currentRatio`

Es decir: **los cinco huecos de máxima y alta prioridad se pueden rellenar hoy mismo.** Lo que no
se puede es Europa, que sigue bloqueada.

---

## 6. Qué propongo

**Ampliar el panel con una tabla nueva** (`fundamentales_extra`), por ticker y trimestre, con:

```
netDebtToEBITDA        returnOnInvestedCapital     freeCashFlowYield
totalDebt / netDebt    returnOnEquity              incomeQuality
currentRatio           daysOfInventoryOutstanding  cashConversionCycle
capexToRevenue         intangiblesToTotalAssets    workingCapital
```

Coste aproximado: 2 llamadas por empresa y por bloque de trimestres. Para las ~1.800 empresas del
universo `U_universo` son ~3.600 llamadas. Es una descarga larga pero de una sola vez.

**Y una advertencia que ya nos ha mordido dos veces:** hay que traer los datos **también para las
empresas desaparecidas**, no sólo para las vivas. Si la descarga sólo cubre las que cotizan hoy,
volveremos a crear exactamente el sesgo que acabamos de descubrir, y la próxima vez estará
escondido en una tabla nueva en vez de en el campo `sector`.

### Las tres hipótesis que yo probaría primero con esos datos

1. **Deuda neta / EBITDA como filtro de exclusión.** Hipótesis: elimina la mayor parte de las
   caídas del −60% sin tocar los aciertos. Es la que más puede subir el alfa **de verdad**,
   porque ataca la cola izquierda en vez de perseguir la derecha.
2. **Inventarios como indicador adelantado del ciclo.** Hipótesis: en una cíclica, el inventario
   subiendo mientras las ventas se frenan anticipa el giro uno o dos trimestres antes que el
   precio. Sería el punto de inflexión que llevamos buscando desde el principio.
3. **ROIC frente a coste del capital.** Hipótesis: separa las cíclicas que crean valor a lo largo
   del ciclo de las que sólo lo trasladan. Y es la pregunta que hiciste tú al principio de todo.
