# Pre-registro — El eje temporal (regla de exposición por régimen)

**Escrito y comiteado ANTES de calcular ningún resultado de las reglas.** Cumple la regla 1
de método. Fecha: 2026-09-02.

## 1. Hipótesis

Todo lo probado en la serie anterior son reglas de **sección cruzada** (qué comprar), y
ninguna descorrelaciona (HALLAZGOS C5, C6). La hipótesis viva es que una regla de **serie
temporal** (cuánta exposición tener según el régimen) sí puede descorrelacionar del Nasdaq
manteniendo rentabilidad de renta variable, que es el mecanismo del seguimiento de tendencia.

## 2. Datos

`senal_regimen.csv`, 17 años (2007–2023), reconstruido con `c4_base.sql` sin tocar ninguna
guarda. Validado contra HALLAZGOS: CAGR 14,16%, Nasdaq 13,89%, correlación 0,918 —
coincide con C9 y C3.

**Restricción descubierta al construirlo, ya incorporada:** los precios del panel están
forward-filled antes de 2007 (91,7% de los tickers con `mom12` exactamente 0 en 2004). La
serie no puede empezar antes de 2007. Documentado en `NOTA-PRECIOS-PLANOS-PRE-2007.md`.

## 3. Las reglas, cerradas y SIN parámetros libres

Ambas deciden cada febrero del año Y, con información disponible en ese momento:

- **R1 (primaria) — momento del índice.** `e[Y] = 1` si el retorno del Nasdaq en los 12
  meses previos (feb Y−1 → feb Y, columna `qqq_prev`) es **> 0**; si no, `e[Y] = 0`.
- **R2 (secundaria) — momento del universo.** `e[Y] = 1` si la mediana de `mom12` del
  universo filtrado en feb Y (`med_mom_univ`) es **> 0**; si no, `e[Y] = 0`.

Fuera del mercado se asume efectivo al **2% anual** (el `RF` que ya usa `nasdaq.py`). Se
reporta también con 0%.

**El umbral es 0 en ambas. No se ajusta nada.** Esto es deliberado: una regla sin parámetros
libres no necesita muestra de descubrimiento, así que **recupera la potencia que el split
pares/impares destruiría**. El split se usa solo como comprobación de consistencia, no para
fijar nada.

## 4. Contraste principal: permutación de la exposición

El contrafactual aleatorio (regla 2) trasladado al eje temporal. Ya medido en `poder.py`:
**el 70% de los overlays aleatorios con p=0,7 bajan la correlación de 0,918 a menos de 0,80,
y el 8,3% cumplen a la vez correlación < 0,80 y CAGR > Nasdaq.** Probar 15 variantes y
quedarse con la mejor da éxito aparente con probabilidad ~73% sin ninguna señal.

Por tanto el null correcto **no** es "siempre invertido", sino **permutar el propio vector de
exposición de la regla entre los años**. Eso mantiene fijo *cuántas* veces sale del mercado y
pregunta solo si acierta *cuándo*. Es la única pregunta que importa.

- Estadístico: el par (CAGR del overlay, correlación del overlay con el Nasdaq).
- `p_conjunta` = fracción de permutaciones con CAGR ≥ observado **y** correlación ≤ observada.
- 20.000 permutaciones, semilla 13 (la de toda la serie).

## 5. Criterio de éxito, declarado por adelantado

Una regla se declara **superviviente** solo si cumple las tres:

1. `p_conjunta < 0,025` sobre los 17 años (Bonferroni: 0,05 / 2 reglas).
2. CAGR del overlay ≥ CAGR del Nasdaq (13,89%). Bajar la correlación perdiendo
   rentabilidad no sirve: el usuario pide las dos cosas.
3. El signo del efecto se mantiene en años pares y en años impares por separado.

Cualquier otro resultado se reporta como **no distinguible del ruido**.

## 6. Límite de potencia, reconocido antes de mirar

Calculado en `poder.py` sobre esta misma serie:

- El IC95% de la correlación observada 0,918 con n=17 es **[0,784, 0,971]**.
- Separar r=0,92 de r=0,70 exige |Δz| > 0,741 y solo hay 0,709: **ni siquiera con los 17
  años completos hay potencia para afirmar descorrelación**. Con 9 y 8 años, menos.
- El SE del CAGR es **5,85 pp**: el IC95% de cualquier CAGR de esta serie es ±11,5 pp.

**Consecuencia asumida por adelantado:** este estudio puede refutar, pero casi no puede
confirmar. Si una regla pasa el criterio de la sección 5, se reportará como *indicio*, nunca
como efecto establecido, y se dirá qué datos harían falta para cerrarlo.

## 7. Qué falsaría la hipótesis

Que la `p_conjunta` de ambas reglas quede por encima de 0,025 — es decir, que acertar
*cuándo* salir no aporte nada sobre salir *igual de a menudo* al azar.
