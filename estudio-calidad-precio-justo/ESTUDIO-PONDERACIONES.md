# Ponderación: cuánto inclinar la cartera hacia el momentum

19 esquemas de ponderación sobre los mismos 541 eventos (2007–2025, entrada de febrero,
top 20% por momentum). **Es un barrido de parámetros, justo lo que el preregistro prohíbe**, así
que todo se juzga contra una banda de ruido medida por permutación, no contra el CAGR pelado.

Conclusión corta: **sí se rascan puntos, unos +1,4 pp pasando de `rank^1` a `rank^2`. Pero el
mecanismo no es el que parece, y las versiones agresivas no se sostienen.**

---

## 1. El barrido

`rank` = puesto por momentum dentro de los ~28 seleccionados (1 = el que menos ha subido).
Peso ∝ `rank^p`. Con p=0 es equiponderado; p=1 es lo que veníamos usando; p<0 invierte la
inclinación (control negativo).

| Esquema | CAGR | Alfa vs SPY | Vol | Peor año | Ret/Vol | Peso máx. medio |
|---|---|---|---|---|---|---|
| **top 10** | **25,58%** | +15,76 | 31,6% | −37,3% | 0,810 | 10,0% |
| rank^5 | 24,94% | +15,98 | 26,5% | −29,2% | **0,941** | **19,6%** |
| rank^3 | 23,84% | +14,88 | 25,7% | −32,4% | 0,928 | 13,6% |
| top 15 | 22,99% | +13,54 | 26,9% | −35,7% | 0,855 | 6,7% |
| **rank^2** | **22,92%** | **+13,97** | 25,1% | −33,7% | 0,913 | 10,4% |
| mitad alta del top20 | 22,36% | +12,99 | 25,3% | −35,7% | 0,884 | 7,2% |
| rank^1,5 | 22,29% | +13,34 | 24,8% | −34,3% | 0,899 | 8,7% |
| top 5 | 21,62% | +13,11 | 26,5% | −33,1% | 0,816 | 20,0% |
| **rank^1 (actual)** | **21,51%** | +12,55 | 24,3% | −34,8% | 0,885 | 7,0% |
| proporcional a m12 | 21,00% | +12,04 | 24,1% | −34,4% | 0,871 | 12,3% |
| rank / volatilidad | 20,94% | +11,98 | 24,5% | −32,6% | 0,855 | 8,6% |
| capitalización inversa | 20,81% | +11,85 | 27,0% | −34,9% | 0,771 | 12,0% |
| rank^0,5 | 20,55% | +11,59 | 23,9% | −35,3% | 0,860 | 5,3% |
| **rank^0 (equiponderado)** | **19,41%** | +10,45 | 23,5% | −35,7% | 0,826 | 3,7% |
| volatilidad inversa | 18,77% | +9,81 | 23,7% | −33,5% | 0,792 | 8,0% |
| **capitalización (como el S&P)** | **18,46%** | +9,50 | 24,2% | −36,3% | 0,763 | 8,2% |
| rank^−1 *(control)* | 16,76% | +7,81 | 24,1% | −37,0% | 0,695 | 25,6% |
| mitad baja del top20 | 15,86% | +7,34 | 25,2% | −35,8% | 0,629 | 7,5% |
| rank^−2 *(control)* | 14,52% | +5,56 | 27,5% | −40,0% | 0,528 | 62,2% |

**La escalera es perfectamente monótona en los nueve niveles de inclinación**, de −2 a +5, y los
controles negativos caen exactamente donde deben. Ponderar por capitalización, como hacen el
S&P y el NASDAQ, es de lo peor de la tabla: **−0,95 pp frente a equiponderar.** Ahí no hay alfa
escondido; la había en la dirección contraria.

---

## 2. ¿Es real? Permutación

Barajo al azar qué acción ocupa cada puesto dentro del año y recalculo. 400 simulaciones.

| Comparación | Observado | Desv. típica nula | p |
|---|---|---|---|
| rank^1 vs equiponderado | +2,10 pp | 0,99 pp | **0,015** |
| **rank^2 vs equiponderado** | **+3,51 pp** | 1,55 pp | **0,010** |
| rank^5 vs equiponderado | +5,53 pp | **2,69 pp** | 0,018 |

Los tres pasan, pero fíjate en la columna del medio: **la banda de ruido crece con la
inclinación.** A `rank^5`, inclinar al azar te da ±2,7 pp de CAGR por pura suerte de
concentración. El +5,53 pp sólo son dos desviaciones típicas. `rank^2` tiene el p más limpio
(0,010) precisamente porque su ruido es la mitad.

