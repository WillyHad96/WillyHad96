# Test del protocolo /cyclical_clock v1.1 como señal predictiva

Traduce las métricas C1–C6 del protocolo a variables medibles en cada decisión de febrero y
mide su AUC contra el decil superior de retorno, partido en pares/impares.
Script: `cyclical_clock.py`. Datos: 60 Industrials, `income-statement` trimestral (80T), **634
decisiones**, 2007–2023. Desfase anti-look-ahead: último trimestre cerrado antes del 15 de
noviembre del año anterior.

## 1. Qué se testea y qué no

**El protocolo no afirma predecir retornos.** Su §0 prohíbe explícitamente los verbos
prescriptivos y se define como diagnóstico forense: sitúa la empresa en su reloj del ciclo.
Este test mide otra cosa: **si ese diagnóstico predice el retorno del año siguiente**, que es
lo que necesita una cartera sistemática.

Son afirmaciones distintas, y lo que sigue **no refuta el protocolo como marco de análisis**.
Refuta su utilidad como fuente de alfa en este universo.

**Cinco de sus métricas ya estaban medidas** en `ESTUDIO-PILOTO-CICLICAS.md` y ninguna
replicó: C3 posición del margen (0,483/0,527), C7 inventario (0,488/0,476), C9 capex÷D&A
(0,496/0,485), C11 EV/EBITDA normalizado (0,493/0,388), C13 deuda neta/EBITDA (0,684/**0,517**).
Este estudio añade lo genuinamente nuevo: **C5, la segunda derivada**, que es su tesis central.

## 2. El resultado

| métrica del protocolo | AUC pares | AUC impares | ¿replica? |
|---|---|---|---|
| C2 margen EBITDA (nivel) | 0,503 | 0,506 | nada |
| C3 margen ÷ media del ciclo | 0,510 | 0,484 | no |
| C3 posición en el rango | 0,498 | 0,470 | nada |
| C3 supera el pico previo | 0,478 | 0,469 | nada |
| C4 EBITDA en riesgo | 0,479 | 0,486 | nada |
| **C5 incremental SECUENCIAL** | **0,645** | **0,490** | **NO** |
| C5 incremental seq − margen op | 0,645 | 0,492 | NO |
| C5 incremental INTERANUAL | 0,529 | 0,523 | signo ok, tamaño no |
| C6 crecimiento de ventas TTM | 0,478 | 0,525 | no |
| **(control) P/S del panel** | **0,452** | **0,446** | **sí** |

## 3. La lección: C5 secuencial es una trampa de manual

**0,645 en años pares.** Por encima del umbral de 0,60 que teníamos declarado. Si este test
se hubiera hecho sin partir la muestra —que es exactamente como se usaría el protocolo en la
práctica— el titular sería *"la tesis central de /cyclical_clock funciona, AUC 0,645"*.

**Y en años impares da 0,490.** Nada.

Es el séptimo caso de la serie con este patrón. El protocolo, por diseño, **no tiene ningún
mecanismo que proteja contra esto**: es un marco de diagnóstico por empresa, sin muestra de
confirmación. Su propio §11 (anti-alucinación) cubre inventarse datos, no auto-engañarse con
una mitad de la muestra.

## 4. Una crítica constructiva a C5

La fórmula del protocolo compara el trimestre actual con **el de hace tres** (secuencial). En
industriales estacionales eso mezcla estacionalidad con ciclo: comparar Q4 con Q1 mide sobre
todo el calendario.

La versión **interanual** (T0 frente a T−4) controla la estación, y es la única del protocolo
que **mantiene el signo en las dos mitades** (0,529 / 0,523) y en la dirección que él predice:
margen incremental alto → más probable en la cola alta. Pero |AUC−0,5| es de 0,02, dentro del
ruido.

**Recomendación concreta para el protocolo: C5 debería definirse interanual, no secuencial.**
Es más defendible conceptualmente y es la única versión que no se desmonta al cambiar de
mitad de la muestra.

## 5. Veredicto

**Ninguna métrica del protocolo supera al control.** El P/S simple del panel da 0,452/0,446 —
replicado y más fuerte que cualquier C1–C6.

Para lo que estamos construyendo —un criterio sistemático de selección dentro de
Industriales— **el protocolo no añade nada medible sobre lo que ya teníamos**.

Lo que sí aporta, y conviene no tirar:

- **Sus avisos de integridad (§4) son correctos y necesarios.** Verificado en GBX: el
  `operatingCashFlow` del Q3 2026 sale **−226,8 M$** por un `otherNonCashItems` de −219,3 M$,
  y el `propertyPlantEquipmentNet` salta de 719 M$ a 2.007 M$ entre trimestres consecutivos.
  Basura reclasificada, exactamente lo que §4 anticipa.
- **Como marco narrativo por empresa** —para entender *por qué* una cíclica está donde está
  antes de tomar una decisión discrecional— no está evaluado aquí y puede ser valioso.

Lo que no hace es dar una señal transversal que ordene retornos.
