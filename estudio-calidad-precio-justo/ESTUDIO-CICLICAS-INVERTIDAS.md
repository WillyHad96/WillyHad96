# ¿Qué nos estaban quitando los filtros de las cíclicas?

Pre-registrado en `PREREGISTRO-CICLICAS-INVERTIDAS.md` (regla + adenda), comiteado antes de
mirar la confirmación. Scripts: `criba_ciclicas.py`, `confirmacion_ciclicas.py`, `tamano.py`.
Datos: `ciclicas_pares.csv` (1.830 ev.), `ciclicas_impares.csv` (2.094 ev.).

## Resumen en una frase

**Los filtros no eran el problema. El universo cíclico entero, sin ningún filtro, rinde
2,50 pp menos que el Nasdaq con correlación 0,862 — así que no hay giro de filtros que saque
de ahí rentabilidad y descorrelación a la vez.**

---

## 1. El dato que ordena todo lo demás

Las 231 cíclicas de cada año, equiponderadas, **sin aplicar ninguno de nuestros filtros**:

| muestra | n/año | CAGR cíclicas | Nasdaq | dif | corr |
|---|---|---|---|---|---|
| descubrimiento (pares) | 229 | 10,99% | 8,60% | +2,38 | 0,888 |
| confirmación (impares) | 233 | 12,59% | 19,68% | **−7,09** | 0,882 |
| **los 17 años** | **231** | **11,83%** | **14,33%** | **−2,50** | **0,862** |

**El techo del compartimento cíclico es 2,5 pp por debajo del Nasdaq**, con la misma
correlación de siempre. Optimizar filtros dentro de un charco que rinde menos que el índice
solo puede funcionar si los filtros añaden más de 2,5 pp, y nada de lo probado lo hace.

Nótese también el vuelco entre mitades: **+2,38 pp en pares, −7,09 pp en impares.** Un
columpio de 9,5 pp entre las dos mitades de la misma muestra. Es B6 otra vez, en carne viva.

## 2. Qué quita cada filtro (descubrimiento, años pares)

| variante | n/año | CAGR | corr | azar | real | vs QQQ |
|---|---|---|---|---|---|---|
| todas las cíclicas | 229 | 10,99% | 0,888 | 0,888 | +0,000 | +2,38 |
| estabilidad pasa | 91 | 11,67% | 0,851 | 0,883 | −0,032 | +3,07 |
| estabilidad invertida | 63 | 8,31% | 0,810 | 0,875 | −0,065 | −0,30 |
| r40 pasa / falla | 170/59 | 10,57 / 9,66% | | | +0,006/−0,016 | +1,96/+1,06 |
| mcap pasa | 182 | 9,38% | 0,877 | 0,886 | −0,009 | +0,77 |
| **mcap falla (<p25)** | 46 | **16,16%** | 0,817 | 0,871 | −0,055 | **+7,56** |
| C4 cíclicas completo | 12 | 10,81% | 0,814 | 0,818 | −0,003 | +2,21 |
| **estab. invertida + momento** | 12 | **13,13%** | 0,675 | 0,818 | **−0,142** | **+4,53** |

Lecturas de descubrimiento:

- **La regla 40 no quita casi nada.** Los dos lados rinden casi igual.
- **El momento aporta poco dentro de cíclicas**: top 20% da 11,15% frente a 10,99% del total.
- **El filtro de capitalización quita rentabilidad**: el cuartil pequeño rinde 16,16% frente
  al 9,38% del resto.
- **El filtro de estabilidad quita descorrelación**: invertirlo baja la correlación.

## 3. La confirmación (años impares) — las cuatro reglas fallan

| regla | descubrimiento | confirmación | veredicto |
|---|---|---|---|
| R-A capitalización invertida | 22,34%, real +0,117 | 33,96%, real **+0,304** | **fallo**: n=2, mal especificada |
| R-B estabilidad invertida | 13,13%, real −0,071 | **3,83%**, real **−0,339** | **fallo**: pierde la rentabilidad |
| R-C las dos juntas | 0,64% | **−8,41%** | **fallo** total |
| R-A2 tamaño puro | 16,16%, p=0,007 | 14,78%, **p=0,126** | **fallo**: no bate al Nasdaq (19,68%) |

### R-A estaba mal especificada, y lo digo

