-- Bloque base reutilizable del estudio "Calidad a precio justo" (2026-08-17)
-- Proyecto Supabase: mlcpuqlawehpznidumvi · tabla hypergrowth_panel
--
-- Puntos criticos, no quitar ninguno:
--   * margen_bruto acotado a [0.05,0.95]      -> defecto 7 (P/GP explota sin esto)
--   * verificacion (fecha_fin-fecha_ini)/365.25 -> defecto 8 (reporte semestral)
--   * descarte de precios forward-filled en AMBOS extremos -> defecto 2
--   * SPY encadenado geometricamente: spy = fwd_4t - fwd_4t_rel_spy
--   * round() exige ::numeric en Postgres; cualificar fecha en los joins

with clean as (
  select ticker, fecha, precio_post, sector, ingresos_ttm, multiplo_ps,
         margen_operativo, delta_margen_op, dilucion_yoy,
    case when margen_bruto between 0.05 and 0.95 then margen_bruto end as mb,
    case when crecimiento between -0.99 and 3.0 then crecimiento end as cr,
    case when fwd_4t is not null and fwd_4t_rel_spy is not null
              and fwd_4t between -0.99 and 10
         then fwd_4t - fwd_4t_rel_spy end as spy0
  from hypergrowth_panel
  where fecha >= '1995-01-01' and precio_post is not null and precio_post > 0
    and ticker ~ '^[A-Z]{1,5}$'
    and not (length(ticker) >= 5 and right(ticker,1) in ('F','Y'))
    and not (length(ticker) >= 4 and right(ticker,1) in ('W','U','R','Z'))
),
px as (
  select *,
    (precio_post is not distinct from lag(precio_post) over w) as ff_ini,
    lead(precio_post,4)  over w p4,  lead(fecha,4)  over w f4,  lead(precio_post,3)  over w p4p,
    lead(precio_post,8)  over w p8,  lead(fecha,8)  over w f8,  lead(precio_post,7)  over w p8p,
    lead(precio_post,12) over w p12, lead(fecha,12) over w f12, lead(precio_post,11) over w p12p,
    lead(precio_post,20) over w p20, lead(fecha,20) over w f20, lead(precio_post,19) over w p20p,
    lead(spy0,4) over w s1, lead(spy0,8) over w s2, lead(spy0,12) over w s3, lead(spy0,16) over w s4,
    stddev_samp(mb) over w8 sd_mb, stddev_samp(cr) over w8 sd_cr,
    min(margen_operativo) over w4 min_mop, count(mb) over w8 n8,
    row_number() over (partition by ticker, date_trunc('year',fecha) order by fecha) rn_yr
  from clean
  window w  as (partition by ticker order by fecha),
         w8 as (partition by ticker order by fecha rows between 7 preceding and current row),
         w4 as (partition by ticker order by fecha rows between 3 preceding and current row)
),
u as (
  select extract(year from fecha)::int yr, ticker, fecha, sector, mb, multiplo_ps,
         multiplo_ps/mb p_gp, sd_mb, sd_cr,
    (min_mop > 0)::int q1, (delta_margen_op > 0)::int q2, (dilucion_yoy < 0.02)::int q3,
    case when (f4-fecha)/365.25 between 0.75 and 1.25 and p4 is distinct from p4p
              and not ff_ini and spy0 is not null
         then (p4/precio_post)/(1+spy0)-1 end rel4,
    case when (f8-fecha)/365.25 between 1.75 and 2.25 and p8 is distinct from p8p
              and not ff_ini and spy0 is not null and s1 is not null
         then (p8/precio_post)/((1+spy0)*(1+s1))-1 end rel8,
    case when (f12-fecha)/365.25 between 2.75 and 3.25 and p12 is distinct from p12p
              and not ff_ini and spy0 is not null and s1 is not null and s2 is not null
         then (p12/precio_post)/((1+spy0)*(1+s1)*(1+s2))-1 end rel12,
    case when (f20-fecha)/365.25 between 4.75 and 5.25 and p20 is distinct from p20p
              and not ff_ini and spy0 is not null and s1 is not null and s2 is not null
              and s3 is not null and s4 is not null
         then (p20/precio_post)/((1+spy0)*(1+s1)*(1+s2)*(1+s3)*(1+s4))-1 end rel20
  from px
  where mb is not null and cr is not null and ingresos_ttm >= 1e7 and precio_post >= 1
    and sector is not null and sector <> 'desconocido' and multiplo_ps > 0
    and multiplo_ps*ingresos_ttm between 3e8 and 5e9        -- market cap 300M-5000M
    and n8 >= 6
    and delta_margen_op is not null and dilucion_yoy is not null
    and sd_mb is not null and sd_cr is not null
),
-- percentile_cont NO admite OVER en Postgres: usar percent_rank()
q as (
  select *,
    (percent_rank() over (partition by yr order by sd_mb) < 0.5)::int q4,
    (percent_rank() over (partition by yr order by sd_cr) < 0.5)::int q5
  from u
),
g as (
  select *, case when q1+q2+q3+q4+q5 = 5 then 'CALIDAD'
                 when q1+q2+q3+q4+q5 <= 2 then 'MEDIOCRE' end grupo
  from q
),
tg as (select *, ntile(3) over (partition by grupo, yr order by p_gp) t from g where grupo is not null)

-- Contraste principal (H3): calidad vs mediocre por tercil de P/GP
select grupo, t, count(*) n, count(distinct ticker) tk,
  (100*percentile_cont(0.5) within group (order by rel4))::numeric(6,1)  m4,
  (100*percentile_cont(0.5) within group (order by rel8))::numeric(6,1)  m8,
  (100*percentile_cont(0.5) within group (order by rel12))::numeric(6,1) m12,
  (100*percentile_cont(0.5) within group (order by rel20))::numeric(6,1) m20
from tg group by 1,2 order by 1,2;
