import datetime
import pandas as pd


symbols_data = [
        {
            "Symbol": "A",
            "Name": "Agilent Technologies Inc",
            "ListedDt": datetime.datetime(2005, 1, 3).isoformat(),
            "LastDt": datetime.datetime(2022, 9, 6).isoformat(),
            "Status": "Active",
        },
        {
            "Symbol": "AA",
            "Name": "Alcoa Corporation",
            "ListedDt": datetime.datetime(2016, 10, 18).isoformat(),
            "LastDt": datetime.datetime(2022, 9, 6).isoformat(),
            "Status": "Active",
        },
        {
            "Symbol": "ZGNX",
            "Name": "Zogenix",
            "ListedDt": datetime.datetime(2010, 11, 23).isoformat(),
            "LastDt": datetime.datetime(2022, 3, 4).isoformat(),
            "Status": "Active",
        }
    ]

update_data = [
        {
            "Symbol": "AA",
            "Name": "Updated Alcoa Corporation",
            "ListedDt": datetime.datetime(2022, 10, 18).isoformat(),
            "LastDt": datetime.datetime(2022, 9, 6).isoformat(),
            "Status": "Active",
        },
        {
            "Symbol": "ZGNX",
            "Name": "Updated Zogenix",
            "ListedDt": datetime.datetime(2012, 11, 23).isoformat(),
            "LastDt": datetime.datetime(2022, 3, 4).isoformat(),
            "Status": "Active",
        }
    ]


def city_data():   
    print('------- SOURCE 1 -------')
    df1 = pd.DataFrame({'City': ['New York', 'Chicago', 'Tokyo', 'Paris','New Delhi'],
                         'Temp': [59, 29, 73, 56,48]})
    print(df1)
    print('------- SOURCE 2 -------')
    df2 = pd.DataFrame({'City': ['London', 'New York', 'Tokyo', 'New Delhi','Paris'],
                         'Temp': [55, 55, 73, 85,56]})
    return df1, df2


source = pd.DataFrame(symbols_data)
updated = pd.DataFrame(update_data)
print(source)
print(updated)
print('Left join')
print(pd.merge(source, updated, on='Symbol', how='left', suffixes=['_s','_u']))
print('Right join')
print(pd.merge(source, updated, on='Symbol', how='right', suffixes=['_s','_u']))












# print('------- MERGE inner ----')
# inner = df1.merge(df2, how='inner', indicator=False)
# print(inner)
# print('------- MERGE outer ----')
# outer = df1.merge(df2, how='outer', indicator=True)
# print(outer)
# print('------- MERGE on City ----')
#city_merge = df1.merge(df2, on='City', suffixes=['_source','_new'])
#print(city_merge)