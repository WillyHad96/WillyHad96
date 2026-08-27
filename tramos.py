import statistics as st
raw="""1,2007,-1.22,-7.12,-1.09;1,2008,-36.11,-41.67,-32.18;1,2009,43.71,34.62,46.36;1,2010,43.66,20.70,29.37;1,2011,19.80,2.73,9.81;1,2012,21.86,13.49,8.60;1,2013,54.72,27.22,37.79;1,2014,9.57,12.29,16.71;1,2015,-14.95,-7.02,-3.17;1,2016,35.60,22.99,26.75;1,2017,31.06,18.76,29.05;1,2018,22.41,1.83,4.31;1,2019,19.98,17.44,27.83;1,2020,53.05,24.36,48.03;1,2021,-4.46,10.92,7.20;1,2022,17.52,-11.19,-22.45;1,2023,46.38,26.73,43.88;1,2024,30.45,20.06,20.12;1,2025,36.24,19.39,22.99;2,2007,-0.23,-9.25,1.74;2,2008,-35.68,-36.37,-25.46;2,2009,35.75,32.96,40.24;2,2010,29.06,14.42,19.34;2,2011,8.35,2.64,11.82;2,2012,32.47,17.49,8.83;2,2013,37.97,21.00,27.22;2,2014,6.53,11.15,20.75;2,2015,-1.21,-0.74,-0.79;2,2016,31.97,16.99,28.00;2,2017,25.49,12.67,20.11;2,2018,8.81,8.89,13.23;2,2019,1.78,-1.13,13.84;2,2020,69.32,51.29,56.98;2,2021,-16.29,0.59,-3.72;2,2022,15.19,-2.85,-0.80;2,2023,43.78,28.13,36.77;2,2024,27.75,10.91,12.71;2,2025,50.43,32.19,41.60;3,2007,-13.44,-14.80,-6.68;3,2008,-26.19,-21.90,-11.70;3,2009,23.69,12.47,17.18;3,2010,47.43,19.94,28.95;3,2011,18.09,9.61,15.14;3,2012,38.47,23.67,18.55;3,2013,26.27,17.88,26.90;3,2014,14.41,4.23,12.30;3,2015,11.15,3.98,3.64;3,2016,31.53,16.46,26.15;3,2017,16.80,14.73,23.00;3,2018,0.98,4.45,5.74;3,2019,20.00,11.81,33.19;3,2020,46.73,36.48,39.23;3,2021,-11.17,-7.87,-16.44;3,2022,41.67,13.37,22.91;3,2023,37.82,23.34,25.84;3,2024,25.89,18.56,24.33;3,2025,31.22,22.37,26.15;4,2007,-38.76,-36.83,-40.54;4,2008,10.99,11.12,25.93;4,2009,33.64,12.75,24.38;4,2010,20.29,4.04,9.60;4,2011,31.33,15.57,15.65;4,2012,46.28,27.66,28.82;4,2013,11.34,12.82,19.28;4,2014,7.68,3.90,11.55;4,2015,6.54,3.75,5.03;4,2016,30.08,22.10,29.20;4,2017,14.28,5.96,11.42;4,2018,21.84,12.65,16.89;4,2019,13.80,11.69,33.88;4,2020,42.55,36.12,38.63;4,2021,-16.39,-16.96,-34.46;4,2022,19.07,13.46,30.01;4,2023,44.88,37.79,38.93;4,2024,9.42,15.11,21.38"""
D={}
for r in raw.split(';'):
    rn,yr,a,s,q=r.split(',')
    D.setdefault(int(rn),{})[int(yr)]=(float(a)/100,float(s)/100,float(q)/100)
def cagr(x):
    p=1.0
    for v in x: p*=(1+v)
    return p**(1/len(x))-1
MES={1:'Febrero',2:'Mayo',3:'Agosto',4:'Noviembre'}
Y=list(range(2007,2025))

print("=== CARTERA vs S&P 500 vs NASDAQ-100 · 2007-2024 (18 años, solo precio) ===")
print(f"{'Entrada':<12}{'CAGR':>9}{'SPY':>9}{'QQQ':>9}{'vs SPY':>9}{'vs QQQ':>9}{'Gana QQQ':>10}{'Peor':>8}{'Vol':>7}")
S={}
for rn in [1,2,3,4]:
    a=[D[rn][y][0] for y in Y]; s=[D[rn][y][1] for y in Y]; q=[D[rn][y][2] for y in Y]
    ca,cs,cq=cagr(a),cagr(s),cagr(q); S[rn]=ca
    w=sum(1 for x,z in zip(a,q) if x>z)
    print(f"{MES[rn]:<12}{ca*100:>8.2f}%{cs*100:>8.2f}%{cq*100:>8.2f}%{(ca-cs)*100:>8.2f}{(ca-cq)*100:>9.2f}{w:>8}/18{min(a)*100:>7.1f}%{st.stdev(a)*100:>6.1f}%")
