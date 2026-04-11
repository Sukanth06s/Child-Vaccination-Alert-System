import pandas as pd
input_path=r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\datasetfinal\finalone.csv"
output_path=output_path=r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccinesfinal"
df=pd.read_csv(input_path)
label=["h9a"]
generic=["v012","v106","v190","v025","v101","b4","bord","m14","m15","m17","m18","h1","v113","v116"]
vac=["h7","h8","h53","h63","h59","h9"]
measles2=df[df["b19"]>=16][generic+vac+label+["v481"]+["v155"]].copy()
measles2=measles2[measles2["h9a"].notna()]
measles2=measles2.rename(columns={"h9a":"label"})
measles2.to_csv(r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccinesfinal\measles2.csv",index=False)
