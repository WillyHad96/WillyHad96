-- Reconstruccion de la estrategia C4 (spec en ESTUDIO-ALFA-POST-DELISTINGS.md §7).
-- Universo: US, mcap 300M-5000M, ingresos_ttm>=1e7, precio_post>=1, SIN filtro de sector.
-- Filtros: sd(margen_bruto) 8T < mediana del anho, sd(crecimiento) 8T < mediana,
--          regla40 > p25 del anho, mcap > p25 del anho.
-- Seleccion: top 20% por momento 12m. Pesos: rank^2. Venta a 12 meses.
-- Guardas de calidad de datos: ver consultas.sql (defectos 2, 7, 8). No quitar ninguna.
with clean as (
  select ticker, fecha, precio_post, sector, ingresos_ttm, multiplo_ps, regla40,
    case when margen_bruto between 0.05 and 0.95 then margen_bruto end mb,
    case when crecimiento between -0.99 and 3.0 then crecimiento end cr,
    case when fwd_4t is not null and fwd_4t between -0.99 and 10 then fwd_4t end f4r,
    case when fwd_4t is not null and fwd_4t between -0.99 and 10
           then fwd_4t - fwd_4t_rel_qqq end qqq0,
    case when fwd_4t is not null and fwd_4t between -0.99 and 10
           then fwd_4t - fwd_4t_rel_spy end spy0
  from hypergrowth_panel
  where fecha >= '1995-01-01' and precio_post > 0
    and ticker ~ '^[A-Z]{1,5}$'
    and not (length(ticker) >= 5 and right(ticker,1) in ('F','Y'))
    and not (length(ticker) >= 4 and right(ticker,1) in ('W','U','R','Z'))
),
px as (
  select *,
    (precio_post is not distinct from lag(precio_post) over w) ff_ini,
    lag(precio_post,4)  over w p_1y,
    lead(precio_post,4) over w p4,
    lead(fecha,4)       over w f4,
    lead(precio_post,3) over w p4p,
    stddev_samp(mb) over w8 sd_mb,
    stddev_samp(cr) over w8 sd_cr,
    count(mb)       over w8 n8,
    row_number() over (partition by ticker, date_trunc('year',fecha) order by fecha) rn_yr
  from clean
  window w  as (partition by ticker order by fecha),
         w8 as (partition by ticker order by fecha rows between 7 preceding and current row)
),
u as (
  select ticker, fecha, extract(year from fecha)::int yr, sector, regla40,
    sd_mb, sd_cr,
    multiplo_ps*ingresos_ttm mcap,
    precio_post/nullif(p_1y,0)-1 mom12,
    case when (f4-fecha)/365.25 between 0.75 and 1.25
              and p4 is distinct from p4p and not ff_ini then f4r  end ret,
    case when (f4-fecha)/365.25 between 0.75 and 1.25
              and p4 is distinct from p4p and not ff_ini then qqq0 end qqq,
    case when (f4-fecha)/365.25 between 0.75 and 1.25
              and p4 is distinct from p4p and not ff_ini then spy0 end spy
  from px
  where mb is not null and cr is not null
    and ingresos_ttm >= 1e7 and precio_post >= 1
    and multiplo_ps*ingresos_ttm between 3e8 and 5e9
    and n8 >= 6 and rn_yr = 1
    and regla40 is not null and p_1y is not null
),
r as (
  select *,
    percent_rank() over (partition by yr order by sd_mb)   pr_mb,
    percent_rank() over (partition by yr order by sd_cr)   pr_cr,
    percent_rank() over (partition by yr order by regla40) pr_r40,
    percent_rank() over (partition by yr order by mcap)    pr_mc
  from u
),
c4 as (select * from r where pr_mb < 0.5 and pr_cr < 0.5 and pr_r40 > 0.25 and pr_mc > 0.25),
top as (
  select *, row_number() over (partition by yr order by mom12 desc) rn,
            count(*)     over (partition by yr) n
  from (select *, percent_rank() over (partition by yr order by mom12 desc) prm from c4) z
  where prm < 0.20
),
cartera as (
  select *, power(n-rn+1, 2)::numeric pw
  from top
  where ret is not null and yr between 2007 and 2023
)
