import pandas as pd
import numpy as np

data = pd.read_csv('countrygroup.csv')

data = data[['Country Code', 'Country', 'Country Group Code']]
data.columns = ['country_id', 'country_name', 'region_id']
data = data[data['region_id'].isin([5100, 5200, 5300, 5400, 5500, 5600])]
country = data
country[country.country_name == 'United States of America']['country_name'] = 'United States'
country[country.country_name == 'United States']


country = country.replace({231:231, 'United States of America':'United States', 5200: 5200})

country.to_csv('country.csv', index=False)
