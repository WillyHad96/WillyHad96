# Los precios del panel están planos antes de 2007

Hallazgo colateral al construir la serie del eje temporal. **No estaba en `HALLAZGOS.md`** y
es independiente del sesgo de supervivencia ya documentado en A1.

## El dato

Porcentaje de tickers del universo filtrado cuyo `mom12` es **exactamente 0** — es decir,
`precio_post` idéntico al de cuatro trimestres antes:

| año | % con mom12 = 0 exacto | % positivo | % negativo |
|---|---|---|---|
| 2004 | **91,7%** | 6,6% | 1,7% |
| 2005 | **88,7%** | 7,1% | 4,2% |
| 2006 | **83,6%** | 10,9% | 5,5% |
| 2007 | 9,4% | 64,6% | 26,1% |
| 2012 | 8,3% | 45,8% | 45,8% |
| 2020 | 7,3% | 43,0% | 49,6% |
| 2023 | 2,2% | 35,5% | 62,2% |

Reproducible con `flat.sql`.

## Qué significa

1. **Antes de 2007 el panel no tiene precios: tiene una constante repetida.** Nueve de cada
   diez tickers no se mueven en doce meses. Cualquier backtest que empiece antes de 2007 no
   está midiendo una estrategia, está midiendo un forward-fill.
2. **A1 se queda corto.** A1 decía que 2002–2014 era ficción *porque no registra muertes*.
   Esto es un defecto distinto y anterior: los precios tampoco existen. El tramo
   "2002–2014: ficción" debe leerse como **"antes de 2007: sin precios; 2007–2014: precios
   sí, muertes no"**.
3. **El arranque en 2007 de `c4_base.sql` no era conservadurismo, era necesidad**, y nadie
   lo había justificado por escrito. Ahora está justificado.
4. **Queda un ~8% residual entre 2007 y 2020** que sí contamina la estrategia en producción:
   `mom12` es la **variable de selección** (top 20% por momento). Un ticker con `mom12 = 0`
   exacto no puede entrar nunca en el top 20%. Es decir, ese ~8% del universo está
   **excluido en silencio de la selección** por un defecto de datos, no por la regla.

## Efecto colateral ya visible

Explica por qué la mediana de `mom12` del universo sale exactamente 0,00 en 2012, 2019 y
2020: son años con el universo partido casi al 50% entre positivos y negativos, y la masa
del ~8% en cero exacto cae justo sobre la mediana. Es un síntoma, no un defecto aparte.

## Pendiente

Medir si ese ~8% excluido rinde distinto del resto. Si rinde distinto, es un sesgo de
selección con signo, del mismo tipo que el centinela `'desconocido'` de A4.
