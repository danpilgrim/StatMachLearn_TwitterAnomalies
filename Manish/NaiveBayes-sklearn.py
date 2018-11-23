#!/usr/bin/env python
# coding: utf-8

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


# # Naive Bayes & kNN
# 
# In this notebook we will train Guassian Naive Bayes and kNN classifier over vectored models. But this time we will implement TF-IDF. Logisitc regression behaves better no matter what as it is generally act well with binary classifiers. But Naive bayes and kNN may take a lot of time to perform if provided with large sparse matrices and may not perform well in real time. Thus, we will use **term frequency-inverse document frequency(TF-IDF)** to provide a more accurate and better results in GNB and kNN. TFIDF simply converts count vector into frequency vector thus eliminating risk of high weightage for repeated words. (Please refer report for further detail on TFIDF)

# In[2]:


X = frame.content
y = frame.Normal
print X.shape
print y.shape


# In[3]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)


# In[4]:


from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)
feature_names = vectorizer.get_feature_names()
print len(feature_names)


# In[5]:


from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train)
X_train_tf = tf_transformer.transform(X_train)
X_train_tf.shape


# In[7]:


from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tf, y_train)


# In[8]:


print clf.score(X_test, y_test)


# In[11]:


from sklearn.metrics import confusion_matrix
pred_naivebayes = clf.predict(X_test)
confusion = confusion_matrix(y_test, pred_naivebayes)
print confusion


# Naive bayes gave a high 89% accuracy. Also, algorithm performed better and faster due to TF-IDF implementation.

# # k-NearestNeighbor

# In[12]:


print "false positive : 2226"
print "false negative : 11051"


# In[16]:


from sklearn.neighbors import KNeighborsClassifier
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X_train, y_train) 


# In[17]:


print neigh.score(X_test, y_test)


# In[19]:


from sklearn.metrics import confusion_matrix
pred_knn = neigh.predict(X_test)
confusion = confusion_matrix(y_test, pred_knn)
print confusion


# In[ ]:


print "false positive : 5626"
print "false negative : 21286"


# kNN didnot perform well which we could have guessed before as it does not classify binary data with less resemblence. We could have changed neighbors but that did not have changed much. 
