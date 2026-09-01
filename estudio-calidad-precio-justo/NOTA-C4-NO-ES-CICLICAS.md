# C4 no es "las cíclicas": dos objetos bajo una misma etiqueta

Corrección de encuadre. En la conversación y en varios documentos se ha usado "las
cíclicas" para referirse a la estrategia cuyo alfa se mide (C4, +15,4%). **No son lo mismo.**

## 1. Los dos objetos

**C4** (`ESTUDIO-ALFA-POST-DELISTINGS.md` §7): universo de bolsa estadounidense entre
300 M$ y 5.000 M$, **sin filtro de sector**, filtros de *estabilidad* (desviación típica del
margen bruto y del crecimiento en 8 trimestres por debajo de la mediana), regla 40 y
capitalización, selección por momento a 12 meses. Es de donde salen el 15,4%, el 14,16% de
la reconstrucción y la correlación de 0,92 con el Nasdaq.

**"Las cíclicas"** (`ciclicas_eventos.txt`, 194 eventos, 129 tickers): el **subconjunto** de
C4 cuyo sector es Consumer Cyclical, Industrials, Basic Materials o Energy. Se recortó en
`sect.py` / `interim.py` para comprobar si el efecto de la deuda se sostenía dentro de los
sectores cíclicos, y ese mismo recorte se reutilizó después en el estudio de ROIC/FCF
(`deuda_cic.csv` 190 + `deuda.csv` 74 = 264 eventos).

Así que los tres últimos estudios (deuda piloto, deuda cíclicas, ROIC/FCF) corren sobre
**una rebanada** de C4. El alfa y la correlación se miden sobre **el todo**. El error ha sido
no separar las dos cosas cada vez que se cambiaba de una a otra.

## 2. Por qué incluso la rebanada cíclica se parece al Nasdaq

Los filtros de C4 seleccionan **baja volatilidad de fundamentales**. Dentro de los cuatro
sectores cíclicos:

| | sd(margen bruto) 8T |
|---|---|
| nombres que pasan el filtro | **1,41 pp** |
| nombres que lo fallan | **4,76 pp** |

Los que pasan tienen **3,4 veces menos** volatilidad de margen. El filtro escoge, por
construcción, a los miembros *menos cíclicos* de los sectores cíclicos: Ross, Tractor
Supply, Ulta, Pool, Middleby, TransDigm, Watsco, LKQ. Etiqueta sectorial cíclica,
economía de compounder.

**El compartimento nunca fue "exposición a cíclicas". Fue "negocios estables que casualmente
están en sectores cíclicos".**

## 3. Pero las dos mitades de C4 sí se comportan distinto

Partiendo C4 por sector (ponderación rank² dentro de cada mitad, feb–feb, 2007–2023):

| | corr Nasdaq | beta Nasdaq | corr S&P | beta S&P | CAGR | desv. |
|---|---|---|---|---|---|---|
| mitad de sectores cíclicos (~47% del peso) | +0,836 | 0,89 | **+0,880** | 1,14 | 12,36% | 23,5 |
| mitad del resto | +0,849 | 1,02 | +0,770 | 1,13 | 14,64% | 26,7 |

**Correlación entre las dos mitades: solo +0,68.** La mitad cíclica correlaciona *más* con el
S&P que con el Nasdaq; la otra, al revés.

Años en que divergen más de 20 pp:

| año | mitad cíclica | resto | Nasdaq | S&P |
|---|---|---|---|---|
| 2008 | **−49,9** | −23,4 | −28,8 | −40,2 |
| 2011 | +22,4 | −6,9 | +9,8 | +3,0 |
| 2018 | −9,7 | **+36,0** | +4,0 | +2,1 |
| 2020 | +40,3 | +67,0 | +48,4 | +24,1 |
| 2021 | **+14,6** | −16,5 | +6,9 | +11,0 |
| 2022 | **+15,6** | −9,4 | **−19,9** | −10,2 |

Eso **sí** es comportamiento cíclico: cae más en 2008, se desacopla del Nasdaq en 2021–2022
(los años de value y energía). La intuición era correcta *para esa mitad*.

## 4. Por qué el 0,92 del conjunto es más alto que el de cada mitad

Dos series con correlación 0,68 entre sí y ~0,84 cada una con el índice, al promediarse,
cancelan ruido idiosincrático y la mezcla sigue al mercado más de cerca. Es aritmética de
diversificación, no un fallo de medición.

Y una cosa más general: **a frecuencia anual, cualquier cesta de acciones americanas
correlaciona 0,8–0,95 con cualquier índice americano.** El S&P y el Nasdaq correlacionan
0,94 entre sí en estos mismos datos. La correlación anual mide "¿es bolsa de EE.UU.?", no
"¿es cíclica?". Para eso sirven la beta y los años de divergencia, y esos sí distinguen.

## 5. Qué cambia

- **Las conclusiones de los estudios de deuda y ROIC/FCF aplican a la rebanada cíclica, no a
  C4.** Queda anotado como alcance.
- **`ESTUDIO-CARTERAS.md` mide C4 completo.** Su conclusión ("no diversifica del Nasdaq") es
  correcta para el todo, pero incompleta: la mitad cíclica es un objeto distinto, con
  correlación 0,84 y desacoplamiento real en años de value.
- **Si se quiere un compartimento cíclico de verdad**, C4 entero no lo es. La mitad cíclica
  de C4 se acerca, pero sigue siendo "calidad dentro de cíclicas". Exposición cíclica pura
  exigiría *quitar* el filtro de estabilidad, que es justo lo que C4 penaliza.
- **Descripción honesta de C4:** small/mid cap USA de calidad y momento, todos los sectores,
  ~47% en sectores cíclicos, comportamiento agregado tipo Nasdaq, con una mitad que se
  desacopla en años de value.

## Ficheros

- `dos_mitades_c4.py` — correlaciones, betas, años de divergencia y volatilidad de margen.
