import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# print(os.listdir('/Users/Ashley/Desktop/'))
file_name ='/Users/Ashley/Desktop/decimated.csv'
df = pd.read_csv(file_name)
out = (df.loc[df['TRACK_ID'] == '10'])

df1 = out.iloc[:, 4:6]
to_plot = np.asarray(df1)
plt.plot(to_plot[:,0], to_plot[:,1],'r-')

file_name ='/Users/Ashley/Desktop/fitted.csv'
df = pd.read_csv(file_name)
out = (df.loc[df['TRACK_ID'] == '2'])

df1 = out.iloc[:, 4:6]
to_plot = np.asarray(df1)
plt.scatter(to_plot[:,0], to_plot[:,1])



plt.show()
