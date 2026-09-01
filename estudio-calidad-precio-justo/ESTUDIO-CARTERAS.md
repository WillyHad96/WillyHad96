# C4 como compartimento de cartera: qué diversifica y con cuántas posiciones

Medición previa a montar carteras reales. Dos preguntas prácticas: **¿C4 descorrelaciona
del Nasdaq?** y **¿aguanta con las pocas posiciones que permiten 10.000 €?**

**Respuestas: no descorrelaciona (correlación 0,92), y sí aguanta concentrada.**

Ventanas feb–feb del propio panel, 2007–2023, cartera con ponderación rank². Los índices
son los del panel (`fwd_4t − fwd_4t_rel_*`), no series de mercado externas.

## 1. C4 no es un diversificador del Nasdaq

| | correlación | beta |
|---|---|---|
| C4 vs Nasdaq | **+0,918** | 1,00 |
| C4 vs S&P 500 | +0,895 | 1,19 |
| Nasdaq vs S&P 500 | +0,936 | — |

**R² de C4 explicado por el Nasdaq: 84%.** Solo el 16% del movimiento es independiente.

| | CAGR | desv. | peor año |
|---|---|---|---|
| C4 | 14,16% | 24,1 | **−42,5%** |
| Nasdaq | 13,89% | 22,1 | −28,8% |
| S&P 500 | 7,78% | 18,1 | −40,2% |

C4 es, operativamente, **un Nasdaq con más volatilidad y peor caída máxima, por 27 puntos
básicos de más rentabilidad**. Contra el S&P sí hay distancia clara (+6,4 pp/año en esta
ventana, que favorece al crecimiento).

Mezclas 50/50 rebalanceadas cada año:

| mezcla | CAGR | desv. | peor año |
|---|---|---|---|
| C4 + Nasdaq | 14,15% | 22,6 | −35,6% |
| C4 + S&P | 11,08% | 20,6 | −41,3% |
| Nasdaq + S&P | 10,91% | 19,8 | −34,5% |

Añadir C4 a una posición de Nasdaq **no reduce el riesgo** (22,6 vs 22,1 de desviación) ni
mejora la rentabilidad. Es aditivo en exposición, no en diversificación.

**Consecuencia para el diseño de cartera:** C4 no es "un compartimento descorrelacionado",
es **small/mid cap USA de calidad**. Sirve como complemento al Nasdaq y como alternativa
al S&P. No sirve como contrapeso.

## 2. Concentración: 15–20 nombres funcionan

Top N por momento a 12 meses, equiponderado, dentro del universo que pasa los cuatro
filtros de C4:

| posiciones | CAGR | vs Nasdaq |
|---|---|---|
| 10 | 15,19% | +0,15 pp |
| 15 | 15,57% | +0,53 pp |
| 20 | 16,77% | +1,73 pp |
| 30 | 13,58% | −1,46 pp |
| 50 | 12,22% | −2,82 pp |

**No hay que leer el 20 como óptimo.** Con desviación anual del 24% y 17 observaciones, el
error típico de la media ronda los 6 pp/año: ninguna de estas diferencias es distinguible
del ruido. Lo que sí se puede afirmar es lo operativo: **concentrar en 15–20 nombres no
rompe la estrategia**, lo que hace viable un compartimento de 10.000 € (~500 €/posición).

El coste es la cola:

| | desviación anual | peor año |
|---|---|---|
| 10 nombres | 34,3 | −49,6% |
| 20 nombres | 24,5 | −37,5% |

## 3. Advertencia sobre el siguiente estudio: turnarounds

`AUDITORIA-COBERTURA-TEMPORAL.md` establece que el panel **no registra prácticamente
ninguna baja antes de 2015** (0–5 al año frente a las 200–400 reales).

Un filtro de turnarounds selecciona, por definición, empresas cerca de la angustia
financiera. **Las que no se recuperaron no están en los datos.** Cualquier backtest de
turnarounds sobre este panel dará un resultado excelente y será ficción, y el sesgo será
mucho mayor que en C4 porque actúa exactamente sobre la población seleccionada.

**Turnarounds es la idea que estos datos menos pueden soportar.** Aparcada hasta disponer
de un universo punto-en-el-tiempo.

Arbitraje de fusiones / situaciones especiales sí tiene beta baja real, pero exige 15–20
operaciones simultáneas para ser estadística en vez de lotería.

## 4. Limitaciones

- Todo hereda el sesgo de supervivencia documentado: universo con 83–85% de supervivientes
  donde debería haber ~50%. Las correlaciones son menos sensibles a ese sesgo que los
  niveles de rentabilidad, pero no inmunes.
- Los índices son los incorporados al panel, no series externas verificadas. El S&P sale
  a 7,78% en ventana feb–feb 2007–2023, por debajo del retorno total real del periodo.
  Sirve para comparar, no como cifra de referencia.
- 17 observaciones anuales. Todo lo de aquí es indicativo.

## Ficheros

- `correlacion.py` — correlaciones, betas, mezclas y tabla de concentración.

## 5. Corrección posterior: C4 no es "las cíclicas"

La medición de arriba es sobre **C4 completo**. La etiqueta "cíclicas" usada en la
conversación corresponde a un **subconjunto** de C4 (194 eventos en cuatro sectores) que se
recortó para los estudios de deuda y ROIC/FCF. Partiendo C4 por sector, las dos mitades
correlacionan solo +0,68 entre sí, y la mitad cíclica se desacopla del Nasdaq en 2021–2022.
Detalle y tablas en `NOTA-C4-NO-ES-CICLICAS.md`.
