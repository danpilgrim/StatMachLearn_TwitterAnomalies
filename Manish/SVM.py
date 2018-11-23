#!/usr/bin/env python
# coding: utf-8

# # Implementation of Support Vector Machine (SVM)
# 
# We implemented svm in this notebook. As we know Support Vector Machine (SVM) is another great classifier that can be used to classify binary data. Below results will show that SVM performed very well in term of performance but took a really long time to train. We used only linear classifier, as there was no use to implement any kernel for binary data.

# In[1]:


import glob
import os as os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path =r'Data/'
frame = pd.DataFrame()
frame =pd.read_csv('Data/tweetData.csv',index_col=None, header=0, usecols=[1,2])
print (frame.info())
X = frame.content
y = frame.Normal
print (X.shape)
print (y.shape)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)
feature_names = vectorizer.get_feature_names()
print (len(feature_names))
from sklearn import svm
clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(X_train,y_train)


# In[10]:


print (clf.score(X_test,y_test))


# In[16]:


from sklearn.metrics import confusion_matrix
pred_svm = clf.predict(X_test)
confusion = confusion_matrix(y_test, pred_svm)
print (confusion)


# In[17]:


print ("False positive : 3114")
print ("False negative : 4058")

