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
print frame.shape
df.hist(column="language")
plt.show()