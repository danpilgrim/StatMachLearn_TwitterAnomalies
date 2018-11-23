#!/usr/bin/env python
# coding: utf-8

# # Feature and Time line Analysis
# 
# In this notebook we will observe major trend behaviour in troll tweets. This behaviour along with timeline analysis will help us to retrieve similar data from twitter which is related to election. The main rason for this is because we want to extract tweets which are similar to troll tweets in every aspect of influence. So this analysis will provide us most popular hastags and peak times when trollers were active. We will use this data and extract non-troll tweets from twitter. 

# In[1]:


import glob
import pandas as pd
import os as os
import matplotlib.pyplot as plt


path =r'Data/russian_tweets/'
allFiles = glob.glob(os.path.join(path, "*.csv"))
troll = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
troll = pd.concat(list_)


# In[2]:


print troll.shape


# We will start with removing null content from data. After that we will extract time and date of tweets posted by trolls. Then this time line will be checked against major comapaign and election dates. We will observe how these account's activities changed during these events. We will also observe that even after election how they keep influencing US politics.

# In[3]:


troll.isnull().sum().sort_values(ascending = False)


# In[4]:


print(troll.dtypes)


# In[5]:


troll['publish_date'] = pd.to_datetime(troll['publish_date'])


# In[6]:


start_date_tweet = troll['publish_date'].min()
end_date_tweet = troll['publish_date'].max()
print start_date_tweet,end_date_tweet


# In[7]:


troll['created_str_date'] = pd.to_datetime(troll['publish_date'].dt.date)


# In[8]:


# Count the number of times a date appears in the dataset and convert to dataframe
tweet_trend = pd.DataFrame(troll['created_str_date'].value_counts())

# index is date, columns indicate tweet count on that day
tweet_trend.columns = ['tweet_count']
# sort the dataframe by the dates to have them in order
tweet_trend.sort_index(ascending = True, inplace = True)


# In[9]:


print tweet_trend['tweet_count'].sort_values(ascending=False).head(15)


# In[10]:


plt.style.use('seaborn-darkgrid')
tweet_trend['tweet_count'].plot(linestyle = "-", figsize = (12,8), rot = 45, color = 'k',
                               linewidth = 1)
plt.title('Tweet counts by date', fontsize = 15)
plt.xlabel('Date', fontsize = 13)
plt.ylabel('Tweet Count', fontsize = 13)


# Till now we have observed how these accounts were active till banned. Now we will run this timeline in juxtapose with some hand picked major comapign dates. We can see from below graph that trolls were very active during election debates and in primary nominations as well. This shows us that these accounts were primarily targeted to influence elections.

# In[11]:


dates_list = ['2015-11-27', '2015-07-22', '2016-02-01',
              '2017-08-16', '2017-08-17', '2016-03-11',
              '2016-05-03', '2016-05-26', '2016-06-20', 
              '2016-07-15', '2016-07-21', '2016-08-17',
              '2016-09-26', '2016-10-07', '2016-10-06']

# create a series of these dates.
important_dates = pd.Series(pd.to_datetime(dates_list))

# add columns to identify important events, and mark a 0 or 1.
tweet_trend['Important Events'] = False
tweet_trend.loc[important_dates, 'Important Events'] = True
tweet_trend['values'] = 0
tweet_trend.loc[important_dates, 'values'] = 1


# In[12]:


plt.style.use('seaborn-darkgrid')
tweet_trend['tweet_count'].plot(linestyle = "--", 
                                figsize = (12,8), rot = 45, 
                                color = 'k',
                                label = 'Tweet Count per Day',
                               linewidth = 1)

# plot dots for where values in the tweet_trend df are 1
plt.plot(tweet_trend[tweet_trend['Important Events'] == True].index.values,
         tweet_trend.loc[tweet_trend['Important Events'] == True, 'values'],
         marker = 'o', 
         color = 'r',
         linestyle = 'none',
        label = 'Important Dates in campaign')

# Lets add a 30 day moving average on top to view the trend! Min_periods tells rolling() to
# use 10 points if 30 not available!
plt.plot(tweet_trend['tweet_count'].rolling(window = 30, min_periods = 10).mean(), 
         color = 'r', 
         label = '30 Day Moving Avg # of tweets')
plt.title('Tweet counts by date', fontsize = 15)
plt.xlabel('Date', fontsize = 13)
plt.ylabel('Tweet Count', fontsize = 13)
plt.legend(loc = 'best')


# ## Cleaning & Hashtag Analysis
# Now after having date comparison we will extract some most famous hashtags from tweets, which we will give us an idea how trolls tried to mingle with general public trolls. We will see many similar and popular hashtags among trolls which were famous in elections and are very important issues during complete presidential run. **Like : #BlackLivesMatter**

