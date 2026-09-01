# Desde qué año se puede creer el panel, y qué parte del alfa está en la zona limpia

Tres preguntas: (a) qué falla en usar solo la SEC, (b) desde cuándo el panel está mal
construido, (c) si ayuda que el alfa esté concentrado en los años recientes.

**Respuesta corta a (c): sí ayuda, y el dato lo respalda — pero el test no es independiente
del que ya hicimos, y la conclusión importante es otra: hay dos alfas distintos y solo uno
de ellos está contaminado.**

## 1. Cuándo empieza el panel a mentir: hay tres cortes visibles

Reconstruido desde el propio panel: tickers por año, altas (primera aparición), bajas
(última aparición) y cobertura del campo `sector`.

| año | tickers | altas | **bajas** | % con sector | % que sobrevive a 2025 |
|---|---|---|---|---|---|
| 2000 | 720 | 196 | **0** | 6,7 | 54,4 |
| 2001 | 1.315 | **608** | **0** | 14,5 | 69,8 |
| 2002 | 2.420 | **1.123** | **0** | **36,5** | 82,0 |
| 2008 | 3.657 | 354 | **5** | 30,0 | 81,4 |
| 2012 | 4.915 | 337 | **4** | 26,4 | 82,8 |
| 2015 | 5.611 | 158 | **18** | 26,1 | 82,9 |
| 2016 | 5.775 | 173 | **58** | 26,1 | 83,0 |
| 2021 | 6.608 | 92 | **105** | 27,3 | 85,1 |
| 2023 | 6.468 | 23 | **243** | 28,6 | 88,7 |
| 2025 | 5.914 | 0 | **545** | 31,4 | 97,1 |

En el mercado real desaparecen del orden de **200 a 400 cotizadas al año** por fusiones y
exclusiones. El panel registra **entre 0 y 5 al año hasta 2014**.

Tres cortes:

1. **~2001–2002: nace la historia.** 608 + 1.123 altas en dos años y la cobertura de
   `sector` salta del 6,7% al 36,5%. Antes de 2001 quedan ~700 tickers: un residuo, no un
   universo. **Nada anterior a 2002 es utilizable.**
2. **~2015–2016: empiezan a registrarse las muertes.** De 5 bajas en 2014 a 18 y 58. Es
   el momento en que la fuente empieza a seguir exclusiones.
3. **~2021: la tasa de muerte se vuelve semi-realista.** 1,6% en 2021, 2,5% en 2022,
   3,8% en 2023, 5,1% en 2024. La tasa real ronda el 4–5%.

Y un cuarto detalle: **0 altas en 2024 y 2025.** No se ha incorporado ninguna cotizada
nueva después de 2023. La ingesta de nuevas salidas a bolsa está parada.

**Veredicto de cobertura:**

| tramo | estado como universo |
|---|---|
| antes de 2002 | inservible |
| 2002–2014 | **ficción**: cero muertes registradas |
| 2015–2020 | contaminado, mejorando |
| 2021–2023 | aceptable con reservas |
| 2024+ | sin altas nuevas |

La columna "% que sobrevive a 2025" es la prueba más limpia: **se queda plana en 82–85%
desde 2002 hasta 2020.** Una cohorte de 2002 y una de 2020 no pueden tener la misma tasa
de supervivencia a 2025. Solo eso ya invalida el universo.

## 2. ¿Está el alfa en la zona limpia? Sí, pero ojo con leerlo mal

Usando la tasa de muerte registrada de cada año como proxy de "cuán real es el dato":

| tramo de cobertura | años | alfa vs NASDAQ | pasar el filtro vs no pasarlo |
|---|---|---|---|
| sucio (<0,20% muertes) | 9 | **−2,6 pp** | +4,0 pp |
| medio (0,20–1,0%) | 5 | **+4,1 pp** | −0,1 pp |
| limpio (>1,0%) | 3 | **+5,7 pp** | +5,2 pp |

Correlación alfa ↔ cobertura de muertes: **r = +0,379**, p (permutación, 20.000 it,
semilla 13) = **0,138**.

Va en la dirección buena: el alfa es mayor donde el dato es menos falso. Pero:

**Aviso importante: este test no aporta evidencia nueva.** La cobertura de muertes crece
monótonamente con el año, así que "años limpios" y "años recientes" son la misma variable.
Este r = +0,379 es el mismo hecho que la brecha H1/H2 de `ESTUDIO-MITADES.md` (p = 0,105),
mirado desde otro ángulo. **No es una confirmación independiente, es la misma observación
contada dos veces.** No se puede separar "el dato mejoró" de "la estrategia funcionó mejor"
con 17 años.

## 3. Lo que sí sale de aquí: hay dos alfas y solo uno está contaminado

