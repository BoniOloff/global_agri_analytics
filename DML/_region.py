import os
import pandas as pd
import numpy as np
import seaborn as sns

######### DIRECTORY
path = ''
# os.chdir(path)

######### COUNTRY & COUNTRY GROUP DICSTIONARY
df_countrygroup = pd.read_csv(os.path.join(path, 'countrygroup.csv'))
df_countrygroup['Country Group'].value_counts()
df_countrygroup = df_countrygroup.drop(columns=['M49 Code', 'ISO2 Code', 'ISO3 Code'], axis=1)
df_countrygroup.columns = ['Region Code', 'Region', 'Area Code', 'Area']
df_countrygroup = df_countrygroup[(df_countrygroup['Region Code']%100 == 0) & (df_countrygroup['Region Code']%5000 != 0)]


######### REGION TABLE
df_region = df_countrygroup[['Region Code', 'Region']]
df_region.columns = ['region_id', 'region_name']
df_region.to_csv('region.csv', index=False)
