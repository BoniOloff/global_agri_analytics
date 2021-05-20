import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sqlalchemy as db


# load data
path = ''
# os.chdir(path)

df_production = pd.read_csv(os.path.join(path, 'production.csv'), encoding='ISO-8859-1')

data = df_production[['Area Code', 'Item Code', 'Element', 'Year', 'Value']]
data = data.pivot_table(index=['Area Code', 'Item Code', 'Year'], columns='Element', values='Value').reset_index()
data.columns = ['country_id', 'commodity_id', 'year', 'area_harvested', 'production_value', 'yield']
production_stat = data

path = r'C:\Users\bonio\Downloads\group4\Clean table'
commo = pd.read_csv(os.path.join(path, 'commodity.csv'))
production_stat = production_stat.merge(commo[['commodity_id']], on='commodity_id', how="inner")

path = r'C:\Users\bonio\Downloads\group4\Clean table'
country = pd.read_csv(os.path.join(path, 'country.csv'))
production_stat = production_stat.merge(country[['country_id']], on='country_id', how="inner")

production_stat = production_stat.reset_index()
production_stat = production_stat.rename(columns={'index': 'production_id'})

production_stat.to_csv('production_stat.csv', index=False)