El hallazgo era `mcap<=p25` a secas (46 nombres). Al escribir R-A le añadí estabilidad,
regla 40 y top 20% de momento y la dejé en **2 nombres/año**. Su descorrelación real salió
**positiva** (+0,117 y +0,304): dos nombres elegidos sistemáticamente correlacionan **más**
que dos al azar. Se re-cerró como R-A2 en la adenda, antes de calcularla, y R-A2 también
falla.

## 4. El hallazgo estructural: los dos objetivos se pagan el uno al otro

Es lo más útil que sale del estudio, y replica en las dos mitades:

| filtro | qué da al invertirlo | qué cuesta |
|---|---|---|
| **estabilidad** | descorrelación real **−0,071 / −0,339** (replicada) | la rentabilidad: **3,83%** con el Nasdaq al 19,68% |
| **capitalización** | rentabilidad sobre el azar (16,16 vs 10,88; 14,78 vs 12,41) | nada, pero **no descorrelaciona** (real −0,055, ruido) |
| **las dos juntas (R-C)** | nada | **−8,41%** |

**No es que no hayamos encontrado la combinación. Es que las dos palancas empujan en
direcciones opuestas, y juntarlas da lo peor de las dos.** La estabilidad es lo que hace que
el compartimento rinda; quitarla descorrelaciona y hunde el CAGR. Es C7 otra vez, y ahora
sabemos por qué.

## 5. El diagnóstico de supervivencia salió al revés de lo predicho

Predicción declarada en la adenda §12: si el efecto tamaño es sesgo de supervivencia, debe
**encogerse** en 2021–2023, el único tramo donde A1 dice que las bajas están registradas.

| tramo | calidad del registro | media PEQ − RESTO | años positivos |
|---|---|---|---|
| 2007–2014 | **sin muertes registradas** | **+0,25 pp** | 4/8 |
| 2015–2020 | parcial | **+11,75 pp** | **6/6** |
| 2021–2023 | realista | **+6,88 pp** | 2/3 |

**Sale al revés.** El efecto es **cero justo donde el sesgo debería ser máximo** y aparece
donde las muertes sí se registran. Así que el efecto tamaño dentro de cíclicas **no parece
sesgo de supervivencia** — pero tampoco es utilizable: es enteramente posterior a 2015 y lo
dominan dos años, **2020 (+42,6 pp)** y **2022 (+18,9 pp)**. Quitando 2020, el tramo
2015–2020 baja de +11,75 a +5,58 pp.

Una observación honesta más: el número de pequeñas por año crece de 33 (2007) a 64 (2020).
La composición de la muestra cambia con el tiempo (A2), así que parte del patrón temporal
puede ser cobertura del panel, no mercado.

## 6. Respuesta a la pregunta que originó el estudio

> *"¿Qué nos está sacando a las cíclicas de mayor rentabilidad de nuestros propios filtros?
> ¿Puede un giro de uno o dos filtros dar la rentabilidad y la descorrelación que necesito?"*

- **Lo que quitan los filtros está medido**: capitalización quita rentabilidad, estabilidad
  quita descorrelación, regla 40 y momento no quitan casi nada.
- **Pero ningún giro sirve**, y no por falta de haberlo intentado: porque **el pool cíclico
  rinde 2,50 pp menos que el Nasdaq** y las dos palancas que funcionan se anulan entre sí.
- **La hipótesis de partida —"metiéndole volatilidad saco rentabilidad"— queda refutada en
  su mitad importante.** Invertir la estabilidad sube la volatilidad y la descorrelación, y
  **baja** la rentabilidad. Coincide con C6: la volatilidad extra es beta, y la beta se
  compra gratis.

## 7. Lo que sí queda para el futuro

1. **El efecto tamaño merece probarse fuera de cíclicas**, sobre el universo completo. Aquí
   falló, pero el pool cíclico es malo de partida; en el universo entero el punto de partida
   es 14,16%, no 11,83%. **No está probado, y es barato.**
2. **Aplicar el test de ventanas (B8) a este estudio** cuando haya historia más larga.
3. **Filtro de liquidez** antes de tomarse en serio cualquier variante de cuartil pequeño
   (300–700 M$), que sigue sin medirse (`METODOLOGIA-Y-PENDIENTES.md`, Factor 8).
