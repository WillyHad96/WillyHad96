# ¿Hay charco donde pescar? Las colas del universo cíclico

Descriptivo, no prueba ninguna regla: mide **el premio disponible** y **si es alcanzable**.
Scripts: `colas.py`, `pescable.py`, `concentracion.py`. Datos: `universo_sectorizado.csv`
(8.831 eventos, 3.924 cíclicos / 4.907 no cíclicos, 2007–2023).

## Resumen en una frase

**Hay charco y hay peces enormes — el decil superior de las cíclicas compone al 101,7%
anual — pero ninguna variable del panel dice cuáles son: el AUC de todas está entre 0,44 y
0,57, y el del momento, que es nuestra variable de selección, es 0,482.**

---

## 1. La cola existe, y la cíclica es más gorda

Retorno anual por evento, agrupando los 17 años:

| grupo | n | p1 | p10 | p25 | **p50** | p75 | **p90** | **p95** | **p99** | media |
|---|---|---|---|---|---|---|---|---|---|---|
| **cíclicas** | 3.924 | −77,5 | −38,3 | −16,7 | **7,4** | 35,4 | **69,9** | **99,5** | **205,9** | 14,8 |
| no cíclicas | 4.907 | −72,5 | −34,8 | −14,4 | 6,3 | 31,1 | 63,3 | 90,4 | 190,1 | 13,3 |

Asimetría 3,46 (cíclicas). **La cola alta cíclica es más gorda que la no cíclica en todos los
percentiles superiores**: +6,6 pp en p90, +9,1 pp en p95, +15,8 pp en p99.

## 2. Y correlaciona menos cuanto más arriba

Correlación de cada percentil anual con el Nasdaq:

| | p10 | p25 | p50 | p75 | **p90** | **p95** | **p99** |
|---|---|---|---|---|---|---|---|
| **cíclicas** | 0,734 | 0,807 | 0,855 | 0,881 | **0,855** | **0,825** | **0,715** |
| no cíclicas | 0,799 | 0,821 | 0,840 | 0,899 | 0,898 | 0,857 | 0,814 |

**La cola alta cíclica correlaciona menos que su propia mediana (0,715 vs 0,855) y menos que
la cola alta no cíclica en todos los percentiles superiores.** Es la primera vez en toda la
serie que las cíclicas se ven estructuralmente distintas.

*Con n=17 el IC de 0,715 es aproximadamente [0,35, 0,89] y el de 0,855 [0,63, 0,95]: se
solapan. La dirección es consistente, la diferencia no está establecida.*

## 3. Y paga en los años malos del Nasdaq

| año | Nasdaq | CIC p50 | **CIC p90** | NOC p90 |
|---|---|---|---|---|
| 2008 | **−31,2%** | −45,3 | −3,6 | +1,3 |
| 2015 | **−2,5%** | −19,5 | +16,6 | +22,8 |
| **2022** | **−16,1%** | +3,4 | **+53,7** | +35,6 |

En 2022 la cola alta cíclica batió al Nasdaq por **69,8 pp**. El p90 cíclico bate al Nasdaq
**17 años de 17**, con un exceso medio de **+47,6 pp**.

**Conclusión de las secciones 1–3: el charco existe, es más rico en cíclicas, y su cola paga
cuando el índice no. La intuición era correcta.**

---

## 4. Pero la cola no es pescable con lo que tenemos

Perfil **previo** del decil superior frente al resto. AUC = probabilidad de que un evento de
la cola tenga la variable más alta que uno del resto. **0,5 = ninguna capacidad de distinguir.**

| variable (cíclicas) | cola alta | resto | **AUC** | |
|---|---|---|---|---|
| **momento 12m previo** | 30,59 | 17,29 | **0,482** | **nada — peor que una moneda** |
| percentil de capitalización | 0,43 | 0,49 | 0,439 | débil (más pequeño, mejor) |
| pctl sd margen (alto = inestable) | 0,53 | 0,46 | **0,569** | el único con algo |
| pctl sd crecimiento | 0,52 | 0,49 | 0,527 | nada |
| percentil regla 40 | 0,47 | 0,46 | **0,500** | exactamente nada |

**Y aquí hay una trampa que conviene no volver a pisar.** El momento medio de la cola alta es
30,59% frente a 17,29% del resto: parece una señal enorme. **Pero su AUC es 0,482.** La
diferencia de medias la producen los mismos valores extremos que se intentan predecir, no una
separación real. Media y AUC dicen cosas opuestas, y la que vale es el AUC.

