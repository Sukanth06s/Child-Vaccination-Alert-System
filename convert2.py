import pandas as pd
import os
input_path=r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\datasetfinal\finalone.csv"
output_path=r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines"
df=pd.read_csv(input_path)
generic=["v012","v106","v190","v025","v101","b4","bord","m14","m15","m17","m18","h1","v113","v116"]
vaccines=["h2","h3","h5","h7","h4","h6","h8","h0","h9","h9a","h50","h51","h52","h53","h57","h58","h59","h61","h62","h63"]

grace={
    "h2":  0,   # BCG
    "h0":  0,   # Polio 0
    "h50": 0,   # HepB birth

    # 6 weeks → 3 months
    "h3":  3,   # DPT1
    "h4":  3,   # Polio1
    "h51": 3,   # Penta1
    "h61": 3,   # HepB1
    "h57": 3,   # Rota1

    # 10 weeks → 4 months
    "h5":  4,   # DPT2
    "h6":  4,   # Polio2
    "h52": 4,   # Penta2
    "h62": 4,   # HepB2
    "h58": 4,   # Rota2

    # 14 weeks → 5 months
    "h7":  5,   # DPT3
    "h8":  5,   # Polio3
    "h53": 5,   # Penta3
    "h63": 5,   # HepB3
    "h59": 5,   # Rota3

    # measles
    "h9":  10,  # Measles 1
    "h9a": 16   # Measles 2
}

bcg=df[generic+["h2"]].copy()
bcg=bcg[bcg["h2"].notna()]
bcg=bcg.rename(columns={"h2":"label"})
bcg.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\bcg.csv",index=False)

polio0=df[generic+["h0"]].copy()
polio0=polio0[polio0["h0"].notna()]
polio0=polio0.rename(columns={"h0":"label"})
polio0.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\polio0.csv",index=False)

hepBBirth=df[generic+["h50"]].copy()
hepBBirth=hepBBirth[hepBBirth["h50"].notna()]
hepBBirth=hepBBirth.rename(columns={"h50":"label"})
hepBBirth.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\hepBBirth.csv",index=False)

for(v,name)in[("h3","dpt1"),("h4","polio1"),("h51","penta1"),("h61","hepb1"),("h57","rota1")]:
    d=df[df["b19"]>=grace[v]][generic+[v]+["h2","h0","h50"]]
    d=d[d[v].notna()]
    d=d.rename(columns={v:"label"})
    d.to_csv(os.path.join(output_path,f"{name}.csv"),index=False)

for(v,name,prev)in[("h5","dpt2","h3"),("h6","polio2","h4"),("h52","penta2","h51"),("h62","hepb2","h61"),("h58","rota2","h57")]:
    d=df[df["b19"]>=grace[v]][generic+[v]+[prev]+["v157","v158","v159"]]
    d=d[d[v].notna()]
    d=d.rename(columns={v:"label"})
    d.to_csv(os.path.join(output_path,f"{name}.csv"),index=False)

dpt3=df[df["b19"]>=grace["h7"]][generic+["h7"]+["h3","h5","v467d"]].copy()
dpt3=dpt3[dpt3["h7"].notna()]
dpt3=dpt3.rename(columns={"h7":"label"})
dpt3.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\dpt3.csv",index=False)

polio3=df[df["b19"]>=grace["h8"]][generic+["h8"]+["h0","h4","h6","v467d"]].copy()
polio3=polio3[polio3["h8"].notna()]
polio3=polio3.rename(columns={"h8":"label"})
polio3.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\polio3.csv",index=False)

pentavalent3=df[df["b19"]>=grace["h53"]][generic+["h53"]+["h51","h52","v467d"]].copy()
pentavalent3=pentavalent3[pentavalent3["h53"].notna()]
pentavalent3=pentavalent3.rename(columns={"h53":"label"})
pentavalent3.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\pentavalent3.csv",index=False)

HepB3=df[df["b19"]>=grace["h63"]][generic+["h63"]+["h50","h61","h62","v467d"]].copy()
HepB3=HepB3[HepB3["h63"].notna()]
HepB3=HepB3.rename(columns={"h63":"label"})
HepB3.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\HepB3.csv",index=False)

Rota3=df[df["b19"]>=grace["h59"]][generic+["h59"]+["h57","h58","v467d"]].copy()
Rota3=Rota3[Rota3["h59"].notna()]
Rota3=Rota3.rename(columns={"h59":"label"})
Rota3.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\Rota3.csv",index=False)

Measles1=df[df["b19"]>=grace["h9"]][generic+["h9"]+["v481"]].copy()
Measles1=Measles1[Measles1["h9"].notna()]
Measles1=Measles1.rename(columns={"h9":"label"})
Measles1.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\Measles1.csv",index=False)

Measles2=df[df["b19"]>=grace["h9a"]][generic+["h9a"]+["v155","v481","h9"]].copy()
Measles2=Measles2[Measles2["h9a"].notna()]
Measles2=Measles2.rename(columns={"h9a":"label"})
Measles2.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\Measles2.csv",index=False)