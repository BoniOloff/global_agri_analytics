import os
import pandas as pd
import numpy as np
import seaborn as sns

######### DIRECTORY
path = ''
# os.chdir(path)

######### COMMODITY DICTIONARY TABLE
df_item = pd.read_csv(os.path.join(path, 'production_item_hscode.csv'))
df_item = df_item[df_item['Item Group'] != 'Crops Primary']
df_item['HS12 Code'] = df_item['HS12 Code'].astype('str')
df_item['HS12 Code'] = df_item['HS12 Code'].str[:6]
df_item2 = df_item
df_item = df_item.drop(columns=['Item Group', 'Factor', 'Item', 'HS Code', 'HS07 Code', 'CPC Code'])

df_item_desc = pd.read_csv(os.path.join(path, 'production_item_desc.csv'))
df_item_desc['HS12 Code'] = df_item_desc['HS12 Code'].astype('str')
df_item_desc['HS12 Code'] = df_item_desc['HS12 Code'].str[:6]
df_item_desc = df_item_desc.drop(columns=['HS Code', 'HS07 Code', 'CPC Code'])
df_item_desc = df_item_desc[['Item Code', 'Description']]

df_item2 = df_item2[['Item Group', 'Item Code', 'Item']]
df_item2 = df_item2.merge(df_item_desc, on='Item Code', how='left')
df_item2 = df_item2.rename(columns={'Item Group': 'commodity_group',
                         'Item': 'commodity_name',
                         'Item Code': 'commodity_id',
                         'Description': 'commodity_desc'})
df_item2.to_csv('commodity.csv', index=False)
