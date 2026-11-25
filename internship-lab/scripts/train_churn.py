"""Train and evaluate the ChurnLens Logistic Regression pipeline."""
from pathlib import Path
import json, joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

ROOT=Path(__file__).resolve().parents[1]
NUM=["tenure_months","monthly_charges_inr","support_tickets_90d","has_dependents","autopay_enabled","payment_delay_days"]
CAT=["contract_type","internet_service"]

def main():
    df=pd.read_csv(ROOT/"data/customer_churn.csv")
    X=df[NUM+CAT]; y=df["churned"].astype(int)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    num=Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler())])
    cat=Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore",sparse_output=False))])
    prep=ColumnTransformer([("num",num,NUM),("cat",cat,CAT)])
    model=Pipeline([("prep",prep),("classifier",LogisticRegression(max_iter=1500,class_weight="balanced",C=.8,random_state=42))])
    model.fit(Xtr,ytr); prob=model.predict_proba(Xte)[:,1]; pred=(prob>=.5).astype(int)
    metrics={"accuracy":round(accuracy_score(yte,pred),4),"precision":round(precision_score(yte,pred,zero_division=0),4),
      "recall":round(recall_score(yte,pred,zero_division=0),4),"f1":round(f1_score(yte,pred,zero_division=0),4),
      "roc_auc":round(roc_auc_score(yte,prob),4),"confusion_matrix":confusion_matrix(yte,pred,labels=[0,1]).tolist(),
      "train_rows":len(ytr),"test_rows":len(yte),"threshold":.5}
    fitted=model.named_steps["prep"]; clf=model.named_steps["classifier"]
    fmap=[]
    for name in fitted.get_feature_names_out():
        if name.startswith("num__"): fmap.append({"type":"numeric","name":name[5:]})
        else:
            rest=name[5:]; field=next((c for c in CAT if rest.startswith(c+"_")),None)
            fmap.append({"type":"categorical","name":field,"value":rest[len(field)+1:] if field else rest})
    scaler=fitted.named_transformers_["num"].named_steps["scale"]
    artifact={"model_name":"Logistic Regression","threshold":.5,"numeric_means":dict(zip(NUM,map(float,scaler.mean_))),
      "numeric_scales":dict(zip(NUM,map(float,scaler.scale_))),"feature_map":fmap,"weights":list(map(float,clf.coef_[0])),
      "intercept":float(clf.intercept_[0]),"metrics":metrics}
    (ROOT/"data/churn_model.json").write_text(json.dumps(artifact,indent=2),encoding="utf-8")
    joblib.dump(model,ROOT/"data/churn_pipeline.joblib")
    print(json.dumps(metrics,indent=2))

if __name__=="__main__": main()
