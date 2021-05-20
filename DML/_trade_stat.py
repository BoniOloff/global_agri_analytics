import os
import pandas as pd
import numpy as np
import seaborn as sns

######### DIRECTORY
path = ''
# os.chdir(path)


# df_item = df_item_desc.merge(df_item[['Item Group Code', 'Item Group', 'Item Code', 'Item']], on=['Item Code', 'Item'], how='left')
df_item = df_item.dropna()
df_item = df_item.groupby('Item Code').first().reset_index()

# df_item_desc['HS12 Code'] = [sub.split(",") for sub in df_item_desc['HS12 Code']]
# df_item_desc = df_item_desc.explode('HS12 Code')


######### TARIFF TABLE
df_tariff_bound_0708 = pd.read_csv(os.path.join(path, 'tariff_bound_0708.csv'))
df_tariff_bound_0910 = pd.read_csv(os.path.join(path, 'tariff_bound_0910.csv'))
df_tariff_bound_1112 = pd.read_csv(os.path.join(path, 'tariff_bound_1112.csv'))
df_tariff_bound_40 = pd.read_csv(os.path.join(path, 'tariff_bound_40.csv'))


# concat dan convert format for all tariff tables
tariffs = [df_tariff_bound_0708, df_tariff_bound_0910, df_tariff_bound_1112, df_tariff_bound_40]
df_tariff = pd.concat(tariffs)
df_tariff = df_tariff[['Reporter', 'Product', 'AVDuty average', 'AVDuty minimum', 'AVDuty maximum', 'Percent duty free', 'ODC AVDuty average']]
df_tariff = df_tariff.dropna(subset=['Product'])
df_tariff['Product'] = df_tariff['Product'].astype('int')
df_tariff['Product'] = df_tariff['Product'].astype('str')
df_tariff = df_tariff.merge(df_countrygroup, left_on=['Reporter'], right_on=['Area'], how='inner')
df_tariff = df_tariff.drop(columns=['Reporter', 'Region Code', 'Region', 'Area'])


######### TRADE TABLE
# df_trade = pd.read_csv(os.path.join(path, 'trade_compressed.csv'))
# commodities = df_item_desc['Item Code'].unique()
# df_trade = df[df['Item Code'].isin(commodities)]
# df_trade = pd.read_csv(os.path.join(path, 'trade.csv'))
# df_trade = df_trade.drop(columns=['Unnamed: 0', 'Item', 'Element', 'Unit'])
# df_trade.to_csv('trade.csv')
df_trade = pd.read_csv(os.path.join(path, 'trade.csv'))
df_trade = df_trade.merge(df_item[['Item Code', 'HS12 Code']], on=['Item Code'], how='inner')
df_trade = df_trade.drop(columns=['Unnamed: 0'])
df_trade['HS12 Code'] = df_trade['HS12 Code'].astype('int')
df_trade['HS12 Code'] = df_trade['HS12 Code'].astype('str')
df_trade_wide = df_trade.pivot_table(index=['Reporter Country Code', 'Partner Country Code', 'Item Code', 'HS12 Code', 'Year'], columns=['Element Code'], values='Value').reset_index()
df_trade_wide = df_trade_wide.merge(df_tariff, left_on=['Partner Country Code', 'HS12 Code'], right_on=['Area Code', 'Product'], how='inner')
df_trade_wide = df_trade_wide.rename(columns={'Reporter Country Code': 'from_country_id',
                              'Partner Country Code': 'to_country_id',
                              'Item Code': 'commodity_id',
                              'Year': 'year',
                              5610: 'import_quantity',
                              5622: 'import_value',
                              5910: 'export_quantity',
                              5922: 'export_value',
                              'AVDuty average': 'tariff_avg',
                              'AVDuty minimum': 'tariff_min',
                              'AVDuty maximum': 'tariff_max',
                              'Percent duty free': 'percent_dutyfree',
                              'ODC AVDuty average': 'tariff_others'})

df_trade_wide = df_trade_wide.drop(columns=['HS12 Code', 'Product', 'Area Code'])
df_trade_wide = df_trade_wide.reset_index()
df_trade_wide = df_trade_wide.rename(columns={'index':'trade_id'})
df_trade_wide.to_csv('trade_stat.csv', index=False)
