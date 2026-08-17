import numpy as np
from math import comb
# yr, cal, cal_t2, med_t1, med_all, ctrlAM, ctrlNZ   (mediana rel20, %)
D=[(2007,37.41,50.89,28.24,-3.57,0.15,32.86),(2008,33.32,27.36,6.54,-14.31,-5.77,15.86),
(2009,19.55,11.19,46.15,8.43,5.82,18.12),(2010,17.55,21.99,20.80,-4.16,-2.91,4.56),
(2011,18.24,33.52,8.21,-20.99,-16.44,-11.45),(2012,18.62,23.38,-2.40,-8.07,2.43,-11.37),
(2013,2.46,-9.63,-17.92,-19.66,-15.12,-12.62),(2014,-20.52,-31.73,-10.06,-26.69,-20.52,-26.87),
(2015,-18.69,-5.15,-25.40,-25.05,-22.70,-20.98),(2016,-9.96,-21.79,-0.27,-19.08,-14.84,-13.89),
(2017,-22.13,-25.25,-22.86,-23.26,-23.26,-22.01),(2018,-7.64,-16.99,-13.48,-24.20,-23.13,-19.04),
(2019,-9.87,-21.17,-23.94,-33.40,-32.09,-21.81),(2020,-11.33,2.50,-14.91,-25.25,-21.75,-15.05),
(2021,-13.32,-7.96,-9.47,-24.88,-21.53,-28.05)]
A=np.array(D,float); yr=A[:,0].astype(int)
cal,cal_t2,med_t1,med_all,am,nz = A[:,1],A[:,2],A[:,3],A[:,4],A[:,5],A[:,6]

def test(d,label):
    n=len(d); m=d.mean(); se=d.std(ddof=1)/np.sqrt(n); t=m/se
    pos=int((d>0).sum())
    # test de signos exacto, dos colas
    p=2*sum(comb(n,k) for k in range(max(pos,n-pos),n+1))/2**n
    p=min(p,1.0)
    print(f"{label:<42}{m:>8.2f}{se:>8.2f}{t:>7.2f}{pos:>5}/{n:<4}{p:>9.4f}")

print(f"{'contraste (dif. de medianas anuales, pp)':<42}{'media':>8}{'EE':>8}{'t':>7}{'signos':>10}{'p_signos':>9}")
print("-"*84)
test(cal-med_all,   "H3-amplia: CALIDAD - MEDIOCRE (todas)")
test(cal_t2-med_t1, "H3-preregistrada: CAL-T2 - MED-T1")
test(cal-med_t1,    "CALIDAD (todas) - MEDIOCRE-T1 barato")
test(am-nz,         "H5 control negativo: A-M menos N-Z")
print()
print("Efecto principal (H3-amplia) media  = %+.1f pp"%(cal-med_all).mean())
print("Control negativo (H5)        media  = %+.1f pp  -> %.0f%% del efecto principal"
      %((am-nz).mean(), 100*abs((am-nz).mean())/abs((cal-med_all).mean())))
print()
# backtest ciego: congelado <=2016, evaluado 2017+
for lo,hi,nm in [(2007,2016,"EN MUESTRA  2007-2016"),(2017,2021,"FUERA MUESTRA 2017-2021")]:
    m=(yr>=lo)&(yr<=hi)
    print(f"{nm}: CALIDAD-MEDIOCRE = {(cal-med_all)[m].mean():+6.2f} pp   "
          f"CAL_T2-MED_T1 = {(cal_t2-med_t1)[m].mean():+6.2f} pp   (n={m.sum()} cohortes)")