---

## 3. Pero el mecanismo NO es el que parece

Aquí es donde el hallazgo se estropea. La correlación de rangos entre momentum y retorno
futuro **dentro del grupo ya seleccionado**:

| | Valor |
|---|---|
| Spearman global | **0,0555** |
| Años con correlación positiva | **10 de 19** |
| Rho medio por año | 0,043 |
| t | **1,06** |

Diez años de diecinueve es una moneda al aire. **No hay un gradiente fiable acción a acción.**

Y desglosando por cuartil de momentum dentro del top 20%:

| Cuartil | n | Momentum medio | Exceso **MEDIO** | Exceso **MEDIANO** | % gana al SPY | Mejor del grupo |
|---|---|---|---|---|---|---|
| 1 (bajo) | 144 | +42% | +7,93 | +2,97 | 53,5% | +278% |
| 2 | 138 | +55% | +8,64 | +2,88 | 53,6% | +288% |
| 3 | 132 | +74% | +12,37 | **+11,00** | 58,3% | +260% |
| 4 (alto) | 127 | +142% | **+17,96** | +8,44 | 58,3% | **+586%** |

- La **media** sube monótona: 7,93 → 17,96.
- La **mediana** no: el cuartil 3 (+11,00) **bate al cuartil 4** (+8,44).
- El **porcentaje de aciertos** no tiene cuatro escalones, tiene dos: 53,5 / 53,6 / 58,3 / 58,3.
- El mejor nombre del cuartil 4 hizo **+586%**; en los otros tres, entre +260% y +288%.

**Toda la ventaja del cuartil alto vive en la cola derecha.** Es exactamente la misma trampa que
tumbó el frog-in-the-pan hace dos pruebas, y la regla del preregistro dice mediana y geométrica,
no media aritmética.

Lo que sí es real es un efecto de **dos niveles, no de cuatro**: la mitad alta del top 20% acierta
un 58,3% de las veces y la mitad baja un 53,5%. Eso sí aparece en la mediana y en la tasa de
acierto. Lo que no existe es el gradiente fino que justificaría inclinar mucho.

---

## 4. Y el sesgo de supervivencia pega justo aquí

Una ventaja que vive en la cola derecha es **la más frágil posible** en un panel del que se han
borrado las empresas que desaparecieron. En los datos, de las 541 seleccionadas ninguna se fue
a cero. En la realidad, algunas se van.

Cuanto más inclinas, más depende el resultado de un puñado de nombres, y más te duele que la
muestra haya eliminado los desastres. **`rank^5` con un 19,6% en un solo valor pequeño es
precisamente la configuración que peor envejecerá cuando arreglemos los delistings.**

---

## 5. Veredicto

**Pasar de `rank^1` a `rank^2`.** Es lo que se puede defender:

| | Actual (rank^1) | Propuesto (rank^2) | Diferencia |
|---|---|---|---|
| CAGR | 21,51% | 22,92% | **+1,41 pp** |
| Volatilidad | 24,3% | 25,1% | +0,8 pp |
| Retorno/Vol | 0,885 | 0,913 | +0,028 |
| Peso máximo medio | 7,0% | 10,4% | +3,4 pp |
| p frente a equiponderar | 0,015 | **0,010** | — |

**Lo que NO recomiendo**, aunque salga arriba en la tabla:

- **`rank^5`** (24,94%): la mejora sobre `rank^2` son +2,0 pp con un ruido de ±2,7 pp. Está
  dentro del error. Y mete casi un 20% en un solo nombre.
- **top 10** (25,58%): el CAGR más alto de todos, pero con **31,6% de volatilidad** — el peor
  ret/vol de la tabla junto con cap-weighted. Es más rentabilidad comprada con más riesgo, no
  alfa. Además `top 5` rinde *menos* que `top 10`, lo que delata cuánto de esto es azar.

**Y un descarte firme:** ponderar por capitalización rinde 18,46% frente al 19,41% de
equiponderar. La intuición de que ahí había alfa por imitar al S&P y al NASDAQ era **incorrecta,
y en la dirección contraria.**

---

## 6. Aviso de método

Se han probado 19 esquemas sobre la misma muestra. Aunque la monotonía de la escalera y los
controles negativos ayudan mucho, esos nueve niveles **no son nueve pruebas independientes**:
`rank^1` y `rank^1,5` seleccionan casi la misma cartera. Es una señal vista a nueve resoluciones,
no nueve confirmaciones.

Con eso: el efecto de inclinar es real (p≈0,01), su tamaño defendible es **+1,4 pp**, y el resto
de la tabla es cola y suerte.
