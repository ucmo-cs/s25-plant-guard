import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
df = pd.read_csv(r'G:\My Drive\CS4920 Senior Project\SeniorProject\plant_training_data.csv')

feature_columns = ['soil_moisture','temperature','humidity','lux','plant_health_status','previous_plant_health_status','plant_unique_id','hour','delta_temp','delta_humidity','delta_light']
target_columns = ['recommended_temp','recommended_humidity','recommended_light']

X = df[feature_columns]
y = df[target_columns]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

base_model = RandomForestRegressor(n_estimators=100, random_state=42)
model = MultiOutputRegressor(base_model)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("MAE (Temp):", mean_absolute_error(y_test.iloc[:,0], y_pred[:,0]))
print("MAE (Humidity):", mean_absolute_error(y_test.iloc[:,1], y_pred[:,1]))
print("MAE (Light):", mean_absolute_error(y_test.iloc[:,2], y_pred[:,2]))

joblib.dump(model, "environmental_adjustment_model.pkl")