import numpy as np
# yr, A_dil, A_resto, B_estab, B_resto, C_perfil, C_resto, D_sin_excl_sector, n_dil, n_perf
D=[(2007,19.36,2.07,28.38,-1.26,19.36,5.86,19.36,212,88),(2008,25.04,0.05,33.71,4.98,35.01,4.99,35.01,234,103),
(2009,27.17,-9.69,33.18,5.91,35.72,5.91,35.20,246,106),(2010,6.25,1.74,16.35,-0.92,18.06,0.98,15.41,209,83),
(2011,-13.97,-14.52,6.11,-16.24,4.88,-15.95,6.36,213,80),(2012,-4.00,-4.01,17.11,-8.56,19.81,-8.56,17.50,269,97),
(2013,-7.58,-12.62,3.60,-14.89,3.60,-13.88,3.60,254,92),(2014,-18.13,-15.04,-11.62,-18.56,-11.07,-18.52,-11.99,258,102),
(2015,-19.54,-24.71,-17.07,-24.36,-16.36,-24.54,-17.56,294,118),(2016,-2.52,-22.08,4.53,-19.38,1.54,-17.93,-10.06,336,136),
(2017,-20.80,-30.71,-14.65,-30.39,-15.15,-27.96,-20.99,304,122),(2018,-6.78,-26.03,-1.02,-22.41,-0.60,-20.79,-8.15,282,109),
(2019,-13.55,-35.49,-7.93,-32.30,-5.80,-32.03,-13.11,314,134),(2020,-15.14,-31.56,-13.95,-27.67,-10.03,-27.53,-15.01,319,136),
(2021,-6.59,-25.90,-16.43,-21.87,-7.21,-22.74,-10.63,304,138)]
A=np.array(D,float); yr=A[:,0].astype(int)
BAND=5.77
def ev(d,lab,n=None):
    m=d.mean(); se=d.std(ddof=1)/np.sqrt(len(d)); ins=yr<=2016; out=yr>=2017
    tag = "OK" if abs(m)>BAND else "RUIDO"
    extra = f"  n/año {n.mean():5.0f}" if n is not None else ""
    print(f"{lab:<40}{m:>7.2f}{se:>6.2f}{m/se:>6.2f}{int((d>0).sum()):>4}/{len(d):<3}"
          f"{d[ins].mean():>8.2f}{d[out].mean():>8.2f}{tag:>7}{extra}")
print(f"{'definicion':<40}{'efecto':>7}{'EE':>6}{'t':>6}{'coh':>8}{'en-m':>8}{'fuera':>8}{'vs5.8':>7}")
print("-"*100)
ev(A[:,1]-A[:,2],"A. dilucion<2% sola (+ sin Fin/RE)",A[:,8])
ev(A[:,3]-A[:,4],"B. estabilidad sola (mb+crec, sin dil)")
ev(A[:,5]-A[:,6],"C. PERFIL completo (3 condiciones)",A[:,9])
ev(A[:,7]-A[:,6],"D. PERFIL sin excluir Fin/RE")
print()
print(f"C - A (lo que aportan margen estable + crec. consistente sobre dilucion sola): "
      f"{((A[:,5]-A[:,6])-(A[:,1]-A[:,2])).mean():+.2f} pp")
print(f"C - D (lo que aporta excluir Financials/Real Estate):                          "
      f"{(A[:,7]-A[:,5]).mean()*-1:+.2f} pp")
print(f"\nnombres/año: dilucion sola {A[:,8].mean():.0f}  ·  PERFIL {A[:,9].mean():.0f}")
