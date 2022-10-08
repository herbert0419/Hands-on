#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import pickle


# In[3]:


url = '/home/leo0419/Desktop/Breast_Cancer.csv'
Data = pd.read_csv(url)
Data.head()


# In[4]:


Data.shape


# In[5]:


Data.dtypes


# In[8]:


x = Data.iloc[:,2:].values
y = Data.iloc[:,1].values


# In[9]:


x


# In[10]:


y


# In[11]:


from sklearn.model_selection import train_test_split


# In[12]:


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)


# In[13]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(x_train)

x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)


# In[14]:


x_train


# In[15]:


from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier (n_neighbors=9)
classifier.fit(x_train, y_train)


# In[16]:


y_pred = classifier.predict(x_test)
y_pred


# In[18]:


y_pred = classifier.predict(x_test)
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
# Saving model to disk
pickle.dump(classifier, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(classifier.predict([[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.1,0.2,0.3]]))
