# Buscando beta descorrelacionada: no está en las cíclicas, está en las defensivas

Pregunta: dentro de lo ya probado, ¿qué compartimento aporta rentabilidad parecida al
Nasdaq con la menor correlación posible? Se acepta más volatilidad; **beta y rentabilidad
son los criterios**.

**Respuesta: la parte cíclica NO es la descorrelacionada. Es la defensiva.** Y el
resultado es frágil: no supera el control fuera de muestra.

Todo en ventanas feb–feb 2007–2023 (17 observaciones), sobre `hypergrowth_panel`.
Benchmark: Nasdaq 13,82% CAGR, desv. 21,9; S&P 8,36%, desv. 19,0.

## 1. La rejilla de variantes cíclicas: ninguna descorrelaciona

| # | variante | n/año | CAGR | desv. | corr Nasdaq | **beta** | alfa |
|---|---|---|---|---|---|---|---|
| 1 | C4 completo | 36 | 13,74 | 21,3 | +0,85 | 0,83 | +2,7 |
| 2 | C4 solo cíclicos | 15 | 12,36 | 22,0 | +0,85 | 0,86 | +1,2 |
| 4 | Cíclicos sin filtro de estabilidad | 33 | 10,97 | 23,3 | +0,81 | 0,86 | +0,1 |
| 5 | Cíclicos C4 sin momento | 73 | 12,59 | 22,6 | +0,91 | 0,93 | +0,1 |
| 6 | Cíclicos C4 momento invertido | 15 | 13,87 | 30,7 | +0,88 | 1,23 | −2,0 |
| 7 | Cíclicos C4 + value (P/S bajo) | 15 | **15,78** | 28,8 | +0,87 | 1,14 | +1,4 |
| 8 | Cíclicos sin estabilidad + value | 33 | 13,65 | 40,3 | +0,86 | 1,59 | −5,5 |

**Todas las variantes cíclicas están entre 0,81 y 0,91 de correlación.** Ninguna baja de
0,80. Quitar el filtro de estabilidad, invertir el momento, añadir value: nada mueve la
correlación, solo sube la beta y la volatilidad.

La #7 (cíclicos + value) es la que más rinde, 15,78%, pero con beta 1,14: es **más**
Nasdaq, no menos. Gana por apalancamiento implícito, no por descorrelación.

## 2. Donde sí baja la correlación: defensivos

Consumer Defensive + Healthcare + Utilities, con los filtros de C4:

| # | variante | n/año | CAGR | desv. | corr | **beta** | alfa | peor año |
|---|---|---|---|---|---|---|---|---|
| D1 | Def + regla40 + mcap, top 20% momento | 12 | 11,50 | 20,3 | **+0,62** | **0,58** | **+4,1** | −22,1 |
| D7 | ConsDef+Utilities, solo mcap>p25 | 33 | 8,10 | 12,7 | +0,79 | **0,45** | +1,6 | −17,3 |
| D2 | Def, C4 completo, equiponderado | 26 | 12,78 | 19,4 | +0,85 | 0,75 | +2,5 | −31,1 |
| D3 | Def + regla40 + mcap, equiponderado | 57 | 11,41 | 18,4 | +0,82 | 0,69 | +2,0 | −25,4 |

**D1 es el único candidato serio:** correlación 0,62 frente a 0,85 de todo lo cíclico,
beta 0,58, y aun así 11,50% de CAGR. Y hace lo que se le pide en los años malos:

| | 2008 | 2015 | 2022 | media |
|---|---|---|---|---|
| Nasdaq | −30,1 | −2,4 | −14,8 | −15,8 |
| C4 cíclicos | −44,1 | −9,8 | +9,1 | −14,9 |
| **D1 defensivos** | **−18,3** | −7,5 | **+8,5** | **−5,8** |

El momento importa: D1 (con momento) tiene correlación 0,62; D3 (los mismos sin momento)
sube a 0,82. Seleccionar por momento **dentro** de defensivos es lo que descorrelaciona.

## 3. El control fuera de muestra: D1 no aguanta

Partiendo en años pares (descubrimiento) e impares (confirmación), como en los estudios
anteriores:

| mitad | n | CAGR | corr | beta | alfa |
|---|---|---|---|---|---|
| pares | 8 | 14,66 | +0,89 | 0,79 | **+7,9** |
| impares | 9 | 8,77 | +0,40 | 0,40 | **+2,3** |
| todos | 17 | 11,50 | +0,62 | 0,58 | +4,1 |