a4=[st.mean([D[rn][y][0] for rn in [1,2,3,4]]) for y in Y]
s4=[st.mean([D[rn][y][1] for rn in [1,2,3,4]]) for y in Y]
q4=[st.mean([D[rn][y][2] for rn in [1,2,3,4]]) for y in Y]
c4,cs4,cq4=cagr(a4),cagr(s4),cagr(q4)
w4=sum(1 for x,z in zip(a4,q4) if x>z)
print(f"{'4 TRAMOS':<12}{c4*100:>8.2f}%{cs4*100:>8.2f}%{cq4*100:>8.2f}%{(c4-cs4)*100:>8.2f}{(c4-cq4)*100:>9.2f}{w4:>8}/18{min(a4)*100:>7.1f}%{st.stdev(a4)*100:>6.1f}%")

print("\n=== ¿'RINDE MENOS'? LA MEZCLA CONTRA SUS PROPIAS PARTES ===")
media_partes=st.mean([S[rn] for rn in [1,2,3,4]])
print(f"  Media aritmetica de los 4 CAGR individuales : {media_partes*100:.2f}%")
print(f"  CAGR real de la mezcla                      : {c4*100:.2f}%")
print(f"  -> la mezcla GANA {(c4-media_partes)*100:+.2f} pp sobre la media de sus partes (menos varianza)")
print(f"  Solo pierde contra febrero ({S[1]*100:.2f}%), que es el mejor de los cuatro por casualidad.")

print("\n=== EL PEOR AÑO: DE DONDE SALE EL -21.7% ===")
peor=min(range(len(Y)), key=lambda i:a4[i]); yp=Y[peor]
print(f"  Peor año de la mezcla: {yp}  ({a4[peor]*100:.2f}%)")
for yy in [2007,2008]:
    print(f"\n  Entradas de {yy} (cada una mantenida 12 meses):")
    for rn in [1,2,3,4]:
        print(f"    {MES[rn]:<10} {D[rn][yy][0]*100:>8.2f}%   (SPY {D[rn][yy][1]*100:>7.2f}%)")
    print(f"    {'MEZCLA':<10} {st.mean([D[rn][yy][0] for rn in [1,2,3,4]])*100:>8.2f}%")

print("\n=== CAIDA ACUMULADA REAL 2007+2008 (dos años encadenados) ===")
for rn in [1,2,3,4]:
    d=(1+D[rn][2007][0])*(1+D[rn][2008][0])-1
    print(f"  {MES[rn]:<10}{d*100:>8.1f}%")
d4=(1+a4[0])*(1+a4[1])-1
print(f"  {'MEZCLA':<10}{d4*100:>8.1f}%")

print("\n=== ¿ES DE VERDAD MEJOR QUE EL NASDAQ? ===")
import random
for lab,serie in [('Febrero',[D[1][y][0] for y in Y]),('4 TRAMOS',a4)]:
    q = [D[1][y][2] for y in Y] if lab=='Febrero' else q4
    dif=[(x-z)*100 for x,z in zip(serie,q)]
    m=st.mean(dif); sd=st.stdev(dif); se=sd/len(dif)**0.5
    print(f"  {lab:<10} diferencia anual vs QQQ: media {m:+.2f} pp, mediana {st.median(dif):+.2f} pp")
    print(f"  {'':<10} desv.tipica {sd:.1f} pp, error tipico {se:.2f} pp -> t = {m/se:.2f}")
    print(f"  {'':<10} gana en {sum(1 for x in dif if x>0)}/{len(dif)} años")
    # bootstrap por años
    B=20000; cnt=0
    for _ in range(B):
        s=[random.choice(dif) for _ in dif]
        if st.mean(s)<=0: cnt+=1
    print(f"  {'':<10} bootstrap: P(ventaja<=0) = {cnt/B:.3f}\n")

print("=== AJUSTE POR DIVIDENDOS (QQQ rinde ~0.6%/año, nuestras pequeñas ~1.0-1.3%) ===")
print("  Contra el SPY el ajuste NOS RESTA ~0.8 pp (el SPY reparte mas que nosotros).")
print("  Contra el QQQ el ajuste NOS SUMA  ~0.5 pp (nosotros repartimos mas que el QQQ).")
print(f"  -> 4 tramos vs NASDAQ en retorno total: {(c4-cq4)*100+0.5:+.2f} pp aprox.")
