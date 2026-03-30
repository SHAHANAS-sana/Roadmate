import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Step 2: Data Loading
data = pd.read_csv(r'C:\Users\ramseena\PycharmProjects\roadmate\fuel_prices.csv')  # Replace with your file path


data= data.values[:,1]
# print(petrolprice)


X = []
y = []

for i in range(3, len(data)):  # Start from index 3 so that we have enough previous data
    # Features: Prices of the previous 3 days
    X.append(data[i-3:i])
    # Target: Next day's petrol price
    y.append(data[i])

# Convert lists to numpy arrays for training


# Step 4: Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train the Random Forest Model
model = RandomForestRegressor(n_estimators=100, random_state=42)  # 100 trees, can adjust
model.fit(X_train, y_train)


datas=data[len(data)-3:]
print(datas)

# Step 6: Predictions
y_pred = model.predict([datas])

print(y_pred[0])
