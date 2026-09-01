# Descorrelación y rentabilidad (la volatilidad no penaliza)

Revisión de `ESTUDIO-BETA-DESCORRELACIONADA.md` con el criterio corregido. **Beta baja y
correlación baja no son lo mismo**: beta = correlación × (volatilidad del sleeve /
volatilidad del índice). Una cartera poco volátil tiene beta baja aunque se mueva a la vez
que el índice, y eso no diversifica nada.

Ejemplo de la rejilla anterior: "ConsDef+Utilities" tenía **beta 0,45** — parecía el mejor
— pero **correlación 0,79**. Su beta baja era volatilidad baja, no descorrelación. Con el
criterio corregido queda descartada.

## 1. La trampa: la correlación baja sola al reducir nombres

Antes de comparar variantes hay que fijar el contrafactual. Carteras **aleatorias** del
universo filtrado, equiponderadas, 300 simulaciones por tamaño (orden determinista):

| nombres | correlación con el Nasdaq de una cartera **al azar** |
|---|---|
| 3 | **0,654** |
| 5 | 0,735 |
| 12 | 0,825 |
| 25 | 0,866 |
| 40 | 0,883 |

Una cartera de 3 nombres **elegidos al azar** ya da 0,65 de correlación. Eso no es
descorrelación: es varianza idiosincrática, que añade riesgo sin añadir rentabilidad
esperada. Cualquier variante estrecha va a "parecer" descorrelacionada.

Por eso la métrica correcta no es la correlación, sino la **descorrelación real**:
correlación observada − la que da el azar con ese mismo número de nombres y ese mismo pool.

## 2. Las 16 variantes, ordenadas por descorrelación real

| variante | n/año | CAGR | corr | azar | **real** | alfa |
|---|---|---|---|---|---|---|
| Solo Energía+Materiales | 3 | 12,87 | 0,49 | 0,70 | **−0,21** | +3,5 |
| C4 solo defensivos | 5 | 13,60 | 0,46 | 0,65 | **−0,19** | +4,4 |
| **Defensivos + momento** | 12 | 11,50 | 0,62 | 0,76 | **−0,14** | +2,1 |
| Cíclicos sin estabilidad | 33 | 10,97 | 0,81 | 0,88 | −0,07 | +0,1 |
| Def+Energía+Materiales | 38 | 12,92 | 0,90 | 0,88 | +0,02 | +1,0 |
| C4 completo | 36 | 13,74 | 0,85 | 0,88 | −0,02 | +1,3 |
| C4 solo cíclicos | 15 | 12,36 | 0,85 | 0,85 | **−0,00** | +0,6 |
| Cíclicos + value | 15 | 15,78 | 0,87 | 0,85 | **+0,02** | +0,7 |
| Cíclicos momento invertido | 15 | 13,87 | 0,88 | 0,85 | +0,02 | −1,0 |
| Cíclicos sin momento | 73 | 12,59 | 0,91 | 0,88 | +0,03 | +0,0 |

Solo tres bajan del percentil 5 de su contrafactual aleatorio, y de esos, uno tiene 3
nombres y otro 5 — demasiado estrechos para llamarlos cartera. **El único con descorrelación
real y tamaño operable es "defensivos + momento" (12 nombres, −0,14).**

Y confirma lo del documento anterior: **ninguna variante cíclica descorrelaciona**.
Todas están en ±0,03 de lo que daría el azar.

## 3. El criterio que junta las dos cosas: CAGR de la cartera combinada

Si la volatilidad no penaliza, lo que importa es el CAGR final del conjunto. Mezcla 50/50
con Nasdaq, rebalanceada cada año (Nasdaq solo: 13,82%):

| variante | CAGR mezcla | vs Nasdaq | alfa de la mezcla | descorr. real |
|---|---|---|---|---|
| Cíclicos + value | **15,08** | **+1,26** | +0,7 | +0,02 |
| Cíclicos sin estab + value | 14,21 | +0,39 | −2,8 | −0,02 |
| C4 solo defensivos | 14,18 | +0,36 | **+4,4** | −0,19 |
| Cíclicos momento invertido | 14,06 | +0,24 | −1,0 | +0,02 |
| C4 completo | 13,93 | +0,10 | +1,3 | −0,02 |
| Solo Energía+Materiales | 13,89 | +0,07 | +3,5 | −0,21 |
| Defensivos + momento | 13,02 | −0,80 | +2,1 | −0,14 |

## 4. Pero el que gana, gana por beta — y eso se compra más barato

"Cíclicos + value" da +1,26 pp. Su descorrelación real es **+0,02**: cero. Su beta es 1,14.
La mezcla 50/50 tiene beta 1,07. Comparación directa:

| | CAGR |
|---|---|
| Nasdaq | 13,82 |
| Nasdaq × 1,05 | 14,41 |
| **Nasdaq × 1,07** (misma beta que la mezcla) | **14,66** |
| Nasdaq × 1,10 | 14,98 |
| Mezcla 50/50 con cíclicos+value | 15,08 |

**Casi todo el +1,26 pp se replica subiendo la exposición al Nasdaq.** Queda un residuo de
~0,4 pp, del orden del error de medición. No es una fuente de rentabilidad nueva: es la
misma con más tamaño, y con más trabajo, más comisiones y más impuestos.

*(El escalado no cobra coste de financiación, así que si acaso favorece a la variante.)*

## 5. Qué queda en pie

- **Nada descorrelaciona y rinde a la vez.** Lo que descorrelaciona de verdad
  (defensivos + momento) rinde 2,3 pp menos que el Nasdaq. Lo que rinde más
  (cíclicos + value) no descorrelaciona nada y su ventaja es beta replicable.
- **Las cíclicas quedan definitivamente descartadas** como fuente de descorrelación: las
  siete variantes están dentro del ruido de lo aleatorio.
- **"Defensivos + momento" sigue siendo el único candidato honesto**, pero su alfa no
  sobrevivió al control pares/impares (+7,9 → +2,3) en el documento anterior. Lo que sí
  es estable es la descorrelación (−0,14) y el comportamiento en años malos.
- Este panel **no contiene** un sleeve que descorrelacione del Nasdaq y rinda como él. Es
  un universo de acciones estadounidenses de crecimiento y calidad: todo dentro correlaciona
  0,8–0,9 con todo. La descorrelación de verdad hay que buscarla **fuera** de estos datos.

## 6. Limitaciones

- 17 observaciones anuales. Error típico de una correlación ~0,15, de un CAGR ~6 pp.
  Las diferencias de la tabla 3 no son significativas entre sí.
- El peso óptimo de cada sleeve está ajustado sobre la misma muestra que lo mide:
  sobreajustado por construcción, sirve para ver la forma y no para fijar un peso.
- El contrafactual aleatorio degenera cuando el número de nombres se acerca al tamaño del
  pool (el pool defensivo es ~40). Las marcas de las variantes con 30+ nombres no valen.
- Todo hereda el sesgo de supervivencia: universo con 83–85% de supervivientes y sin
  muertes registradas antes de 2015.

## Ficheros

- `descorrelacion.py` — contrafactual aleatorio, descorrelación real, test de apalancamiento.
- `rejilla_beta.py` / `rejilla_def.py` — las 16 variantes.
