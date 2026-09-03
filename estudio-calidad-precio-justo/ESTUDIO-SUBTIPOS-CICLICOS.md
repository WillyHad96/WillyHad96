# Partir las cíclicas en subtipos: lo primero de la serie que sobrevive a todos los controles

Motivo: "cíclicas" son cuatro animales distintos y promediarlos destruía la señal.
Scripts: `subtipos.py`, `hundidas.py`. Datos: `ciclicas_ampliado.csv`, `universo_sectorizado.csv`.

## Resumen en una frase

**Dentro de Industrials + Basic Materials, el cuartil más barato por P/S rinde 17,79% frente
al 11,03% de su propio pool y al 13,71% del Nasdaq — un alfa interno de +6,76 pp que replica
en ambas mitades, es monótono entre cuartiles, no cambia de signo al quitar ningún año y da
t = +2,38, el primer |t| > 2 de toda la serie.**

---

## 1. Las cíclicas no son un saco: son cuatro animales

| subtipo | n/año | CAGR | **corr Nasdaq** | p10 | p90 |
|---|---|---|---|---|---|
| Consumer Cyclical | 57 | **15,64%** | **0,925** | −35,4 | 79,5 |
| Industrials | 89 | 10,95% | 0,849 | −32,6 | 60,8 |
| Basic Materials | 42 | 10,00% | 0,764 | −39,3 | 65,6 |
| **Energy** | 32 | **5,71%** | **0,529** | −52,4 | 77,6 |
| todas juntas | 220 | 11,98% | 0,849 | −37,3 | 69,8 |

Correlación entre subtipos: Energía–Consumo Cíclico **0,617**. **No son la misma cosa**, y
promediarlas mezclaba un CAGR de 15,6% con uno de 5,7% y una correlación de 0,93 con una de
0,53.

## 2. La señal de "barato" se refuerza al separar

AUC del P/S contra el decil superior (0,5 = nada; por debajo = barato predice la cola):

| subtipo | pares | impares |
|---|---|---|
| **Industrials** | **0,412** | **0,424** |
| **Basic Materials** | **0,430** | **0,386** |
| Consumer Cyclical | 0,490 | 0,457 |
| Energy | 0,365 | 0,525 (no replica) |

En el saco entero daba 0,449 / 0,463. **Separando, Industriales y Materiales dan 0,41–0,43
replicado.** Son la familia del ciclo de capex, y es donde vive la señal.

## 3. El resultado, sobre 17 años

Industrials + Basic Materials, cuartiles por P/S dentro de cada año, equiponderado:

| variante | n/año | CAGR | corr | azar | descorr. real | CAGR azar | **vs azar** | peor año |
|---|---|---|---|---|---|---|---|---|
| familia entera | 131 | 11,03% | 0,843 | 0,842 | +0,001 | 11,02% | +0,01 | −37,4 |
| **BARATAS P/S 25%** | **33** | **17,79%** | 0,785 | 0,816 | −0,031 | 10,86% | **+6,93** | −43,6 |
| BARATAS P/S 10% | 14 | 18,12% | 0,770 | 0,770 | 0,000 | 10,45% | +7,67 | −44,2 |
| **CARAS P/S 25%** | 33 | **5,54%** | 0,876 | 0,816 | +0,060 | 10,84% | −5,30 | −31,9 |
| barata + margen bajo | 28 | 17,44% | 0,775 | 0,811 | −0,036 | 10,85% | +6,60 | −41,5 |

Nasdaq: **13,71%**.

**Monótono**: caras 5,54%, familia 11,03%, baratas 17,79%. Añadir "margen bajo" no aporta
(17,44 vs 17,79): **la señal es la valoración, no el hundimiento operativo**.

## 4. Los cinco controles que pasa

Todo lo demás en esta serie murió bajo uno de estos. Éste pasa los cinco.

1. **Descubrimiento/confirmación (B1).** Pares 17,93% vs azar 10,72%; impares 17,66% vs azar
   11,12%. **+7,2 y +6,5 pp, casi idénticos.**