Lo confirma el corte por deciles de momento previo dentro de cíclicas: D1 (menor momento)
10,7%, D10 (mayor) 12,4%, D2 12,6%, D6 8,2%. **Plano y sin orden. El momento no ordena
retornos en este pool.**

El único con señal es la **inestabilidad** (AUC 0,569) — que es justo lo que nuestro filtro
usa para **excluir**. Coincide con C13, y con su precio: da acceso a la cola y destruye la
mediana.

## 5. Todo el retorno está en la cola

| cíclicas | CAGR | media |
|---|---|---|
| pool completo | **11,83%** | 15,1% |
| quitando el 10% superior | **1,49%** | 4,2% |
| quitando el 5% superior | 5,15% | 8,0% |
| solo el 10% superior | **101,71%** | — |

**Quitar el decil superior se lleva 10,34 pp de los 11,83.** El 87% del retorno del pool está
en el 10% de los nombres.

## 6. La consecuencia práctica: concentrar es comprar lotería

Si la cola vale el 87% del retorno y no se puede predecir, el tamaño de la cartera decide
casi todo. Carteras **aleatorias** del pool cíclico, 3.000 simulaciones por tamaño:

| nombres | CAGR mediano | p10 | p90 | corr Nasdaq | **% que bate al Nasdaq** |
|---|---|---|---|---|---|
| 5 | 10,05% | 4,2 | 16,2 | 0,686 | **19%** |
| **15** | **11,19%** | **7,8** | **14,8** | 0,790 | **16%** |
| 20 | 11,44% | 8,5 | 14,6 | 0,806 | 14% |
| 50 | 11,71% | 10,0 | 13,5 | 0,840 | 4% |
| 200 | 11,83% | 11,5 | 12,2 | 0,859 | 0% |

Nasdaq en esos años: **14,05%**.

**Concentrar no sube la rentabilidad esperada: sube la dispersión.** Con 15 nombres la mediana
baja a 11,19% y la probabilidad de batir al Nasdaq es del **16%**. Con 200 es del 0%, pero la
mediana es mejor. **Concentrar compra un billete de lotería con un 16% de premio, no una
ventaja.**

Y hay un agravante conocido: el panel **no registra las muertes** (A1), así que la cola
izquierda real es peor que la medida. **La lotería es peor de lo que sale aquí.**

## 7. Respuesta a la pregunta

> *"Mira las colas superiores e inferiores, porque lo que interesa es apuntar a la cola alta
> y que tenga descorrelación y más rentabilidad, para saber si hay charco donde pescar."*

- **¿Hay charco?** Sí, y es rico: p99 = 205,9%, decil superior componiendo al 101,7%.
- **¿La cola alta descorrelaciona?** Sí, direccionalmente: 0,715 en p99 frente a 0,855 en la
  mediana, y menos que la cola no cíclica en todos los percentiles altos.
- **¿Y más rentabilidad?** Sí: el p90 bate al Nasdaq 17 de 17 años, +47,6 pp de media.
- **¿Se puede pescar?** **No con lo que hay en el panel.** AUC 0,44–0,57 en todas las
  variables, 0,482 en el momento, 0,500 exacto en la regla 40.

**El problema deja de ser "qué filtro tocar" y pasa a ser "no tenemos ninguna variable que
vea la cola".** Eso es una pregunta distinta, y mejor planteada.

## 8. Qué haría falta ahora

Ya no es tocar filtros. Es **variables que separen la cola**, y ninguna está en el panel:

1. **Aceleración de ingresos y sorpresa frente a expectativas** — están en el panel
   (`aceleracion_pp`, `sorpresa`, `racha`, `guia_implicita`) y **nunca se han medido con AUC
   contra la cola.** Es lo más barato que queda y se hace hoy.
2. **Revisiones de estimaciones de analistas** (FMP `analyst/historical-grades`, mensual).
   Es la variable clásica para cola alta y no está en el panel.
3. **Compras de insiders** (FMP `insiderTrades`, trimestral desde 1997, ya verificado como
   disponible en `AGENDA-ESTUDIOS.md`).

El criterio de éxito para cualquiera de ellas es ahora explícito y medible: **AUC > 0,60
contra el decil superior, replicado en pares e impares.** Nada de lo probado hasta hoy pasa
de 0,57.
