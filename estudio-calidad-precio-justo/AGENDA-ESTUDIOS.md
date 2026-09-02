# Agenda de estudios: qué se puede hacer con los datos actuales

Verificado empíricamente contra el panel y contra FMP (plan Starter), 2026-08.

## 1. Matriz de viabilidad

| Estudio | Datos que exige | ¿Viable ya? |
|---|---|---|
| **Sectores estructurales + mito de la diversificación** | panel actual | **Sí, coste cero** |
| **Añadir en subidas vs recortar en bajadas** | panel actual (precios trimestrales) | **Sí, coste cero** |
| **Tus propias operaciones** | IBKR `get_account_trades` | **Sí, coste cero** |
| ROIC / FCF / ingresos vs retorno a largo | FMP `key-metrics` (anual) | Sí, tras construir la base |
| Flujo presente vs crecimiento futuro | FMP `key-metrics` + `cashflow-statement` | Sí, tras construir la base |
| Corregir el sesgo de supervivencia | delistings históricos | **No** con el plan actual |

## 2. Qué da y qué no da el plan Starter de FMP

**Funciona (verificado):**

| Endpoint | Granularidad | Contenido relevante |
|---|---|---|
| `statements/key-metrics` | **anual** | `returnOnInvestedCapital`, `freeCashFlowYield`, `netDebtToEBITDA`, `investedCapital`, `incomeQuality`, `stockBasedCompensationToRevenue`, `evToFreeCashFlow`, `returnOnCapitalEmployed` |
| `statements/balance-sheet-statement` | anual | `totalDebt`, `netDebt`, `goodwill`, `totalStockholdersEquity` |
| `insiderTrades/insider-trade-statistics` | **trimestral, desde 1997** | `acquiredDisposedRatio`, `totalPurchases`, `totalSales` |
| `analyst/historical-grades` | mensual | recuento de recomendaciones |

**Bloqueado por plan:**

| Qué | Detalle |
|---|---|
| ~~`period=quarter` en `statements`~~ | **CORREGIDO 2026-09-02: ya NO está bloqueado.** La cuenta está en plan Premium y los trimestrales funcionan. Verificado con NUE: 80 trimestres continuos hasta 2006-09-30, cubre entera la ventana 2007-2023. Ver `DISEÑO-PANEL-CICLICAS.md` |
| `company/delisted-companies` con `page>=1` | impide corregir la supervivencia |
| `indexes/historical-*` | sin constituyentes históricos de S&P 500 / NASDAQ |

`key-metrics` anual cubre en una sola llamada por símbolo el ROIC, el FCF, el
apalancamiento y la retribución en acciones. Es la pieza que faltaba.

## 3. El cuello de botella no es el plan, es la tubería

Una llamada por símbolo, ~9.000 tokens por ticker con 10 años. Con ~1.400 tickers en el
universo son ~12,6 M de tokens: **inviable vía MCP**. La arquitectura correcta es descargar
en bloque con la API key desde un script y cargar el resultado en Supabase **una sola vez**;
a partir de ahí cada estudio es SQL barato y repetible.

Requisito: la clave de FMP disponible como variable de entorno. Sin eso, cualquier estudio
que necesite fundamentales queda limitado a muestras de 100–150 tickers.

## 4. Predicciones antes de mirar (para poder equivocarse por escrito)

Derivadas de lo ya establecido en `RESULTADOS.md`:

1. **Por acción domina a agregado.** `ingresos por acción` y `FCF por acción` batirán a sus
   versiones agregadas por un margen amplio. Sigue mecánicamente del hallazgo de la dilución
   (secciones 12 y 17) y contradice cómo se mide habitualmente el crecimiento.
2. **El nivel de ROIC falla; la estabilidad del ROIC funciona.** La rentabilidad sostenida
   aportó −4,2 pp y la estabilidad +10–12 pp. El ROIC alto ya está en el precio.
3. **"Sectores estructuralmente mejores" es retrovisor.** Ya hay evidencia en contra
   (sección 13): el orden sectorial se invirtió entre 2007–2011 y 2012–2021 — Basic Materials
   +35,2% → −5,1%, Consumer Cyclical +25,0% → −17,5%.
4. **Pero la diversificación sí tiene rendimientos decrecientes rápidos.** Predicción: más
   allá de 4–5 sectores el beneficio marginal en Sharpe es despreciable. Apoyaría la intuición
   de concentrar, aunque no por elegir "los mejores" sectores sino porque el número basta.
5. **Accruals (`incomeQuality`) darán señal.** Beneficio muy por encima del flujo de caja
   predice mal rendimiento (Sloan, 1996) y encaja con el tema de cómo se financia el
   crecimiento. Barato de probar y con alta probabilidad de salir.
6. **Añadir a ganadores depende del plazo.** Funcionará a 3–12 meses y dejará de funcionar
   más allá. Si sale así, "dejar correr los ganadores" y "rebalancear" no se contradicen:
   son horizontes distintos.

## 5. Secuencia recomendada

1. **Sectores y diversificación** — coste cero, y una de las dos mitades ya está medio contestada.
2. **Tus operaciones reales de IBKR** — es lo único irrepetible y nadie más lo tiene.
3. **Construir la base anual de FMP** (necesita la clave) → ROIC, FCF, apalancamiento, accruals y SBC de una sentada.
4. **Delistings** solo si se van a tomar decisiones con las cifras absolutas, no con las relativas.
