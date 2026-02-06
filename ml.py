import pandas as pd
from sklearn.linear_model import LogisticRegression

# Step 1: Training data (hours studied vs result)
data = {
    "hours": [1, 2, 3, 4, 5, 6, 7, 8],
    "result": [0, 0, 0, 1, 1, 1, 1, 1]  # 0 = Fail, 1 = Pass
}

df = pd.DataFrame(data)

# Step 2: Split input/output
X = df[["hours"]]
y = df["result"]

# Step 3: Train model
model = LogisticRegression()
model.fit(X, y)

# Step 4: Predict new value
hours = 3.5
prediction = model.predict([[hours]])

def predict_result(hours):
    prediction = model.predict([[hours]])
    return "Pass ✅" if prediction[0] == 1 else "Fail ❌"
