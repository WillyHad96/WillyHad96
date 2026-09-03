# Las muertes sí están en el panel: son el cubo `'desconocido'`

Hallazgo al buscar cíclicas quebradas para poder validar el bloque de supervivencia.
**Reordena A3, A4 y el alcance de todo el análisis sectorial de la serie.**

## 1. El dato

Tickers que dejan de aparecer en el panel (última observación >6 meses antes del final):

| grupo | tickers | salen | **% que sale** |
|---|---|---|---|
| **`'desconocido'`** | 4.808 | **1.619** | **33,7%** |
| otro sector | 1.153 | 4 | 0,3% |
| **cíclico** | 704 | **3** | **0,4%** |

**Ochenta veces más mortalidad en el cubo sin sector que en el cubo con sector.**

## 2. Qué significa

**`sector = 'desconocido'` no es "falta el dato". Es el marcador de muerte.** A la empresa que
desapareció nunca le rellenaron los metadatos, porque el panel se construyó desde una lista
de tickers vivos y las bajas quedaron sin clasificar.

Consecuencias, por orden de importancia:

1. **A4 queda explicado.** El centinela predecía −8,98 pp (p=0,064) y −12,63 pp ponderado
   (p=0,008) porque **el centinela *es* "esta empresa va camino de desaparecer"**. No era
   un sesgo raro de metadatos: era la tasa de mortalidad, colándose por la puerta de atrás.
2. **Todo análisis sectorial de la serie ha corrido sobre un universo con 0,4% de
   mortalidad cuando la real es 33,7%.** Eso incluye C2, C12, C13, C14, `ESTUDIO-COLAS.md`
   y el piloto de cíclicas. No es un sesgo de grado: es otro universo.
3. **Pero las muertes SÍ están en los datos.** Simplemente no se pueden ver por sector.
   Son recuperables.

## 3. Las bajas no son todas muertes

Un ticker que desaparece puede haber quebrado (−100%) o haber sido comprado con prima
(+30%). Clasificando por el **retorno del último año antes de salir**:

| año | clasificables | bala grave (<−60%) | bala leve (−60 a −25%) | neutra | **compra con prima (>+10%)** |
|---|---|---|---|---|---|
| 2015 | 16 | 3 | 3 | 6 | 4 |
| 2018 | 16 | 4 | 3 | 2 | 7 |
| 2020 | 23 | 8 | 2 | 8 | 5 |
| 2021 | 93 | 8 | 7 | 12 | **66** |
| 2022 | 139 | 21 | 25 | 34 | **59** |
| 2023 | 152 | **40** | 25 | 30 | **57** |

**En 2021–2023 hay 126 balas reales y 182 compras con prima.** En 2021 el retorno medio de
las salidas fue **+86,5%**: fue año de M&A, no de muertes. **Contar toda salida como muerte
sobreestimaría el sesgo tanto como ignorarlas lo subestima.**

Clasificar por caída respecto al pico de 2 años **no sirve**: marca como bala a ONEM
(comprada por Amazon con prima), ZNGA (Take-Two), COUP, ZEN, OSH y las fusiones DISCA/VIAC.
El retorno del último año sí las separa.

## 4. Las balas son reconocibles

Entre las 2021–2023: **SIVB** (Silicon Valley Bank), **SBNY** (Signature), **FRC** (First
Republic), **RAD** (Rite Aid), **ENDP**, **MNK**, **YELL**, **WPG**, **PEI**, **AMRS**,
**CANO**, **SDC**, **FTCH**, más una docena con sufijo **Q**, que es literalmente el marcador
de quiebra en el ticker (CORZQ, TREVQ, NAVBQ, SIMPQ, REVRQ, XEBEQ, FNHCQ).

Que aparezcan los nombres correctos es la mejor validación de que la clasificación funciona.

## 5. Segunda corrección a `AGENDA-ESTUDIOS.md`

`AGENDA` decía: *"`company/delisted-companies` con `page>=1`: impide corregir la
supervivencia"*. **Ya no es cierto en Premium: verificado, devuelve datos con `page=3`.**
Da símbolo, nombre, mercado, fecha de salida a bolsa y **fecha de baja**.

Es la segunda cosa que `AGENDA` daba por bloqueada y no lo está (la primera fueron los
trimestrales). **Conviene reverificar el plan antes de dar nada por imposible.**

## 6. El estudio que esto habilita — "esquivar balas"

Por primera vez se puede probar el bloque C del diseño (supervivencia), que era el que
`DISEÑO-PANEL-CICLICAS.md` §7 daba por no validable.

- **Casos:** las ~126 balas de 2021–2023 (retorno del último año < −25%), más ~50 de 2015–2020.
- **Controles:** supervivientes del mismo año.
- **Variables:** las mismas del piloto — `nd_mid_ebitda`, `ndebitda`, `curratio`,
  `interestCoverageRatio`, `capexdep`, `pos_roce` — medidas **antes** de la muerte, con el
  mismo desfase anti-look-ahead (último trimestre cerrado antes del 15-nov previo).
- **Criterio:** AUC contra "muere", con ~126 casos el SE es ~0,045, así que **AUC ≥ 0,60 sí
  es detectable**. Esta vez el umbral está calculado antes, no después.
- **Coste:** ~126 balas + ~200 controles = ~330 llamadas, ~27 rondas. Contexto ~0.

**Y esta prueba es más fuerte que la del piloto**, porque el resultado que busca (la deuda
predice la muerte) es un efecto grande y bien documentado en la literatura, no un alfa
marginal de 2 pp.

## 7. Lo que NO arregla

Recuperar las bajas registradas **no** reconstruye el universo point-in-time. Siguen faltando
las empresas que murieron **antes de 2015**, donde el panel registra 0–5 bajas al año frente
a 200–400 reales (A1). El tramo 2021–2023 es el único con registro creíble, y es el único
sobre el que este estudio puede concluir.
