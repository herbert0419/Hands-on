# necessary imports 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle

import warnings
warnings.filterwarnings('ignore')

plt.style.use('ggplot')

df = pd.read_csv("insurance_claims.csv")

df.replace('?', np.nan, inplace = True)
df['collision_type'] = df['collision_type'].fillna(df['collision_type'].mode()[0])
df['property_damage'] = df['property_damage'].fillna(df['property_damage'].mode()[0])
df['police_report_available'] = df['police_report_available'].fillna(df['police_report_available'].mode()[0])

to_drop = ['policy_number','policy_bind_date','policy_state','insured_zip','incident_location','incident_date',
           'incident_state','incident_city','insured_hobbies','auto_make','auto_model','auto_year', '_c39']

df.drop(to_drop, inplace = True, axis = 1)

df.drop(columns = ['age', 'total_claim_amount'], inplace = True, axis = 1)

X = df.drop('fraud_reported', axis = 1)
y = df['fraud_reported']

cat_df = X.select_dtypes(include = ['object'])

cat_df = pd.get_dummies(cat_df, drop_first = True)
num_df = X.select_dtypes(include = ['int64'])

X = pd.concat([num_df, cat_df], axis = 1)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

num_df = X_train[['months_as_customer', 'policy_deductable', 'umbrella_limit',
       'capital-gains', 'capital-loss', 'incident_hour_of_the_day',
       'number_of_vehicles_involved', 'bodily_injuries', 'witnesses', 'injury_claim', 'property_claim',
       'vehicle_claim']]

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaled_data = scaler.fit_transform(num_df)

scaled_num_df = pd.DataFrame(data = scaled_data, columns = num_df.columns, index = X_train.index)

X_train.drop(columns = scaled_num_df.columns, inplace = True)

X_train = pd.concat([scaled_num_df, X_train], axis = 1)

from sklearn.svm import SVC

svc = SVC()
svc.fit(X_train, y_train)

# Saving model to disk
pickle.dump(svc, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[-0.952839742,-0.226858489,-0.489107814,-0.912192595,0.950653128,-1.111687197,-0.840213379,-0.012987355,0.466973335,-1.362158205,-1.380699146,-1.713821242,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,0,0,0,1,0,0]]))

