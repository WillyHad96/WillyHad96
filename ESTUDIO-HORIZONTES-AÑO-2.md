# La rejilla completa: mes de entrada × horizonte de 12 a 24 meses

El año 2 sólo se había mirado a nivel de evento y el backtest de cartera lo había desmentido
sin cerrarlo bien. Aquí está cerrado: **4 meses de entrada × 5 horizontes (12, 15, 18, 21 y 24
meses)**, 2007–2023.

El resultado principal no es sobre el horizonte. Es sobre **de dónde viene realmente la ventaja.**

---

## 0. Antes: dos problemas de datos que hubo que resolver

### 0.1 Defecto 9 (nuevo): `fwd_1t`, `fwd_2t` y `fwd_4t` no son encadenables entre sí

Para medir horizontes de 15, 18 y 21 meses hacía falta un índice de referencia trimestre a
trimestre. La vía natural era encadenar `fwd_1t`. No funciona:

| Encadenando 4 × `fwd_1t` contra `fwd_4t` | Correlación | Error mediano |
|---|---|---|
| Para la **acción** | 0,518 | 2,67 pp |
| Para el **SPY** | 0,890 | 3,10 pp |

Si ni siquiera la acción encadena consigo misma, los tres campos no comparten definición de
ventana. **Sólo son fiables los horizontes múltiplos de 4 trimestres**, que son los que el
estudio venía usando.

*Solución adoptada:* el banco de pruebas pasa a ser el **universo elegible completo**, calculado
exactamente igual que la cartera (`lead(precio_post,k)`), con las mismas guardas y la misma
ventana. Es autoconsistente a cualquier horizonte y elimina el desajuste de ventanas.

### 0.2 Un susto: correlación 0 entre el panel y mis propios cálculos

`corr(fwd_4t, precio(t+4)/precio(t)−1)` daba **−0,0006**. Alarma total. Causa real: **45 filas
de 231.443** con precios disparados por el retroajuste de contrasplits. Acotando rangos:

| | Valor |
|---|---|
| Pearson acotado | **0,9866** |
| Spearman | **0,9901** |
| Dentro de 5 pp | 80,6% |

El panel es coherente. Pero conviene retener la lección: **una correlación de Pearson sobre estos
datos sin acotar no significa nada.**

---

## 1. La rejilla

### Rentabilidad anualizada de la cartera (geométrica, 2007–2023)

| Entrada | 12m | 15m | 18m | 21m | 24m |
|---|---|---|---|---|---|
| Febrero | 18,10% | 17,79% | 18,77% | 14,55% | 17,80% |
| Mayo | 14,28% | 15,00% | 13,57% | 16,43% | 16,22% |
| Agosto | 16,94% | 13,42% | 16,24% | 16,06% | 17,10% |
| Noviembre | 15,84% | 18,77% | 16,96% | 19,27% | 17,66% |
| **4 tramos** | **16,84%** | **16,72%** | **16,78%** | **16,90%** | **17,43%** |

La fila de los cuatro tramos es asombrosamente plana: 16,7% a 17,4% en todo el rango. Las filas
individuales saltan mucho más (13,4% a 19,3%), y ese salto es **ruido de la fecha concreta**, no
señal del horizonte.

### Ventaja anualizada sobre el universo elegible (pp)

| Entrada | 12m | 15m | 18m | 21m | 24m |
|---|---|---|---|---|---|
| Febrero | +3,84 | +3,49 | +3,76 | +1,46 | +2,65 |
| Mayo | +1,05 | +1,11 | +1,49 | +1,75 | +1,78 |
| Agosto | +3,77 | +2,44 | +2,44 | +2,56 | +2,50 |
| Noviembre | +1,47 | +1,45 | +1,03 | +2,38 | +1,15 |
| **4 tramos** | **+2,32** | **+2,03** | **+2,20** | **+2,13** | **+2,06** |
| **Media** | **+2,53** | +2,12 | +2,18 | +2,04 | **+2,02** |

### El decaimiento existe pero no se distingue del ruido

- Caída de 12m a 24m: **−0,51 pp** (un −20% de la ventaja)
- Dispersión entre meses de entrada **dentro de un mismo horizonte**: **1,48 pp**

**El efecto del horizonte es tres veces más pequeño que el efecto de en qué mes entras.** No hay
base para decir que 24 meses sea peor que 12. Tampoco mejor.

---

## 2. El hallazgo de verdad: de dónde sale la ventaja

Descomponiendo el 12m de febrero:

| | CAGR | Aporta |
|---|---|---|
| S&P 500 (sólo precio, 2007–2024) | 8,63% | — |
| **Universo elegible** (300M–5B + perfil de estabilidad) | **14,26%** | **+5,63 pp** |
| **Cartera** (top 20% por momentum) | **18,10%** | **+3,84 pp** |
| | | **= 9,47 pp** |

**El 59% de la ventaja viene de dónde pescamos, no de a quién pescamos.**

Elegir el estanque — pequeñas y medianas estadounidenses, con margen y crecimiento regulares,
sin bancos ni inmobiliarias — aporta 5,63 pp. El filtro de momentum, que es donde hemos metido
casi todo el trabajo de esta investigación, aporta 3,84 pp.

Y hay una asimetría importante de fiabilidad entre los dos trozos:

- **Los +3,84 pp son la parte sólida.** Es una comparación *dentro* de la misma muestra: la
  cartera contra su propio universo. Los dos lados sufren exactamente el mismo sesgo de
  supervivencia, así que en gran medida se cancela.
- **Los +5,63 pp son la parte sospechosa.** Es una cesta amplia de pequeñas comparada contra el
  S&P, y es justo donde el sesgo de supervivencia muerde entero.

Dicho claro: **cuando arreglemos los delistings, lo que se va a mover es el trozo grande.**

---

## 3. Por qué el año 2 "funciona" y por qué no me lo creo

En bruto el año 2 parece aportar tanto como el año 1:

| Entrada | Acumulado 12m | Acumulado 24m | Sólo el año 2 |
|---|---|---|---|
| Febrero | 18,10% | 38,77% | 17,51% |
| Mayo | 14,28% | 35,06% | 18,18% |
| Agosto | 16,94% | 37,12% | 17,26% |
| Noviembre | 15,84% | 38,44% | 19,52% |

Y las peores cohortes **mejoran** al alargar (Noviembre: −38,2% a 12m → −7,8% a 24m).

Ahora el dato que lo desmonta:

> De las **467** empresas seleccionadas entre 2007 y 2023, el **100%** tiene ocho trimestres de
> datos posteriores. Ninguna desaparece. Ni una.

En un universo real de pequeña capitalización, entre un 3% y un 6% anual se va por opa, fusión o
quiebra. Aquí la tasa es **cero**, porque el panel sólo contiene tickers vivos hoy.

**Eso significa que el test del horizonte está estructuralmente sesgado a favor de aguantar más.**
Cuanto más largo el horizonte, más te beneficia el supuesto de que nada muere nunca, y más
tiempo tienen las caídas de recuperarse en una muestra de la que se han eliminado las que no
recuperaron. La conclusión "el año 2 también paga" es precisamente la más contaminada de todas
las que hemos sacado.

---

## 4. Veredicto

**Quedarse en 12 meses.** No porque los datos digan que alargar es peor — no lo dicen, el efecto
es indistinguible del ruido. Sino porque:

1. **A igualdad de resultado medido, gana la opción menos expuesta al sesgo que no hemos
   corregido.** 12 meses depende menos de que nada se muera que 24.
2. La ventaja bruta es la más alta a 12m (+2,53 pp de media).
3. Rebalancear cada año mantiene el filtro de momentum actualizado; a 24 meses estás operando
   con una señal de hasta dos años de antigüedad.

**Y una recalibración de prioridades.** Llevamos toda la investigación optimizando el filtro de
momentum, que aporta 3,84 de los 9,47 puntos. El resto lo aporta la definición del universo — y
esa parte no la hemos auditado nunca, más allá de la banda de capitalización. Antes de seguir
puliendo la selección conviene preguntarse qué pasa con el estanque:

- ¿Cuánto de esos 5,63 pp sobrevive al corregir los delistings? *(el trabajo pendiente)*
- ¿Cuánto aporta el filtro de estabilidad frente a coger las pequeñas sin más?
- ¿Cuánto aporta excluir Financials y Real Estate?

---

## 5. Resumen

| Pregunta | Respuesta |
|---|---|
| ¿12, 15, 18, 21 o 24 meses? | **Indistinguibles.** El efecto del mes de entrada es 3× mayor |
| ¿Aporta el año 2? | En los datos sí. Pero es la conclusión **más contaminada** por supervivencia |
| ¿Qué recomiendo? | **12 meses**, por prudencia frente al sesgo, no por los números |
| ¿De dónde viene la ventaja? | **59% del universo, 41% del momentum** |
| ¿Qué parte es fiable? | Los **+3,84 pp** del momentum. Los +5,63 del universo están por auditar |
| ¿Se pueden encadenar `fwd_1t`? | **No.** Defecto 9. Sólo múltiplos de 4 trimestres |
