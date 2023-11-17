import pandas as pd

df = pd.read_csv('Task-2-data.csv')

df.replace(to_replace="/nanh", value="/0h", inplace=True)

df.replace(to_replace="Not Available", value="http://punch.cool", inplace=True)
print(df.head())

df.to_csv('Eze-Onyekachukwu-task2-data.csv', index=False)