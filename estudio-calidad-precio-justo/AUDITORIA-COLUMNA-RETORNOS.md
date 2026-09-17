# Auditoría — la barra de medir SÍ estaba rota (pero no donde yo buscaba)

**Fecha:** 2026-09-17
**Scripts:** `calibracion.py`, `auditoria_retornos.py`, `rehacer_con_precios.py`
**Origen:** pregunta del usuario — *"si cosas que están demostradas están fallando, ¿no crees
que igual la barra de medir que estamos utilizando está mal de alguna manera?"*

**Respuesta corta: sí, y tenía razón.** La aritmética está bien. Los **datos de entrada** no.

---

## 1. Primero descarté que el problema fuera el método

`calibracion.py` — control positivo. Plantamos un efecto de tamaño **conocido** en un grupo
aleatorio de 11 nombres/año y comprobamos si el procedimiento de siempre lo recupera.

| efecto plantado | lo que lee la barra | t | ¿lo distingue del ruido? |
|---|---|---|---|
| 0 pp | −0,33 pp | — | ruido SE = 2,15 pp |
| 2,0 pp | +1,69 pp | 0,8 | no |
| 3,5 pp | +3,26 pp | 1,5 | no |
| 5,0 pp | +4,80 pp | 2,2 | sí |
| 7,3 pp | +7,11 pp | 3,3 | sí |
| 10,0 pp | +9,89 pp | 4,6 | sí |
| 15,0 pp | +14,90 pp | 6,9 | sí |

**La barra es insesgada**: le metes 10 y lee 9,89. No infla ni desinfla. Lo único que hace
es no poder separar del ruido lo que mide menos de ~4,5 pp. Eso confirma C31 y descarta que
el método sea el culpable.

Probé también si otra barra mide mejor (mismo efecto de 3,5 pp plantado):

| estimador | ruido (SE) | t |
|---|---|---|
| media (el de siempre) | 2,28 pp | 1,55 |
| mediana | 2,33 pp | 1,45 |
| media winsorizada 10% | 2,09 pp | 1,73 |
| media log(1+r) | 2,08 pp | 1,80 |

Los robustos ganan un 9% de ruido. No cambia nada: 3,5 pp sigue invisible con los cuatro.

---

## 2. Después miré los datos de entrada, y ahí estaba

`auditoria_retornos.py`. La columna `fwd_4t` del panel —**la que hemos usado como retorno en
todos los estudios de la serie**— comparada con el propio `precio_post` del panel, sobre
224.041 observaciones que pasan todas las guardas de calidad:

| medida | valor |
|---|---|
| diferencia mediana | **1,64 pp** |
| diferencia p90 | **8,57 pp** |
| % con diferencia > 2 pp | **44,6%** |
| **% con el SIGNO contrario** | **3,1%** |

Ejemplo literal — DY, 2 de marzo de 2022: `precio_post` va de 90,60 a 97,02, o sea **+7,1%**.
La columna `fwd_4t` dice **−7,1%**. Y DY el 23 de noviembre de 2021: precio de 99,91 a 90,20,
**−9,7%**; la columna dice **+9,7%**.

### 2.1 ¿Cuál de las dos miente? Árbitro independiente

Traje precios de FMP (fuente distinta) y calculé el retorno entre **las fechas exactas del
panel** para 43 observaciones de 6 tickers:

| columna | error mediano vs FMP | error medio vs FMP |
|---|---|---|
| **recalculado desde `precio_post`** | **0,03 pp** | **0,02 pp** |
| `fwd_4t` (la que usábamos) | **2,31 pp** | **4,98 pp** |

**`precio_post` es correcto hasta la centésima. `fwd_4t` no.** Errores de hasta 19,4 pp
(DY 2021), y en ambas direcciones.

No son dividendos: DY no paga dividendo y falla; FRO paga muchísimo y falla **a la baja**
(108,6 reales contra 95,2 de la columna), que es el signo contrario al que daría un dividendo.

---

## 3. Qué pasa cuando se rehace el hallazgo principal con precios verificados

