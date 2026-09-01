# Por qué la segunda mitad parece tan superior — y por qué no hay que creérselo

Pregunta de partida: C4 pierde contra el NASDAQ por 1,68 pp en 2007–2015 y le gana por
7,42 pp en 2016–2023. ¿Es que entran empresas distintas — más software, menos cíclicas?

**Respuesta corta: no. La composición apenas se mueve, y la brecha entre mitades no es
distinguible del ruido (p = 0,105).**

## Nota sobre la reconstrucción

El backtest original de C4 no quedó guardado en ningún script, así que lo he reconstruido
en SQL desde la especificación de `ESTUDIO-ALFA-POST-DELISTINGS.md` §7. Da **14,16%** de
CAGR frente al 15,42% documentado, con ~40 nombres/año frente a ~38. No es idéntico —
algún detalle del original difiere — pero reproduce la estructura: pierde contra el NASDAQ
en la primera mitad, gana en la segunda. Lo uso para **comparar composición**, no para
reemplazar la cifra de cabecera.

| | reconstrucción | documentado |
|---|---|---|
| CAGR 2007–2023 | 14,16% | 15,42% |
| 2007–2015 vs NASDAQ | −3,69 pp | −1,68 pp |
| 2016–2023 vs NASDAQ | +5,31 pp | +7,42 pp |

## 1. La composición sectorial casi no cambia

Peso en cartera (ponderación rank²), y exceso medio vs NASDAQ dentro de cada sector:

| sector | peso H1 | peso H2 | dif | exc H1 | exc H2 |
|---|---|---|---|---|---|
| (sin sector) | 35,1% | 30,8% | −4,3 | −7,8 | −8,9 |
| Technology | 17,6% | 19,1% | **+1,5** | +5,9 | +14,7 |
| Consumer Cyclical | 17,1% | 10,9% | −6,2 | +1,9 | +3,0 |
| Industrials | 11,3% | 13,4% | +2,1 | −0,8 | +2,9 |
| Healthcare | 7,5% | 8,0% | +0,5 | −2,0 | +0,7 |
| Consumer Defensive | 3,2% | 6,6% | +3,4 | +2,4 | +8,7 |
| Basic Materials | 3,9% | 3,3% | −0,6 | +7,9 | +5,0 |
| resto | 5,3% | 7,9% | +2,6 | | |

- **Tecnología sube 1,5 pp de peso.** Nada.
- **Cíclicas (ConsCyc + Industriales + Materiales + Energía): 33,1% → 28,6%.** Bajan.

O sea: en la segunda mitad la cartera es *marginalmente menos cíclica* y *marginalmente
más tecnológica*, pero ninguno de los dos cambios tiene tamaño para explicar nada.

Descomposición tipo Brinson de la parte de la brecha atribuible a sectores (+1,74 pp):

| fuente | aportación |
|---|---|
| cambiar de sectores (asignación) | +0,53 pp (30%) |
| los mismos sectores rindiendo más (selección) | +1,21 pp (70%) |

Y esos +1,74 pp son una fracción pequeña de los +7,64 pp de brecha total. **La rotación
sectorial no es la explicación.**

## 2. La explicación es 2008–2009

Exceso anual vs NASDAQ:

| año | exceso | | año | exceso |
|---|---|---|---|---|
| 2007 | −1,46 | | 2016 | +8,55 |
| **2008** | **−13,68** | | 2017 | −4,32 |
| **2009** | **−15,73** | | 2018 | +10,75 |
| 2010 | +3,71 | | 2019 | −1,25 |
| 2011 | +3,77 | | 2020 | +8,10 |
| 2012 | +3,47 | | 2021 | −10,27 |
| 2013 | +6,16 | | **2022** | **+21,44** |
| 2014 | −8,34 | | 2023 | +5,99 |
| 2015 | −2,79 | | | |

- H1 media **−2,77 pp**, H2 media **+4,87 pp**, brecha **+7,64 pp**.
- **Quitando solo 2008 y 2009, H1 pasa a +0,65 pp y la brecha se reduce a +4,23.**
  Esos dos años aportan el **45%** de toda la diferencia.
- Los tres años que más pesan en la brecha son 2022 (+21,4), 2009 (−15,7) y 2008 (−13,7).

Qué pasó en esos dos años: en 2008 la cartera cayó **−42,5%** frente a −28,8% del NASDAQ,
y en 2009 subió **+27,2%** frente a **+42,9%**. Es el patrón clásico de una estrategia de
calidad + momentum en un crash seguido de un rebote de basura: cae con todo y se pierde
el rebote porque el momentum a 12 meses todavía apunta a lo que funcionaba antes.

Beta contra el NASDAQ: **1,06 en H1, 0,85 en H2.**

## 3. Y la brecha no es significativa

| | media | desv. típica | n |
|---|---|---|---|
| H1 2007–2015 | −2,77 pp | 8,1 | 9 |
| H2 2016–2023 | +4,87 pp | 9,9 | 8 |

Permutación de los 17 años entre las dos mitades, 20.000 iteraciones:
**p = 0,105.**

Con 9 y 8 observaciones anuales y una desviación típica de ~9 pp, una brecha de 7,6 pp
entra dentro de lo que produce el azar. **No hay base para decir que la estrategia
"funciona mejor en la segunda mitad".** Lo que hay es una muestra con un crash en una
mitad y no en la otra.

## 4. Lo que sí aparece: un tercio de la cartera sin clasificar

El bucket "sin sector" pesa **30–35% de la cartera** y rinde **−8 a −9 pp vs NASDAQ en
las dos mitades**. Es el mayor lastre identificado, y es consistente.

| grupo | n eventos | tickers | ret medio | exceso vs NASDAQ |
|---|---|---|---|---|
| con sector, viva | 467 | 314 | +20,1% | **+2,9** |
| sin sector, desaparecida | 79 | 49 | +9,0% | **−5,2** |
| sin sector, viva | 118 | 73 | +2,8% | **−10,7** |

Dos cosas que salen de aquí:

1. **Ninguna empresa con sector está desaparecida.** Confirma que el campo `sector` se
   rellenó retroactivamente solo para supervivientes: es el look-ahead ya documentado,
   ahora visible en los datos.
2. **"Sin sector" no es sinónimo de "muerta ni de basura".** Los 73 tickers vivos sin
   sector son empresas normales y reconocibles — SKX, TPX, MASI, GES, BGS, DENN, PLAY,
   SSTK, BLD, JBT, AMED… El campo simplemente no se rellenó. Y son los que **peor**
   rinden (−10,7 pp), peor incluso que los desaparecidos.

Que un tercio del peso de la cartera esté en un bucket sin clasificar y que ese bucket
sea el que peor rinde es un problema de datos más grande que cualquiera de los factores
probados en esta sesión. Rellenar `sector` para esos 122 tickers pasa a ser prioridad.

## Conclusión

- No es software. No es dejar de ser cíclica. La composición es estable.
- La brecha entre mitades es, en gran parte, el crash de 2008 y el rebote de 2009.
- Y no es estadísticamente distinguible del ruido.

La lectura correcta de C4 no es "pierde en la primera mitad y gana en la segunda", sino
**"tiene un exceso medio pequeño contra el NASDAQ y una muestra demasiado corta para
decir más"**. Lo que sí sobrevive en las dos mitades sigue siendo lo de siempre: pasar
el filtro bate a no pasarlo.
