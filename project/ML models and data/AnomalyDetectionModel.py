import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

#load dataset
df = pd.read_csv("wso_processed_dataset.csv")

#rolling features
df['rolling_avg_temp'] = df.groupby('Plant_Unique_ID')['Ambient_Temperature']\
    .rolling(3, min_periods=1).mean().reset_index(drop=True)

df['rolling_std_soil'] = df.groupby('Plant_Unique_ID')['Soil_Moisture']\
    .rolling(3, min_periods=1).std().reset_index(drop=True).fillna(0)

#training features
features = [
    'Soil_Moisture', 'Ambient_Temperature', 'Humidity', 'Light_Intensity',
    'delta_soil_moisture', 'delta_temp', 'delta_humidity', 'delta_light',
    'rolling_avg_temp', 'rolling_std_soil'
]

#scale features
X = df[features].fillna(0).astype(float)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#train the model
iso_forest = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
iso_forest.fit(X_scaled)

#predict
df['anomaly_score'] = iso_forest.decision_function(X_scaled)
df['is_anomaly'] = pd.Series(iso_forest.predict(X_scaled)).map({1: 0, -1: 1})

#geneerate descriptions
def describe_anomaly(row):
    if row['is_anomaly'] == 0:
        return ""
    if abs(row['delta_light']) < 0.5:
        return "Possible light issue"
    elif abs(row['delta_temp']) < 0.5:
        return "Possible heater or temp issue"
    elif abs(row['delta_humidity']) < 1:
        return "Possible humidifier failure or issue"
    elif abs(row['delta_soil_moisture']) < 0.1:
        return "Possible soil moisture sensor failure"
    else:
        return "Unusual sensor behavior"

df['anomaly_description'] = df.apply(describe_anomaly, axis=1)

#save results
df.to_csv("wso_with_improved_anomalies.csv", index=False)
joblib.dump(iso_forest, "anomaly_detection_model.pkl")
joblib.dump(scaler, "anomaly_scaler.pkl")

print("saved")
