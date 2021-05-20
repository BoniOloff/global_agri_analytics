import pandas as pd
import numpy as np
import os

path = ''
######### STOCK TABLE
df_stock = pd.read_csv(os.path.join(path, 'stock.csv'), encoding='ISO-8859-1')
food_balance = ['Opening stocks', 'Loss', 'Processed']
df_stock = df_stock[df_stock['Element'].isin(food_balance)]
df_stock = df_stock.pivot_table(index=['Area Code', 'Item Code', 'Year'], columns=['Element'], values='Value').reset_index()
df_stock = df_stock.rename(columns={'Area Code': 'country_id',
                         'Item Code': 'commodity_id',
                         'Year': 'year',
                         'Loss': 'loss',
                         'Opening stocks': 'inventory',
                         'Processed': 'processed'})

path = r'C:\Users\bonio\Downloads\group4\Clean table'
commo = pd.read_csv(os.path.join(path, 'commodity.csv'))
df_stock = df_stock.merge(commo[['commodity_id']], on='commodity_id', how="inner")

df_stock = df_stock.reset_index()
df_stock = df_stock.rename(columns={'index':'stock_id'})
df_stock = df_stock.rename_axis("", axis=1)


df_stock.to_csv('stock_stat.csv', index=False)
