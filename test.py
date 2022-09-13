import pandas as pd




print('------- SOURCE 1 -------')
df1 = pd.DataFrame({'City': ['New York', 'Chicago', 'Tokyo', 'Paris','New Delhi'],
                     'Temp': [59, 29, 73, 56,48]})
print(df1)
print('------- SOURCE 2 -------')
df2 = pd.DataFrame({'City': ['London', 'New York', 'Tokyo', 'New Delhi','Paris'],
                     'Temp': [55, 55, 73, 85,56]})
print(df2)
# print('------- MERGE inner ----')
# inner = df1.merge(df2, how='inner', indicator=False)
# print(inner)
# print('------- MERGE outer ----')
# outer = df1.merge(df2, how='outer', indicator=True)
# print(outer)
# print('------- MERGE on City ----')
city_merge = df1.merge(df2, on='City', suffixes=['_source','_new'])
print(city_merge)