| medida | media | desv. | t | años positivos |
|---|---|---|---|---|
| alfa vs NASDAQ | +0,83 pp | 9,54 | **+0,36** | 9/17 |
| pasar el filtro vs no pasarlo | **+2,98 pp** | 6,60 | **+1,86** | **12/17** |

Y por tramos de contaminación, la comparación interna **no tiene tendencia**
(r = +0,165, p = 0,55): vale +4,0 / −0,1 / +5,2 en sucio / medio / limpio.

Eso es exactamente lo que se espera de una medida donde **el sesgo afecta a los dos brazos
por igual**. Si faltan las empresas muertas, faltan tanto del grupo que pasa el filtro como
del que no. La comparación interna se lo come; la comparación contra un índice real, no.

**El alfa contra el NASDAQ es la cifra frágil. La comparación interna es la robusta —
y es más fuerte (t = 1,86 vs 0,36) y más consistente (12/17 años vs 9/17).**

## 4. Qué pasaría si tuviéramos las empresas que faltan

Razonando sobre el mecanismo, no midiendo (no se puede medir sin los datos):

- **Alfa vs NASDAQ: se quedaría igual o bajaría.** Las empresas que mueren rara vez pasan
  a la vez el filtro de estabilidad de márgenes y el de momento a 12 meses, así que pocas
  entrarían en cartera. Pero los umbrales son percentiles del universo: meter miles de
  empresas peores baja el p25 de regla40 y sube la mediana de sd(margen), o sea **afloja
  los filtros** y deja entrar más marginales. Efecto neto: neutro o negativo.
- **Comparación interna: subiría.** El brazo "no pasa el filtro" se llenaría precisamente
  de las empresas que el filtro existe para evitar. La distancia entre los dos brazos se
  ensancharía.

Así que tu intuición es correcta, pero **para la medida interna, no para el alfa contra el
índice**. Y eso encaja con lo único que ha sobrevivido a todos los controles de esta
serie de estudios: *pasar el filtro bate a no pasarlo*.

## 5. Qué falla en usar solo la SEC

No es que tenga trampa, es que **no es una base de datos de mercado, es un archivo de
documentos**. Siete problemas concretos:

1. **No hay precios. Ninguno.** Hay que traerlos de otra fuente, y el cruce es el trabajo.
2. **Los Financial Statement Data Sets empiezan en 2009Q2**, y el mandato XBRL fue por
   fases: las grandes desde junio de 2009, las pequeñas hasta junio de 2011. Para small
   caps —tu universo— la cobertura real empieza hacia 2011. **Tu backtest arranca en 2007.**
3. **Es un universo de *presentadores*, no de cotizadas.** Incluye emisores solo de deuda,
   fondos, SPACs, shells y extranjeras con 20-F. No te dice qué cotizaba, en qué bolsa, ni
   si era acción ordinaria.
4. **El mapeo CIK↔ticker histórico es el verdadero asesino.** `dei:TradingSymbol` solo es
   fiable desde ~2019. Para 2008 hay que sacarlo de las portadas de los 10-K, y las
   empresas que cambiaron de ticker o murieron son las difíciles: justo las que necesitas.
5. **Etiquetas XBRL inconsistentes.** "Ingresos" aparece bajo una docena de tags según
   empresa y año. Normalizar eso son meses de trabajo.
6. **No hay acciones corporativas.** Ni splits, ni dividendos, ni spin-offs. Sin eso no hay
   retornos.
7. **La ausencia de sesgo no es gratis.** Si construyes el universo desde el fichero actual
   de tickers de la SEC, te reintroduces el sesgo tú mismo. Hay que construirlo desde los
   índices trimestrales de EDGAR, presentación a presentación.

**Para qué sirve entonces:** como *auditoría* de fundamentales point-in-time de 2011 en
adelante, donde es insuperable porque trae la fecha de presentación. Como fuente de
universo y precios, es mala.

## Conclusión

- El panel es **ficción como universo antes de 2015** y solo aceptable desde 2021.
- El alfa **sí** está concentrado donde el dato es menos malo, pero ese test es colineal
  con el tiempo y **no añade evidencia** sobre la brecha entre mitades.
- Lo que sí cambia la lectura: **hay dos alfas.** El de contra el NASDAQ (+0,83 pp,
  t = 0,36) hereda el sesgo entero. El de pasar-el-filtro contra no-pasarlo (+2,98 pp,
  t = 1,86, 12/17 años) es inmune a él porque el sesgo afecta a los dos lados.
- **La tesis hay que reformularla sobre la medida interna**, no sobre el exceso contra el
  índice. Y con datos completos esa medida debería mejorar, no empeorar.

## Ficheros

- `contaminacion.py` — correlaciones y tramos de este documento.
