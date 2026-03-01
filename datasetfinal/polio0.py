import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (confusion_matrix,accuracy_score,precision_score,recall_score)
input_path=r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\polio0.csv"
df=pd.read_csv(input_path)
x=df[["v012","v106","v190","v025","v101","b4","bord","m14","m15","m17","m18","h1","v113","v116"]]
y=1-df["label"]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)
missed=(y_train==1).sum()
vaccinated=(y_train==0).sum()
ratio=(vaccinated/missed)
model=xgb.XGBClassifier(    
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    scale_pos_weight=ratio,
    eval_metric="logloss",
    random_state=42
    )
model.fit(x_train,y_train)
y_prob = model.predict_proba(x_test)[:, 1]
y_pred = (y_prob >= 0.35).astype(int)
print("accuracy score:",accuracy_score(y_test,y_pred))
print("Recall:",recall_score(y_test,y_pred))
print("Precision:",precision_score(y_test,y_pred))
print("Confusion matrix:")
print(confusion_matrix(y_test,y_pred))
model.save_model("polio0.json")