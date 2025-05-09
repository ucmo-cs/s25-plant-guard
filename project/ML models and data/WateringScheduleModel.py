import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

#load training data
df = pd.read_csv('G:\\My Drive\\CS4920 Senior Project\\SeniorProject\\wso_processed_dataset.csv')

#define X and Y (features and target)
#make X (All attributes other than target)
X = df[['Soil_Moisture', 'Ambient_Temperature', 'Humidity', 'Light_Intensity', 'Plant_Health_Status', 
            'previousSoilMoisture', 'previousPlantHealthStatus', 
            'rolling_avg_soil_moisture', 'Plant_Unique_ID']]

#make Y (target attribute)
y = df['time_to_dry']

#check if shape/length are the same
print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

#split data into testing and training 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#initialize random forest regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state= 42)

#train model
rf_model.fit(X_train, y_train)

#predict on the test set
y_pred = rf_model.predict(X_test)

#evaluate the model using MAE (Mean Absolute Error)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error (MAE): {mae}")

#with hour day day_of_week MAE = 4.201
#without MAE = 4.02325

#save the trained model
model_filename = 'water_schedule_rf_model.pkl'
joblib.dump(rf_model, model_filename)
