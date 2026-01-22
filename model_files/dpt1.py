import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score
import pandas as pd
input_path=r"C:\webp proj\children\vaccine_datasets\DPT1.csv"
output_path=r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\dpt1.json"
df=pd.read_csv(input_path)
x=df[['v012','v106','v025','v190','v101','b19','b4','bord']]
y=df['label']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    random_state=42,
    eval_metric="logloss"
)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
accuracy=accuracy_score(y_test,y_pred)
recall=recall_score(y_test,y_pred)
precision = precision_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("Accuracy is:",accuracy)
print("Recall is:",recall)
print("Precision is:", precision)
print("F1 Score is:", f1)
model.save_model(output_path)