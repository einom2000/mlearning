import pandas as pd

mydataset = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}

myvar = pd.DataFrame(mydataset)
print(myvar)

a = [1, 7, 2]
myvar = pd.Series(a)
print(myvar)

print(myvar[0])

myvar = pd.Series(a, index = ["x", "y", "z"])
print(myvar)

calories = {"day1": 420, "day2": 380, "day3": 390}
myvar = pd.Series(calories)
print(myvar)

import pandas as pd

calories = {"day1": 420, "day2": 380, "day3": 390}
myvar = pd.Series(calories, index = ["day1", "day2"])
print(myvar)


data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}
myvar = pd.DataFrame(data)
print(myvar)

data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}
#load data into a DataFrame object:
df = pd.DataFrame(data)
print(df)
print(df.loc[0])

print(df.loc[[0, 1]])

df = pd.DataFrame(data, index = ["day1", "day2", "day3"])
print(df)
print(df.loc["day2"])

df = pd.read_csv('data.csv')
print(df)
# print(df.to_string())

df = pd.read_json('data.js')
# print(df.to_string())
print(df.head(10))

data = {
  "Duration":{
    "0":60,
    "1":60,
    "2":60,
    "3":45,
    "4":45,
    "5":60
  },
  "Pulse":{
    "0":110,
    "1":117,
    "2":103,
    "3":109,
    "4":117,
    "5":102
  },
  "Maxpulse":{
    "0":130,
    "1":145,
    "2":135,
    "3":175,
    "4":148,
    "5":127
  },
  "Calories":{
    "0":409,
    "1":479,
    "2":340,
    "3":282,
    "4":406,
    "5":300
  }
}

df = pd.DataFrame(data)

print(df)
print(df.tail())
print(df.info())


df = pd.read_csv('dirtydata.csv')
new_df = df.dropna()
print(new_df.to_string())

df = pd.read_csv('dirtydata.csv')
# df.fillna(130, inplace = True)
df["Calories"].fillna(130, inplace = True)
print(df.to_string())

df = pd.read_csv('dirtydata.csv')
# x = df["Calories"].mode()[0] mean() median()
df['Date'] = pd.to_datetime(df['Date'])
df.dropna(subset=['Date'], inplace = True)
df.loc[7, "Duration"] = 99
for x in df.index:
  if df.loc[x, "Duration"] > 90:
    df.loc[x, "Duration"] = 60
for x in df.index:
  if df.loc[x, "Duration"] > 120:
    df.drop(x, inplace = True)
df["Calories"].fillna(999.0, inplace=True)
print(df.duplicated())
df.drop_duplicates(inplace=True)
print(df.to_string())


