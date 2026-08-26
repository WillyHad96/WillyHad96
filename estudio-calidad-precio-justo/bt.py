import numpy as np
# yr, n_perfil, n_nuevas, n_retenidas, n_cartera, con_regla, solo_1anio, spy
D=[(2008,122,28,0,28,-38.87,-38.87,-41.21),(2009,119,21,14,35,41.88,34.41,45.09),
(2010,124,18,14,32,39.53,51.14,20.89),(2011,120,16,7,23,19.91,21.15,2.67),
(2012,114,29,7,36,23.38,23.51,12.45),(2013,122,29,14,43,42.93,47.49,21.94),
(2014,141,29,14,43,7.37,5.87,12.59),(2015,145,35,13,48,-11.19,-13.63,-6.18),
(2016,149,26,21,47,37.69,33.15,25.54),(2017,151,26,13,39,24.74,28.76,16.33),
(2018,149,29,13,42,15.27,22.10,1.04),(2019,175,39,14,53,20.21,20.47,15.69),
(2020,172,46,17,63,47.05,50.05,27.83),(2021,174,33,25,58,0.57,-7.10,13.70),
(2022,172,26,19,45,7.35,14.10,-8.44),(2023,204,48,15,63,38.26,37.64,21.97),
(2024,223,61,22,83,28.72,29.25,19.00)]
A=np.array(D,float); yr=A[:,0].astype(int)
rot=A[:,2]/A[:,4]                      # rotacion real con la regla
c_regla=rot*2*0.003                    # 0,30% por lado
c_1anio=np.full(len(A),1.0*2*0.003)    # rotacion total
reg=A[:,5]/100-c_regla; uno=A[:,6]/100-c_1anio; spy=A[:,7]/100
RF=0.02
def st(r,lab,extra=""):
    k=len(r); cagr=np.prod(1+r)**(1/k)-1; vol=r.std(ddof=1)
    beta=np.cov(r,spy,ddof=1)[0,1]/np.var(spy,ddof=1)
    alpha=(r.mean()-RF)-beta*(spy.mean()-RF)
    ins=yr<=2016; out=yr>=2017
    ci=np.prod(1+r[ins])**(1/ins.sum())-1; co=np.prod(1+r[out])**(1/out.sum())-1
    print(f"{lab:<34}{100*cagr:>8.2f}{100*vol:>7.1f}{(cagr-RF)/vol:>8.2f}{beta:>6.2f}{100*alpha:>7.2f}"
          f"{100*r.min():>8.1f}{100*np.mean(r>spy):>7.1f}{100*ci:>9.2f}{100*co:>9.2f}  {extra}")
print(f"{'cartera (neta de costes)':<34}{'CAGR':>8}{'vol':>7}{'Sharpe':>8}{'beta':>6}{'alfa':>7}{'peor':>8}{'%>SPY':>7}{'08-16':>9}{'17-24':>9}")
print("-"*118)
st(reg,"CON regla de salida (2 años)",f"rotacion {100*rot.mean():.0f}%/año, {A[:,4].mean():.0f} nombres")
st(uno,"SOLO 1 año (lo anterior)",f"rotacion 100%/año, {A[:,2].mean():.0f} nombres")
st(spy,"SPY")
print(f"\nMejora de la regla de salida: {100*(np.prod(1+reg)**(1/len(reg))-np.prod(1+uno)**(1/len(uno))):+.2f} pp de CAGR")
print(f"Coste medio: con regla {100*c_regla.mean():.2f}%/año  ·  solo 1 año {100*c_1anio.mean():.2f}%/año")
print(f"Años en que la regla mejora: {int((reg>uno).sum())} de {len(reg)}")
