# PRE-REGISTRO — ¿Calidad a precio justo bate a barato y aburrido?

**Fecha de congelación:** 2026-08-17
**Estado:** escrito ANTES de calcular ningún resultado de contraste.
Solo se habían ejecutado diagnósticos de calidad de datos (sección 0), ninguno
de los cuales toca la relación valoración→retorno.

---

## 0. Diagnósticos previos ya ejecutados (no son resultados del estudio)

| Comprobación | Resultado | Veredicto |
|---|---|---|
| Defecto 1 — outliers de `crecimiento` | máx. 10^12,09 | confirmado |
| Defecto 2 — forward-fill de precios | 28,3% de filas con `precio_post = lag(precio_post)` | confirmado |
| Defecto 3 — delisting sin marcar | solo 13,6% de tickers desaparecen; **25 tickers** mueren antes de 2015 | **peor de lo documentado** |
| Defecto 4 — `sector='desconocido'` | 68,6% de filas | confirmado, se excluye |
| Defecto 5 — `regla40` fuera de escala | máx. 1,2×10^12 | confirmado, no se usa |
| Defecto 6 — outliers en `fwd_4t` | máx. 10^53,6 | confirmado, se winsoriza |
| **Defecto 7 (NUEVO)** — `margen_bruto` fuera de [0,1] | máx. 64.984, mín. −15.422.466; 8,2% de filas absurdas | **no documentado; letal para P/GP** |
| **Defecto 8 (NUEVO)** — reporte semestral | p95 del salto de 8 filas = **4,00 años exactos**; 15,8% de eventos | **no documentado; rompe el encadenado por offset** |

Los defectos 7 y 8 son hallazgos propios de este estudio y ambos son
existenciales para la pregunta: el 7 porque `P/GP = multiplo_ps / margen_bruto`
explota si el denominador es ~0 o negativo, y el 8 porque el encadenado por
`lead(precio_post, 8)` mide 4 años en vez de 2 en el 15,8% de los casos.

---

## 1. Universo (fijado, no se toca después)

```
fecha >= 1995-01-01
ticker ~ '^[A-Z]{1,5}$'
  and not (length(ticker) >= 5 and right(ticker,1) in ('F','Y'))
  and not (length(ticker) >= 4 and right(ticker,1) in ('W','U','R','Z'))
precio_post >= 1
sector is not null and sector <> 'desconocido'
ingresos_ttm >= 1e7
crecimiento between -0.99 and 3.0
margen_bruto between 0.05 and 0.95        <-- defecto 7
multiplo_ps > 0
market_cap = multiplo_ps * ingresos_ttm  entre 3e8 y 5e9
```
Tamaño esperado: ~56.400 eventos, ~1.700 tickers.

## 2. Retornos (requisito previo)

- `ret_kq = precio_post[i+k] / precio_post[i] − 1`, para k = 4, 8, 12, 20.
- Se descarta el evento si el precio inicial **o** el final están forward-filled
  (`precio = lag(precio)`).
- Se exige coincidencia temporal: `(fecha[i+k] − fecha[i])/365,25` dentro de
  ±0,25 años del objetivo (1, 2, 3, 5). Esto neutraliza el defecto 8.
- Benchmark: `spy_4t = fwd_4t − fwd_4t_rel_spy`, encadenado geométricamente
  por tramos de 4 trimestres del mismo ticker.
- Retorno relativo = `(1+ret_kq)/(1+spy_kq) − 1` (geométrico, no aritmético).

## 3. Definiciones

**CALIDAD** — estructural, sin juicios de perspectiva. Deben cumplirse las 5:
- Q1 `margen_operativo > 0` en cada uno de los 4 trimestres previos (rentabilidad sostenida)
- Q2 `delta_margen_op > 0` (margen operativo mejorando)
- Q3 `dilucion_yoy < 0,02` (no se financia emitiendo acciones)
- Q4 desviación típica de `margen_bruto` en 8T < mediana del universo (margen estable)
- Q5 desviación típica de `crecimiento` en 8T < mediana del universo (crecimiento consistente)

**MEDIOCRE** = cumple ≤ 2 de las 5.

`ESCALABLE` (sección 8 del brief) se reporta como **eje separado**, no se mete
dentro de CALIDAD: ya se sabe que funciona e incluirlo confundiría el contraste
con un factor conocido.

**PRECIO JUSTO** — terciles de `P/GP = multiplo_ps / margen_bruto` calculados
**dentro del grupo de calidad** y **por año de calendario** (para no comparar
valoraciones de 2001 con las de 2021). T1 = barato, T2 = precio justo, T3 = caro.
Se reporta SIEMPRE en paralelo la partición por `multiplo_ps` a secas.

## 4. Hipótesis (congeladas)

- **H1 (control de replicación).** Particionando por `multiplo_ps`, el tercil
  barato bate al caro a 4T. *Criterio:* diferencia de mediana relativa a SPY > 0.
  Si no replica, el pipeline está mal y hay que parar.
- **H2 (la vara de medir).** Con `P/GP` en lugar de `multiplo_ps`, la ventaja del
  barato se reduce sustancialmente o desaparece. *Criterio:* la diferencia
  T1−T3 con P/GP es menos de la mitad de la diferencia con P/S.
- **H3 (Munger).** CALIDAD ∩ P/GP-T2 bate a MEDIOCRE ∩ P/GP-T1, **y la ventaja
  crece con el horizonte**. *Criterio:* diferencia ≤ 0 a 4T y > 0 a 12T y 20T,
  en mediana relativa a SPY.
- **H4 (riesgo).** Aunque el CAGR sea menor, la cartera de calidad da **Sharpe > 0,60**
  y peor año mejor que **−39,4%**.
- **H5 (control negativo).** `inicial_AM` = el ticker empieza por A–M. No debe
  aportar nada. *Criterio de fallo:* si la diferencia A–M vs N–Z supera en
  magnitud al 50% del efecto principal, baja la confianza en todo.
- **H6 (contaminación temporal).** Todo se reporta partido en 2005–2012 y
  2013–2025. Si el efecto solo aparece en el periodo reciente, se marca como sospechoso.

## 5. Reglas de reporte (comprometidas de antemano)

1. Mediana y media geométrica siempre; la media aritmética solo como nota al pie.
2. Se reporta `%>+100pp` y `%desastre` (< −50%) además de los centros.
3. Backtest ciego: parámetros congelados con datos ≤2016, evaluación en 2017–2025.
4. Beta, alfa de Jensen y Sharpe. Un alfa > 15% se trata como error hasta prueba
   en contra.
5. Se reportan las hipótesis refutadas con el mismo detalle que las confirmadas.
6. Si el sesgo de supervivencia impide responder a 20T, se dice y se para ahí.