`rehacer_con_precios.py`. Misma muestra de 772 decisiones, mismo filtro (cuartil barato por
P/S dentro de Industrials), única diferencia el origen del retorno:

| columna de retorno | n/año | CAGR | familia | alfa interno | t | pares | impares |
|---|---|---|---|---|---|---|---|
| `fwd_4t` (lo de siempre) | 11 | 16,63% | 10,75% | **+5,89 pp** | 2,66 | 6,5 | 5,3 |
| **recalculado desde `precio_post`** | 11 | 16,77% | 11,25% | **+5,52 pp** | **2,37** | **5,6** | **5,4** |

**El hallazgo sobrevive, y replica mejor**: 5,6 / 5,4 entre mitades, contra 6,5 / 5,3 antes.
Es el resultado más limpio que ha dado la serie.

Con la muestra completa de 990 decisiones (sin exigir que haya key-metrics de FMP):

| anchura | n/año | CAGR | familia | alfa interno | t | pares | impares | suelo |
|---|---|---|---|---|---|---|---|---|
| 15% | 9 | 24,62% | 13,47% | +11,15 pp | 3,62 | 16,8 | 6,3 | 6,2 pp |
| **25%** | **14** | **19,49%** | **13,47%** | **+6,02 pp** | **2,66** | 9,1 | 3,3 | 4,5 pp |
| 35% | 20 | 17,21% | 13,47% | +3,74 pp | 2,08 | 6,8 | 1,1 | 3,6 pp |
| 50% | 29 | 16,56% | 13,47% | +3,09 pp | 2,31 | 3,6 | 2,6 | 2,7 pp |

**Aviso honesto:** el equilibrio entre mitades se mueve con la definición de la muestra
(5,6/5,4 con 772 obs, 9,1/3,3 con 990). El efecto está; su estabilidad no es tan sólida como
parecía con una sola muestra.

---

## 4. Lo que NO cambia: el suelo de detección

Mismo cálculo de ruido con cada columna, 772 obs, 11 nombres:

| columna | SE | suelo (t=2) |
|---|---|---|
| `fwd_4t` (corrupta) | 2,20 pp | 4,4 pp |
| `precio_post` (verificada) | 2,26 pp | 4,5 pp |

**El error de medición no inflaba el suelo.** Es idiosincrásico y se promedia dentro de una
cartera de 11 nombres. Así que C31 sigue en pie tal cual: el problema de fondo sigue siendo
17 años y pocos nombres, no la calidad del dato.

---

## 5. Consecuencias

1. **`fwd_4t` no se vuelve a usar.** Todo retorno se recalcula desde `precio_post`, que está
   verificado contra fuente externa. `c4_base.sql` debe cambiar `f4r` por
   `p4/precio_post - 1`, manteniendo las mismas guardas.
2. **Toda la serie anterior usó la columna corrupta.** Los estudios A1–C31 se midieron con
   ella. El hallazgo principal aguanta la corrección; **los demás no se han vuelto a medir**.
   Los números publicados de esos estudios hay que tratarlos con un margen de ±2 pp mientras
   no se rehagan.
3. **La intuición del usuario era correcta y mi enfoque anterior era incompleto:** yo había
   auditado cobertura temporal, delistings, forward-fill y duplicados, pero **nunca comprobé
   que la columna de retorno cuadrase con la columna de precios del propio panel**. Es la
   comprobación más barata que existe y no la había hecho.
4. **No es la explicación de "no sale nada".** Tentador, pero falso: §4 lo descarta. El suelo
   de detección manda igual.

---

## 6. Nota de operación

El proyecto de Supabase estaba en `INACTIVE` (pausado por inactividad) y lo reactivé para
poder hacer esta auditoría. Durante el arranque (`COMING_UP`) la base responde con **cero
tablas**, lo cual asusta pero es transitorio: al terminar, `hypergrowth_panel` tenía sus
431.259 filas intactas. Si vuelve a pasar, esperar y volver a consultar antes de alarmarse.