2. **Contrafactual aleatorio a igual tamaño (B2).** El azar con 33 nombres del mismo pool da
   10,86%. La ventaja es **+6,93 pp sobre el azar**, no sobre un índice.
3. **Alfa interno, inmune a supervivencia (B4).** Baratas vs su propio pool: **+6,76 pp de
   CAGR**, diferencia pareada anual **+10,15 pp con t = +2,38**. Bate a la familia **12 de 17
   años**. Primer |t| > 2 de la serie.
4. **Leave-one-year-out (B6/B8).** Rango del alfa: **[+4,84, +8,27] pp**. **El signo no cambia
   al quitar ningún año** y nunca se acerca a cero. Compárese con el eje temporal, donde
   quitar 2008 daba la vuelta al signo.
5. **Trampa de valor, medida sobre el universo CON muertos.** Ver §5.

## 5. La trampa de valor existe, y aun así el efecto gana

Objeción obligada: las baratas son las que más mueren, y el pool sectorizado no tiene muertos
(A7). Test directo sobre el universo **completo**, 2021–2023, donde las bajas sí están:

| cuartil P/S | n | balas | **% balas** | ret medio | p10 |
|---|---|---|---|---|---|
| **Q1 más baratas** | 2.182 | 52 | **2,38%** | **+10,0%** | −56,1 |
| Q2 | 2.181 | 16 | 0,73% | +1,4% | −49,9 |
| Q3 | 2.180 | 22 | 1,01% | −2,5% | −46,8 |
| **Q4 más caras** | 2.179 | 24 | 1,10% | **−11,6%** | −66,0 |

- **La trampa es real: las baratas mueren 2,4 veces más** que el resto.
- **Pero cuesta ~0,7 pp anuales** (1,28 pp extra de eventos × −54% de coste medio).
- **Y el diferencial barato−caro es de 21,6 pp medido sobre un universo que YA incluye los
  muertos registrados.** El efecto sobrevive con margen.
- **Sorpresa: las baratas tienen mejor cola izquierda** (p10 −56,1 vs −66,0). Las caras se
  estrellan más fuerte.

## 6. Lo que NO resuelve

**No descorrelaciona.** Correlación 0,785, descorrelación real **−0,031**: dentro del ruido.
Esto resuelve la mitad de rentabilidad de la pregunta, no la de diversificación.

Y hereda los límites conocidos: 17 años, error del CAGR ±11,5 pp (B6), riesgo de ventana
(B8), y el panel sigue subregistrando muertes fuera de 2021–2023.

**Y en 2008 hizo −43,6% frente al −30,1% del Nasdaq.** Es una estrategia de valor: sufre más
en el pánico.

Un apunte de honestidad: **esto es la prima de valor, que lleva documentada desde
Fama-French.** No es un descubrimiento nuestro. Eso es bueno para su robustez —no es un
artefacto de estos 17 años— y malo para las expectativas: la prima ha sido más floja en las
últimas dos décadas que en el backtest.

## 7. Año a año

| | 2008 | 2009 | 2016 | 2020 | **2021** | **2022** | 2023 |
|---|---|---|---|---|---|---|---|
| baratas | −44 | +127 | +93 | +64 | **+33** | **+19** | +34 |
| Nasdaq | −31 | +56 | +31 | +48 | +8 | **−18** | +36 |

**2022: +19% con el Nasdaq en −18%.** Ahí sí hay desacoplamiento, y es el año de value.

## 8. Qué haría ahora

1. **Recuperar el sector de las 1.619 bajas** (A7) vía FMP y rehacer este mismo cálculo con
   mortalidad real. Es el único control que le falta y ahora es barato y decisivo.
2. **Probar `evToSales` y `priceToBook` de FMP** en lugar del P/S del panel — son la medida
   correcta para cíclicas (EV incluye la deuda; P/B no explota en el suelo).
3. **No** buscarle descorrelación a esto. No la tiene. Si se quiere descorrelación, Energía
   con corr 0,529 es otra conversación, con su propio problema (CAGR 5,71%).
