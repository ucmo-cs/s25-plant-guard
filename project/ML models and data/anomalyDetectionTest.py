import pandas as pd
import joblib


model = joblib.load("anomaly_detection_model.pkl")
scaler = joblib.load("anomaly_scaler.pkl")


df = pd.read_csv("wso_processed_dataset.csv")
test_sample = df[df['hour'].between(8, 18)].head(10).copy()


features = [
    'Soil_Moisture', 'Ambient_Temperature', 'Humidity', 'Light_Intensity',
    'delta_soil_moisture', 'delta_temp', 'delta_humidity', 'delta_light',
    'rolling_avg_temp', 'rolling_std_soil'
]

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


def simulate_failure(base_df, failure_name, modifier_func):
    rows = base_df.copy()
    rows = modifier_func(rows)

  
    rows = rows.reset_index(drop=True)
    rows['rolling_avg_temp'] = rows['Ambient_Temperature'].rolling(3, min_periods=1).mean()
    rows['rolling_std_soil'] = rows['Soil_Moisture'].rolling(3, min_periods=1).std().fillna(0)


    X = rows[features].fillna(0).astype(float)
    X_scaled = scaler.transform(X)
    rows['anomaly_score'] = model.decision_function(X_scaled)
    rows['is_anomaly'] = pd.Series(model.predict(X_scaled), index=rows.index).map({1: 0, -1: 1})
    rows['anomaly_description'] = rows.apply(describe_anomaly, axis=1)


    rows['Timestamp'] = pd.to_datetime(rows['Timestamp']).dt.strftime('%m-%d %H:%M')  # ⬅ Shorten timestamp format
    num_flagged = rows['is_anomaly'].sum()
    print(f"\n===== Simulated Failure: {failure_name} =====")
    print(f"{int(num_flagged)}/{len(rows)} rows flagged as anomalies")
    print(rows[['Timestamp', 'is_anomaly', 'anomaly_score', 'anomaly_description']])

def fail_light(rows):
    rows['Light_Intensity'] = 0
    rows['delta_light'] = 0
    return rows

def fail_heater(rows):
    rows['Ambient_Temperature'] = 35
    rows['delta_temp'] = 0
    return rows

def fail_humidity(rows):
    rows['Humidity'] = 10
    rows['delta_humidity'] = 0
    return rows

def fail_soil_sensor(rows):
    rows['Soil_Moisture'] = rows['Soil_Moisture'].iloc[0]  # Flat value
    rows['delta_soil_moisture'] = 0
    return rows

simulate_failure(test_sample, "Grow Light Failure", fail_light)
simulate_failure(test_sample, "Heater Stuck On", fail_heater)
simulate_failure(test_sample, "Humidifier Failure", fail_humidity)
simulate_failure(test_sample, "Soil Moisture Sensor Failure", fail_soil_sensor)
