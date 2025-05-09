import pandas as pd
'''
# Load dataset
df = pd.read_csv('G:\\My Drive\\CS4920 Senior Project\\SeniorProject\\plant_health_data.csv')

# List of columns we want to keep 
columns_to_keep = ['Timestamp', 'Plant_ID', 'Soil_Moisture', 'Ambient_Temperature', 'Humidity', 'Light_Intensity', 'Plant_Health_Status']

# Make df only keep those columns 
df = df[columns_to_keep]

# Create mapping for Plant Health Status
health_mapping = {
    "High Stress": 0,
    "Moderate Stress": 1,
    "Healthy": 2
}

# Change categorical Plant_Health_Status to numerical using health_mapping
df["Plant_Health_Status"] = df["Plant_Health_Status"].map(health_mapping)

# Convert timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Sort by Plant_ID and Timestamp
df = df.sort_values(by=['Plant_ID', 'Timestamp']).reset_index(drop=True)

# Create mapping for plant or pi column (combining both PlantID and PiID)
plant_or_pi_mapping = {
    1: "plant1",
    2: "plant2",
    3: "plant3",
    4: "plant4",
    5: "plant5",
    6: "plant6",
    7: "plant7",
    8: "plant8",
    9: "plant9",
    10: "plant10",
    "raspPi1": "raspPi1",
    "raspPi2": "raspPi2"
}

# Apply mapping to the Plant_ID column to create 'Plant_Pi_ID' column
df["Plant_Pi_ID"] = df["Plant_ID"].map(plant_or_pi_mapping)

# Create mapping for plant unique IDs (mapping plant and Pi to numeric IDs)
plant_unique_id_mapping = {
    "plant1": 1,
    "plant2": 2,
    "plant3": 3,
    "plant4": 4,
    "plant5": 5,
    "plant6": 6,
    "plant7": 7,
    "plant8": 8,
    "plant9": 9,
    "plant10": 10,
    "raspPi1": 11,
    "raspPi2": 12
}

# Map plant unique id mapping to Plant_Unique_ID
df['Plant_Unique_ID'] = df['Plant_Pi_ID'].map(plant_unique_id_mapping)

#add previous values 
df['previousSoilMoisture'] = df.groupby('Plant_ID')['Soil_Moisture'].shift(1)
df['previousPlantHealthStatus'] = df.groupby('Plant_ID')['Plant_Health_Status'].shift(1)

#add time based features 
df['hour'] = df['Timestamp'].dt.hour
df['day'] = df['Timestamp'].dt.day
df['month'] = df['Timestamp'].dt.month
df['weekday'] = df['Timestamp'].dt.weekday  # Monday=0, Sunday=6

# Create rolling average of soil moisture (e.g., 3 previous readings)
df['rolling_avg_soil_moisture'] = df.groupby('Plant_ID')['Soil_Moisture'].rolling(3, min_periods=1).mean().reset_index(drop=True)

# Fill NaN values for first rows (if necessary)
df['previousSoilMoisture'].fillna(method='bfill', inplace=True)
df['previousPlantHealthStatus'].fillna(method='bfill', inplace=True)

#calculate time to dry (for watering schedule optimization)
MOISTURE_THRESHOLD = 30
MAX_LOOKAHEAD = 10


time_to_dry_list = []

for idx, row in df.iterrows():
    plant_id = row['Plant_ID']
    current_moisture = row['Soil_Moisture']
    current_health = row['Plant_Health_Status']
    base_time = row['Timestamp']

    # Look ahead for up to MAX_LOOKAHEAD steps
    future_rows = df[(df['Plant_ID'] == plant_id) & (df['Timestamp'] > base_time)].head(MAX_LOOKAHEAD)

    label_found = False
    for i, (_, future_row) in enumerate(future_rows.iterrows(), start=1):
        future_moisture = future_row['Soil_Moisture']
        future_health = future_row['Plant_Health_Status']
        
        # Trigger if moisture too low OR health begins to drop
        if future_moisture < MOISTURE_THRESHOLD or future_health < current_health:
            time_to_dry_list.append(i * 6)  # Each step = 6 hours
            label_found = True
            break

    if not label_found:
        time_to_dry_list.append(MAX_LOOKAHEAD * 6)

#add time to dry column
df['time_to_dry'] = time_to_dry_list

df.drop(columns=['Plant_ID'], inplace=True)

#add delta fields for anomaly detection:
# Group by plant and calculate deltas
df['delta_soil_moisture'] = df.groupby('Plant_Unique_ID')['Soil_Moisture'].diff()
df['delta_temp'] = df.groupby('Plant_Unique_ID')['Ambient_Temperature'].diff()
df['delta_humidity'] = df.groupby('Plant_Unique_ID')['Humidity'].diff()
df['delta_light'] = df.groupby('Plant_Unique_ID')['Light_Intensity'].diff()

# Optionally: fill NaNs (created by diff) with 0 or forward-fill
df.fillna(0, inplace=True)

df.to_csv("wso_processed_dataset.csv", index = False)
'''

df = pd.read_csv(r'G:\My Drive\CS4920 Senior Project\SeniorProject\plant_health_training_data.csv')
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour

IDEAL_TEMP_MIN, IDEAL_TEMP_MAX = 22, 26
IDEAL_HUMIDITY_MIN, IDEAL_HUMIDITY_MAX = 50, 70
IDEAL_LIGHT_MIN, IDEAL_LIGHT_MAX = 200, 600
DAY_START, DAY_END = 6, 20


#clamp helper function
def clamp(value, min_val, max_val):
    return max(min(value, max_val), min_val)

#target assignment function 
def assign_targets(row):
    if row['plant_health_status'] == 2:
        #needs no adjustments, so assign current values to the target values
        target_temp = row['temperature']
        target_humidity = row['humidity']
        target_light = row['lux']
    else:
        #recommend values clamped into ideal ranges
        target_temp = clamp(row['temperature'], IDEAL_TEMP_MIN, IDEAL_TEMP_MAX)
        target_humidity = clamp(row['humidity'], IDEAL_HUMIDITY_MIN, IDEAL_HUMIDITY_MAX)
        
        #only recommend light adjustments during daylight hours (doesn't recommend more light during nighttime hours)
        if DAY_START <=  row['hour'] <=DAY_END:
            target_light = clamp(row['lux'], IDEAL_LIGHT_MIN, IDEAL_LIGHT_MAX)
        #if nighttime leave as is
        else:
            target_light = row['lux']
    return pd.Series([target_temp, target_humidity, target_light])

df[['recommended_temp', 'recommended_humidity','recommended_light']] = df.apply(assign_targets, axis = 1)

df.to_csv("plant_training_data.csv", index = False)