# In[13]:


troll['content'].head(10)


# In[14]:


troll.dropna(subset = ['content'], inplace = True)
trolls = troll.query('account_category == "RightTroll" |account_category == "LeftTroll" | account_category == "NewsFeed"')
print trolls.shape
import re
def remove_retweet(tweet):
    '''Given a tweet, remove the retweet element from it'''
    text_only = []
    if len(re.findall("^RT.*?:(.*)", tweet)) > 0:
        text_only.append(re.findall("^RT.*?:(.*)", tweet)[0])
    else:
        text_only.append(tweet)
    return text_only[0]

# extract texts and place in a list
text_only = trolls.query('language=="English"')['content'].map(remove_retweet)


# In[15]:


print text_only.shape


# In[16]:


def remove_links(tweet):
    '''Provide a tweet and remove the links from it'''
    text_only = []
    if len(re.findall("(https://[^\s]+)", tweet)) > 0:
        tweet = re.sub("(https://[^\s]+)", "", tweet)
    if len(re.findall("(http://[^\s]+)", tweet)) > 0:
        tweet = re.sub("(http://[^\s]+)", "", tweet)    
    text_only.append(tweet)
    return text_only[0]

text_no_links = text_only.map(remove_links)


# In[17]:


def remove_hashtags(tweet):
    '''Provide a tweet and remove hashtags from it'''
    hashtags_only = []
    if len(re.findall("(#[^#\s]+)", tweet)) > 0:
        tweet = re.sub("(#[^#\s]+)", "", tweet) 
    hashtags_only.append(tweet)
    return hashtags_only[0]

text_all_removed = text_no_links.map(remove_hashtags)


# In[18]:


def remove_extraneous(tweet):
    '''Given a text, remove unnecessary characters from the beginning and the end'''
    tweet = tweet.rstrip()
    tweet = tweet.lstrip()
    tweet = tweet.rstrip(")")
    tweet = tweet.lstrip("(")
    tweet = re.sub("\.", "", tweet)
    return tweet

text_clean = text_all_removed.map(remove_extraneous)


# In[21]:


def extract_hashtags(tweet):
    '''Provide a tweet and extract hashtags from it'''
    hashtags_only = []
    if len(re.findall("(#[^#\s]+)", tweet)) > 0:
        hashtags_only.append(re.findall("(#[^#\s]+)", tweet))
    else:
        hashtags_only.append(["0"])
    return hashtags_only[0]

# make a new column to store the extracted hashtags and view them!
tweet_hashtags = troll.query('account_category == "RightTroll" |account_category == "LeftTroll" | account_category == "NewsFeed"')['content'].map(extract_hashtags)
#troll['tweet_hashtags'].head(10)


# In[22]:


print tweet_hashtags


# In[23]:


# create a list of all hashtags
all_hashtags = tweet_hashtags

# Next we observe that our all_hashtags is a list of lists...lets change that
cleaned_hashtags = []
for i in all_hashtags:
    for j in i:
            cleaned_hashtags.append(j)

# Convert cleaned_hashtags to a series and count the most frequent occuring
cleaned_hashtag_series = pd.Series(cleaned_hashtags)
hashtag_counts = cleaned_hashtag_series.value_counts()


# In[24]:


hashes = cleaned_hashtag_series.values
hashes = hashes.tolist()
hashes= filter(lambda a: a != '0', hashes)


# In[25]:


from collections import Counter
print Counter(hashes)


# In[26]:


i=0
value1=[]
value2=[]
for x in Counter(hashes).most_common(100):
    value1.append(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x[0]).split()))
    value2.append(x[1])
print value1
print value2
df = pd.DataFrame({'hashtag':value1,'count':value2})


# In[27]:


print df.head(10).plot(x='hashtag',y='count',kind='barh')


# In[32]:


print df['hashtag'].head(50)


# In[ ]:


d = {}
for a, x in df.values:
    d[x]=a
print d


# In[ ]:


import matplotlib.pyplot as plt
from wordcloud import WordCloud

wordcloud = WordCloud(width= 1600, height = 800, 
                      relative_scaling = 0.6, 
                      colormap = "Blues",
                     max_words = 100).generate_from_frequencies(frequencies=d)
plt.figure(figsize=(20,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()


# **From above word cloud we can easily observe that trolls tried to behave as news. This may be because of the reason that news is one of the most popular hashtag during election and can easily show troll's tweets among others.**
# 
# Now as we have complete timeline information and major hashtags, we can easily extract tweets from twitter based on this information.
