#!/usr/bin/env python
# coding: utf-8

# # Logistic Regression with Count Vectorizer
# 
# We will try to apply Logistic Regression over our hot encoded data which is converted into sparse matrices by count vectorizer method. Hot encoded data does not contain any other column than tweets. These tweets are marked as 1 or 0 for being bot or normal. We will only include normal column as it is boolean, it will be sufficient for us to detect which one is bot or not.

# In[1]:


import glob
import pandas as pd
import os as os
import matplotlib.pyplot as plt
import numpy as np


path =r'Data/'
frame = pd.DataFrame()
frame =pd.read_csv('Data/tweetData.csv',index_col=None, header=0, usecols=[1,2])
print frame.info()


# In[2]:


print frame.shape
print frame.head(10)


# In[3]:


print frame.Normal.value_counts()


# In[4]:


X = frame.content
y = frame.Normal
print X.shape
print y.shape


# # Count Vectorizer
# First we will import sklearn library to divide data into test and training dataset. Later we will use sklearn library to convert this data into vectors. These vectors will be sparse matrices containg count of every word that occured in the tweet. This way we will know that which word trolls used most and will help us to detect them among other tweets.

# In[5]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)


# In[6]:


print X_train.shape
print X_test.shape
print y_train.shape
print y_test.shape


# In[7]:


print np.bincount(y_train)


# In[8]:


from sklearn.feature_extraction.text import CountVectorizer


# In[9]:


vectorizer = CountVectorizer()


# In[10]:


X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)


# In[11]:


feature_names = vectorizer.get_feature_names()


# In[12]:


print len(feature_names)


# In[13]:


import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
scores = cross_val_score(LogisticRegression(), X_train, y_train,cv=5)
print np.mean(scores)


# # Logistic Regression
# After completeing vectorization we will run our logistic regression algorithm over vectored data. We can clearly see that how logistic regression quickly converges and gives us upto 92% accuracy. We can say that logisitc regression is one of the most accurate to run over binary classifications. In the end we created a confusion matrix to show false positives and false negatives.

# In[14]:


logreg = LogisticRegression()
logreg.fit(X_train,y_train)
print logreg.score(X_train,y_train)
print logreg.score(X_test, y_test)


# In[15]:


from sklearn.metrics import confusion_matrix
pred_logreg = logreg.predict(X_test)
confusion = confusion_matrix(y_test, pred_logreg)
print confusion


# In[2]:


print ("false positive : 3987")
print ("false negative : 4465")

