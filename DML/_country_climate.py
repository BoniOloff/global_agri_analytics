import pandas as pd
import numpy as np
import os
path = r"C:\Users\bonio\Downloads\group4\Clean table"

data = pd.read_csv('temperature.csv')

data = data[data['Months Code'] == 7020]

data = data[['Area Code', 'Element', 'Year', 'Value']]
data = data.pivot_table(index=['Area Code', 'Year'], columns='Element', values='Value').reset_index()
country_climate = data.rename(columns={'Area Code':'country_id', 'Year': 'year', 'Standard Deviation':'temperature_stdev', 'Temperature change': 'temperature_chg'})
country_climate = country_climate.rename_axis('', axis=1)
country_climate = country_climate.reset_index()
country_climate = country_climate.rename(columns={'index':'climate_id'})

coun = pd.read_csv(os.path.join(path, 'country.csv'))
country_climate = country_climate.merge(coun[['country_id']], on='country_id', how="inner")

country_climate.to_csv('country_climate.csv', index=False)
