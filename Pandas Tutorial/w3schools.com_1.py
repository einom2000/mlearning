import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data_1.csv')
print(df.head())
print(df.corr())

df.plot(kind='scatter', x='Duration', y='Calories')
plt.show()

df["Duration"].plot(kind = 'hist')
plt.show()

