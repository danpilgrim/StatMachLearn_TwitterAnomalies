#!/usr/bin/env python
# coding: utf-8

# # Data Analysis
# 
# we will do some basic data analysis in this file. We will take a look at how data is divided and how trolls behve. We will try to see a trend in language or which language they used for this purpose.This will give us a fair idea how to proceed with our preprocessing.

# In[15]:


import glob
import pandas as pd
import os as os
import matplotlib.pyplot as plt


path =r'Data/russian_tweets/'
allFiles = glob.glob(os.path.join(path, "*.csv"))
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
frame = pd.concat(list_)
#print frame


# In[16]:


print frame.shape


# In[3]:


print frame


# In[4]:


print frame["language"]


# # Language
# 
# We are trying to observe major languages used by Internet Reasearch Agency(IRA) for trolls. Below graph shows that most of trolls were in English but they tweet some trolls in Russian and German as well. German and other languages most probably are choosen becuase of high population in America.

# In[5]:


frame['language'].value_counts().head(3).plot(kind='bar')


# In[6]:


print frame['language'].value_counts().head(10)


# In[7]:


frame_users = frame[['author','language']]


# # Author and Their relation with language
# Most of the authors were bilingiual. Below stats show that authors who posted most tweets were majorly in English but not entirely English. They tweeted in other language as well.

# In[9]:


frame_users['author'].value_counts().head(10).plot(kind='bar')


# In[10]:


print frame_users['author'].value_counts().head(10)


# In[11]:


print frame_users.query('language=="English"')['author'].value_counts().head(10).plot(kind='bar')


# In[12]:


print frame_users.query('language=="English"')['author'].value_counts().head(10)


# In[13]:


print frame['account_category'].value_counts().plot(kind='bar')


# # Category
# Lastly we will observe the tweets categories. These categories gives us a fair idea that a lots of English tweets revoloved around Left , Right or News trolls. Retweeting fake news was a major propaganda among these trolls.

# In[14]:


print frame['account_category'].value_counts()

