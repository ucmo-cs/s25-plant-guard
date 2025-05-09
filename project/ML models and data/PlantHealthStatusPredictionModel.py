import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier


#Load the dataset: 
data = pd.read_csv(r"G:\My Drive\CS4920 Senior Project\SeniorProject\plant_training_data.csv")

if 'timestamp' in data.columns:
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['Year'] = data['timestamp'].dt.year
    data['Month'] = data['timestamp'].dt.month
    data['Day'] = data['timestamp'].dt.day
    data['Hour'] = data['timestamp'].dt.hour
    data = data.drop(columns=['timestamp'])

#make X (All attributes other than target)
X = data.drop(columns=['plant_health_status','anomaly_description','pieId'])

#make Y (target attribute)
y = data['plant_health_status']

#split the data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#create DMatrix objects for XGBoost 
train_dmatrix = xgb.DMatrix(X_train, label = y_train)
test_dmatrix = xgb.DMatrix(X_test, label = y_test)

#paramgrid to find most effective parameters for XGBoost 

# from sklearn.model_selection import GridSearchCV
# from xgboost import XGBClassifier

# xgb_model = XGBClassifier(objective='multi:softmax', num_class=len(np.unique(y)))

# param_grid = {
#     'max_depth': [6, 8, 10],
#     'learning_rate': [0.01, 0.1, 0.2],
#     'n_estimators': [100, 200, 300],
#     'subsample': [0.7, 0.8, 0.9],
#     'colsample_bytree': [0.7, 0.8, 0.9],
# }

# grid_search = GridSearchCV(xgb_model, param_grid, scoring='accuracy', cv=5)
# grid_search.fit(X_train, y_train)

# print("Best Parameters:", grid_search.best_params_)

#returned Best Parameters: {'colsample_bytree': 0.7, 'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 200, 'subsample': 0.9}


#define XGBoost parameters 
params = {
    'objective': 'multi:softmax',  # Adjust based on your problem type
    'num_class': len(np.unique(y)),  # Number of unique classes in the dataset
    'eval_metric': 'mlogloss',
    'max_depth': 6,
    'eta': 0.01,
    'subsample': 0.9,
    'colsample_bytree': 0.7,
}

#train the model 
num_round = 200
bst = xgb.train(params, train_dmatrix, num_round)

#make predictions 
preds = bst.predict(test_dmatrix)

#Evaluate the model 
accuracy = accuracy_score(y_test, preds)
print(f'Accuracy: {accuracy:.4f}')




