import statistics as st
rows=[]
for line in open('liq_data.txt'):
    p=line.split(); tk=p[0]
    obs=[(float(x.split('/')[0]), float(x.split('/')[1])*1000) for x in p[1:]]
    rows.append(dict(tk=tk, px=st.median([o[0] for o in obs]),
                     adv=st.median([a*b for a,b in obs])))
rows.sort(key=lambda r:r['adv'])
FX=1.08

def com(pos,px):  # IBKR fixed: 0.005 $/accion, min 1$, max 1% del importe
    return min(max((pos/px)*0.005,1.00), pos*0.01)

print("=== FILTRO DE LIQUIDEZ SOBRE LA CARTERA DE HOY ===")
for umbral in [1e6,2e6,5e6,10e6]:
    fuera=[r['tk'] for r in rows if r['adv']<umbral]
    print(f"  ADV$ minimo {umbral/1e6:>4.0f} M$ -> caen {len(fuera):>2} nombres  {', '.join(fuera) if fuera else '(ninguno)'}")

keep=[r for r in rows if r['adv']>=2e6]
print(f"\nCartera tras filtro 2 M$: {len(keep)} nombres. Nuevo cuello de botella: {keep[0]['tk']} ({keep[0]['adv']:,.0f} $/dia)")

print("\n=== CAPACIDAD ===")
for lab,pool in [('Cartera actual (43)',rows),('Con filtro ADV>=2M$ (42)',keep)]:
    n=len(pool)
    c5=min(r['adv'] for r in pool)*0.05*n
    c10=min(r['adv'] for r in pool)*0.10*n
    print(f"  {lab:<26} 5% ADV: {c5:>13,.0f} $   10% ADV: {c10:>13,.0f} $")

print("\n=== COSTE DE COMISIONES POR CONFIGURACION (IBKR fixed, ida y vuelta) ===")
print(f"{'Budget EUR':>11}", end='')
for lab in ['43 nombres','21 (cap>=1B)','116 (4 tramos)']:
    print(f"{lab:>16}", end='')
print()
for bud in [5000,10000,20000,50000,100000]:
    usd=bud*FX
    print(f"{bud:>11,}", end='')
    for nn in [43,21,116]:
        pool=rows[:nn] if nn<=43 else rows
        pos=usd/nn
        mult = 1 if nn<=43 else 116/43
        tot=sum(com(pos,r['px']) for r in rows)*2*(nn/43 if nn>43 else 1)
        # aproximacion: mismo perfil de precios, nn posiciones
        tot=sum(com(pos, r['px']) for r in rows)*2 * (nn/43)
        print(f"{tot/usd*100:>15.2f}%", end='')
    print()

print("\n=== PRESUPUESTO MINIMO PARA QUE LA COMISION NO SE COMA LA VENTAJA ===")
print("  (regla: comisiones < 10% del alfa; alfa de referencia 9.8 pp neto de dividendos)")
for nn,lab in [(43,'43 nombres'),(21,'21 nombres'),(116,'4 tramos, 116')]:
    for bud in range(2000,300000,500):
        usd=bud*FX; pos=usd/nn
        tot=sum(com(pos,r['px']) for r in rows)*2*(nn/43)
        if tot/usd*100 < 0.98: break
    print(f"  {lab:<16} minimo ~ {bud:>7,} EUR   (comision {tot/usd*100:.2f}%)")
