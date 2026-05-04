import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

data = {
    "amount": [100, 5000, 10000, 200, 8000, 300],
    "time": [1, 2, 3, 1, 3, 2],      # 1=day, 2=evening, 3=night
    "device": [1, 2, 2, 1, 2, 1],    # 1=mobile, 2=other
    "location": [1, 2, 3, 1, 3, 1],  # 1=karachi, 2=lahore, 3=islamabad
    "fraud": [0, 1, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

X = df[["amount", "time", "device", "location"]]
y = df["fraud"]

model = RandomForestClassifier()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("MODEL TRAINED SUCCESSFULLY")