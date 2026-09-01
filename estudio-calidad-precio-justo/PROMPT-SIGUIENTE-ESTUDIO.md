# Prompt para abrir la siguiente conversación

Copiar y pegar tal cual. Está escrito para que la nueva sesión arranque con el contexto y
las reglas ya puestas, sin repetir los errores que hemos pagado en esta.

---

```
Soy inversor cuantitativo particular. Trabajo sobre la tabla `hypergrowth_panel` del
proyecto Supabase `mlcpuqlawehpznidumvi`. El repo es WillyHad96/WillyHad96, rama
`claude/hypergrowth-analysis-pricing-0z51v1`, y todo el trabajo previo está en
`estudio-calidad-precio-justo/`. Habla en español.

LEE PRIMERO `estudio-calidad-precio-justo/HALLAZGOS.md`. Resume lo establecido en la serie
anterior. No repitas nada de lo que ya está descartado ahí.

## Qué quiero

Construir un compartimento de cartera que cumpla LAS DOS cosas a la vez:
  - correlación BAJA con el Nasdaq (no beta baja: correlación)
  - rentabilidad capaz de COMPETIR con el Nasdaq, no de igualarlo por debajo

La volatilidad no me penaliza. El horizonte es de años y ya tengo Nasdaq en cartera, así
que no busco batirlo: busco que meter todo al Nasdaq no sea mi única opción sensata.
Presupuesto por compartimento: ~10.000 €, o sea 15–20 posiciones como máximo.

## Lo que YA está descartado, no lo rehagas

- Ninguna variante cíclica descorrelaciona. Las siete probadas (C4 cíclicos, sin filtro de
  estabilidad, sin momento, momento invertido, +value, sin estabilidad+value,
  Energía+Materiales) están en ±0,03 de lo que daría el azar.
- "Cíclicos + value" parece ganar (+1,26 pp en mezcla) pero es beta: el Nasdaq escalado
  ×1,07 replica casi todo.
- Deuda neta / ventas, ROIC y FCF yield: refutados en confirmación fuera de muestra.
- "Defensivos + momento" es el único con descorrelación real (−0,14) y tamaño operable,
  pero rinde 2,3 pp menos que el Nasdaq y su alfa murió en el control pares/impares.

## Por dónde creo que hay que ir (discútelo, no lo des por bueno)

Todo lo probado son reglas de SECCIÓN CRUZADA: qué comprar. La hipótesis que queda sin
explorar es el EJE TEMPORAL: cuánta exposición tener según el régimen. Una regla de serie
temporal sí puede descorrelacionar de verdad manteniendo rentabilidad de renta variable —
es el mecanismo del seguimiento de tendencia. Ideas concretas a evaluar:

  1. Modular la exposición del compartimento según el momento del propio índice o del
     universo (fuera cuando el régimen es malo, dentro cuando es bueno).
  2. Ver si la correlación de las variantes con el Nasdaq cambia por régimen, y si se puede
     explotar esa asimetría.
  3. Cualquier otra cosa que se te ocurra que rompa la simetría temporal.

Si concluyes que con estos datos no se puede, dímelo pronto y dime qué datos harían falta.

## Reglas de método — son obligatorias

1. PRE-REGISTRO. Antes de mirar la confirmación, escribe la regla cerrada en un fichero y
   haz commit. Descubrimiento = años pares, confirmación = años impares. En la serie
   anterior murieron SEIS efectos bajo este control; los que estaban pre-registrados no
   costaron nada.
2. CONTRAFACTUAL ALEATORIO. La correlación baja sola al reducir nombres: 3 nombres al azar
   dan 0,65 de correlación con el Nasdaq, 40 dan 0,88. Nunca reportes una correlación sin
   compararla con carteras ALEATORIAS del mismo tamaño y del mismo pool.
3. BETA ≠ CORRELACIÓN. Beta = correlación × volatilidad relativa. No me des beta baja que
   sea sólo volatilidad baja.
4. LOS DOS ALFAS. El alfa contra el índice hereda el sesgo de supervivencia entero. El alfa
   de "pasar el filtro vs no pasarlo" es inmune porque falta lo mismo en los dos brazos.
   Reporta siempre los dos y construye la tesis sobre el segundo.
5. GUARDAS DE CALIDAD. Las de `consultas.sql` (defectos 2, 7 y 8) no se quitan ninguna.
   La reconstrucción de la estrategia está en `c4_base.sql`; reutilízala.
6. Di lo que no sabes. Prefiero un "esto no distingue del ruido" a una cifra bonita.

## Límites de los datos que tienes que respetar

- El panel NO registra muertes antes de 2015 (0-5 al año frente a 200-400 reales). Como
  universo es ficción antes de 2015 y solo aceptable desde 2021.
- La supervivencia se queda plana en 82-85% de 2002 a 2020: imposible.
- `sector` no es nulo, es el centinela 'desconocido' (73% de los tickers), y ese centinela
  PREDICE el retorno dentro del mismo año y sector (p = 0,008). Es sesgo, no señal.
- Hay 13 eventos que son la misma empresa bajo dos o tres tickers. Deduplica.
- 17 observaciones anuales: error típico de una correlación ~0,15 y de un CAGR ~6 pp.
- Aviso ya conocido y NO resuelto: RLS desactivado en `hypergrowth_panel` y otras 8 tablas.
  No lo arregles por tu cuenta.

## Formato de trabajo

Documenta cada estudio en un .md en `estudio-calidad-precio-justo/`, con el script que lo
reproduce, y haz commit y push a la rama. Ficheros de datos y scripts en ese directorio,
no en la raíz.
```

---

## Variante si prefieres atacar los datos en vez de la estrategia

Sustituye la sección "Qué quiero" por:

```
## Qué quiero

Migrar el estudio a un universo point-in-time de verdad. El panel actual tiene sesgo de
supervivencia grave (ver HALLAZGOS.md, sección A). Quiero:
  1. Evaluar Sharadar (vía Nasdaq Data Link) y Norgate contra el test de aceptación:
     - cohorte de 2008 que sigue viva en 2025: debe salir 45-55%, no 83%
     - número de cotizadas por año: debe BAJAR (8.025 en 1996 → 4.102 en 2012)
     - retornos de deslistado: coger 20 quiebras conocidas y ver qué devuelve
  2. Reconstruir C4 sobre esos datos y ver cuánto del 15,19% sobrevive.
```