El alfa cae de +7,9 a +2,3 entre mitades, y la correlación pasa de 0,89 a 0,40. **Las dos
mitades no se parecen en nada.** Con 8 y 9 observaciones esto no distingue una señal real
de ruido, y es el sexto caso en esta serie en que un efecto aparente se deshace bajo
control.

Lo que sí es estable: la beta está por debajo de 1 en las dos mitades (0,79 y 0,40).
**La beta baja es más creíble que el alfa.**

## 4. Correlaciones cruzadas entre lo probado

| | Nasdaq | S&P | C4 | C4 cíclicos | D1 def |
|---|---|---|---|---|---|
| Nasdaq | 1,00 | +0,96 | +0,87 | +0,81 | **+0,62** |
| S&P | +0,96 | 1,00 | +0,84 | +0,84 | **+0,53** |
| C4 completo | +0,87 | +0,84 | 1,00 | +0,91 | +0,83 |
| C4 cíclicos | +0,81 | +0,84 | +0,91 | 1,00 | +0,68 |
| D1 defensivos | +0,62 | +0,53 | +0,83 | +0,68 | 1,00 |

D1 es lo menos correlacionado con **ambos** índices de todo lo que hemos construido.

## 5. Libros de renta variable, equiponderados y rebalanceados cada año

| libro | CAGR | desv. | peor | CAGR/desv | beta | 2008 | 2022 |
|---|---|---|---|---|---|---|---|
| Nasdaq solo | 13,82 | 21,9 | −30,1 | 0,630 | 1,00 | −30,1 | −14,8 |
| Nasdaq + C4 | 14,14 | 22,3 | −36,3 | 0,635 | 0,98 | −36,3 | −6,6 |
| **Nasdaq + D1** | 13,02 | **19,0** | **−24,2** | **0,685** | **0,79** | **−24,2** | −3,2 |
| Nasdaq + C4 + D1 | 13,50 | 20,4 | −30,3 | 0,661 | 0,84 | −30,3 | −1,6 |
| Nasdaq + C4cic + D1 | 13,05 | 19,7 | −32,8 | 0,664 | 0,82 | −32,8 | +3,1 |
| C4 + D1 (sin Nasdaq) | 13,09 | 21,2 | −30,4 | 0,617 | 0,77 | −30,4 | +5,0 |

**Ningún libro supera al Nasdaq en rentabilidad.** El mejor por unidad de riesgo es
Nasdaq + D1: cede 0,80 pp de CAGR a cambio de 2,9 puntos menos de desviación, beta 0,79 y
6 puntos menos de caída en 2008.

Añadir C4 al Nasdaq **empeora** el peor año (−36,3 frente a −30,1) sin ganar casi nada.

## 6. Qué se puede afirmar y qué no

**Se puede afirmar:**
- Las cíclicas de este panel no descorrelacionan. Correlación 0,81–0,91 en todas las
  variantes. La premisa de partida era incorrecta.
- Los defensivos con momento tienen beta estructuralmente inferior a 1 (0,79 y 0,40 en las
  dos mitades por separado), y protegen en los años malos del Nasdaq.
- La combinación con mejor rentabilidad por unidad de riesgo es Nasdaq + defensivos.

**No se puede afirmar:**
- Que D1 tenga alfa. Cae de +7,9 a +2,3 entre mitades.
- Que ninguna combinación bata al Nasdaq. Ninguna lo hace en esta ventana.
- Nada con 12 nombres por año y 17 observaciones tiene potencia estadística. El error
  típico de una correlación aquí es ~0,15 y el de un CAGR ~6 pp.

Y todo hereda el sesgo de supervivencia: universo con 83–85% de supervivientes donde
debería haber ~50%, y sin muertes registradas antes de 2015.

## Conclusión

Si el objetivo es **beta baja con rentabilidad parecida**, el candidato es el
compartimento defensivo con momento, no el cíclico. Pero es un candidato, no un
resultado: su alfa no sobrevive al control fuera de muestra y solo la beta baja parece
estable.

La lectura honesta de toda la rejilla es que **no hemos encontrado nada que bata al
Nasdaq**. Hemos encontrado algo que lo iguala con menos riesgo, y eso, para una cartera
donde el Nasdaq ya está presente, sigue teniendo valor.

## Ficheros

- `rejilla_beta.py` / `rejilla_beta.txt` — 9 variantes cíclicas.
- `rejilla_def.py` / `rejilla_def.txt` — 8 variantes defensivas.
- `tres_sleeves.py` — control por mitades, correlaciones cruzadas y libros combinados.
