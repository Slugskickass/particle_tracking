import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# print(os.listdir('/Users/Ashley/Desktop/NDR_tracker/'))
file_name ='/Users/Ashley/Desktop/NDR_tracker/Decimated.csv'
df = pd.read_csv(file_name)
out = (df.loc[df['TRACK_ID'] == '1'])
df1 = out.iloc[:, 4:6]
to_plot = np.asarray(df1)
plt.scatter(to_plot[:, 0], to_plot[:, 1], label='Decimated')
hold = to_plot[:, 0]


file_name ='/Users/Ashley/Desktop/NDR_tracker/Decimated_fitted.csv'
df = pd.read_csv(file_name)
print(np.shape(df))
out = (df.loc[df['TRACK_ID'] == '6'])
df1 = out.iloc[:, 4:6]
to_plot = np.asarray(df1)
plt.scatter(to_plot[:, 0], to_plot[:, 1], label='Decimated Fitted')

file_name ='/Users/Ashley/Desktop/NDR_tracker/slidding.csv'
df = pd.read_csv(file_name)
print(np.shape(df))
out = (df.loc[df['TRACK_ID'] == '6'])
df1 = out.iloc[:, 4:6]
to_plot = np.asarray(df1)
plt.plot(to_plot[:, 0], to_plot[:, 1], label='Slidding')

file_name ='/Users/Ashley/Desktop/NDR_tracker/slidding_fitted.csv'
df = pd.read_csv(file_name)
print(np.shape(df))
out = (df.loc[df['TRACK_ID'] == '1'])
df1 = out.iloc[:, 4:6]
to_plot = np.asarray(df1)
plt.plot(to_plot[:, 0], to_plot[:, 1], label='Slidding Fitted')

#plt.axis([291, 296, 64, 71])
plt.axis([270, 296, 55, 75])
plt.legend()
plt.savefig("plot2.pdf", dpi=600)
plt.show()
