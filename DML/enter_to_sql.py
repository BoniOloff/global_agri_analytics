import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sqlalchemy as db

path = 'Clean table'
os.chdir(path)

engine = db.create_engine('mysql://root:password@localhost:3306/agri')
connection = engine.connect()

commodity = pd.read_csv('commodity.csv').groupby('commodity_id').first().reset_index()
country_climate = pd.read_csv('country_climate.csv')
country_stat = pd.read_csv('country_stat.csv')
country = pd.read_csv('country.csv')
production_stat = pd.read_csv('production_stat.csv')
region = pd.read_csv('region.csv').groupby('region_id').first().reset_index()
stock_stat = pd.read_csv('stock_stat.csv')
trade_stat = pd.read_csv('trade_stat.csv')

# region OK
region.to_sql('region', con=engine, if_exists='append', index=False)
# country OK
country.to_sql('country', con=engine, if_exists='append', index=False)
# commodity OK
commodity.to_sql('commodity', con=engine, if_exists='append', index=False)
# country_climate OK
country_climate.to_sql('country_climate', con=engine, if_exists='append', index=False)
# country_stat
country_stat.to_sql('country_stat', con=engine, if_exists='replace', index=False)
# production_stat
production_stat.to_sql('production_stat', con=engine, if_exists='append', index=False)
# stock_stat
stock_stat.to_sql('stock_stat', con=engine, if_exists='append', index=False)
# trade_stat
trade_stat.to_sql('trade_stat', con=engine, if_exists='append', index=False)
