import statistics as st

rows=[]
for line in open('liq_data.txt'):
    p=line.split()
    tk=p[0]; obs=[]
    for x in p[1:]:
        pr,vo=x.split('/'); obs.append((float(pr), float(vo)*1000))
    dv=[pr*vo for pr,vo in obs]
    rows.append(dict(tk=tk, px=st.median([o[0] for o in obs]),
                     vol=st.median([o[1] for o in obs]),
                     adv=st.median(dv)))
rows.sort(key=lambda r:r['adv'])

print("=== VOLUMEN MEDIO DIARIO EN DOLARES (mediana, ago-2026) ===")
print(f"{'Ticker':<7}{'Precio':>9}{'Acc/dia':>12}{'ADV $':>14}{'1% ADV':>11}{'10% ADV':>12}")
for r in rows:
    print(f"{r['tk']:<7}{r['px']:>9.2f}{r['vol']:>12,.0f}{r['adv']:>14,.0f}{r['adv']*.01:>11,.0f}{r['adv']*.10:>12,.0f}")

advs=[r['adv'] for r in rows]
print(f"\nMediana ADV$ de la cartera : {st.median(advs):>14,.0f}")
print(f"Minimo (el cuello de botella): {rows[0]['tk']} {rows[0]['adv']:,.0f}")
print(f"Nombres con ADV$ < 1 M$      : {sum(1 for a in advs if a<1e6)}")
print(f"Nombres con ADV$ < 5 M$      : {sum(1 for a in advs if a<5e6)}")

# --- CAPACIDAD ---
# equiponderada: cada nombre = 1/43 de la cartera
n=len(rows)
print("\n=== CAPACIDAD DE LA CARTERA (equiponderada, 1 dia de ejecucion) ===")
for part,lab in [(0.01,'1% del ADV (muy conservador)'),
                 (0.05,'5% del ADV (prudente)'),
                 (0.10,'10% del ADV (agresivo)'),
                 (0.25,'25% del ADV (mueve el precio)')]:
    cap=min(r['adv']*part for r in rows)*n
    print(f"  {lab:<32} cartera maxima ~ {cap:>14,.0f} $")
# excluyendo el cuello de botella CPAC
r2=rows[1:]
for part,lab in [(0.05,'5% del ADV, sin el peor nombre'),(0.10,'10% del ADV, sin el peor nombre')]:
    cap=min(r['adv']*part for r in r2)*len(r2)
    print(f"  {lab:<32} cartera maxima ~ {cap:>14,.0f} $")

# --- COSTES A ESCALA PEQUENA ---
print("\n=== QUE PASA CON PRESUPUESTOS PEQUENOS ===")
print(f"{'Budget EUR':>11}{'Pos/nombre':>12}{'Acc/nombre(med)':>17}{'%ADV(peor)':>12}{'Comis/ano':>11}{'% comis':>9}")
FX=1.08  # EUR->USD aprox
for bud in [5000,10000,20000,50000,100000,250000]:
    usd=bud*FX
    pos=usd/n
    # acciones medianas por nombre
    sh=[pos/r['px'] for r in rows]
    med_sh=st.median(sh)
    worst=max(pos/r['adv'] for r in rows)*100
    # IBKR fixed: 0.005 $/accion, min 1.00 $, max 1% del valor
    def com(pos_usd, px):
        s=pos_usd/px
        return min(max(s*0.005,1.00), pos_usd*0.01)
    total=sum(com(pos,r['px']) for r in rows)*2   # compra + venta
    print(f"{bud:>11,}{pos:>12,.0f}{med_sh:>17,.0f}{worst:>11.2f}%{total:>11,.0f}{total/usd*100:>8.2f}%")
