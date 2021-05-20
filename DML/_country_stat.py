import pandas as pd
import numpy as np
import copy

# Clean employment data
emp = pd.read_csv("agri_employment.csv", skiprows=3)

emp.set_index('Country Name', inplace=True)
emp = emp.iloc[:, 34:]
emp = emp.iloc[:,:-2]
emp_long = emp.reset_index().melt(id_vars='Country Name', var_name='Year', value_name='agriculture_employment')
emp_long['Year'] = emp_long['Year'].astype('int')

# Clean logistic data
log_cols = {'Country': 'country', 'score.1': 'logistics_customs', 'score.2': 'logistics_infrastructure',
            'score.3': 'logistics_shipment', 'score.4': 'logistics_competence', 'score.5': 'logistics_tracking',
            'score.6': 'logistics_timeliness'}

def get_logdata(year):
    log = pd.read_excel('logistics.xlsx', header=2, sheet_name=year)
    log = log[['Country', 'score.1', 'score.2', 'score.3', 'score.4', 'score.5', 'score.6']]
    log = log.rename(columns=log_cols)
    log['year'] = year
    return log

log_2010 = get_logdata('2010')
log_2012 = get_logdata('2012')
log_2014 = get_logdata('2014')
log_2016 = get_logdata('2016')
log_2018 = get_logdata('2018')

log = copy.deepcopy(log_2010)
log = log.append(log_2012)
log = log.append(log_2014)
log = log.append(log_2016)
log = log.append(log_2018)
log['year'] = log['year'].astype('int')

# Clean income group
data = pd.read_excel('OGHIST.xls', sheet_name='Country Analytical History', skiprows=5)
data = copy.deepcopy(data.iloc[5:,:])
data = data.rename(columns={'Unnamed: 0': 'country_code', 'Data for calendar year :':'country'})
data = data.drop(columns='country_code')
data = data.iloc[:-11,:]
income_group = data.melt(id_vars='country', var_name='Year', value_name='income_group')
income_group['Year'] = income_group['Year'].astype('int')

# Clean population
data = pd.read_csv('population.csv')
data = data[data['Element'].isin(['Urban population', 'Rural population'])]
data = data[['Area', 'Element', 'Year', 'Value']]
data = pd.pivot_table(data, index=['Area', 'Year'], columns='Element', values='Value').reset_index()
population = data.rename(columns={'Rural population': 'population_rural', 'Urban population':'population_urban'})
population['Year'] = population['Year'].astype('int')
population['Area'].replace(['United States of America'], 'United States', regex=True, inplace=True)

# Clean GDP Agri database
data = pd.read_csv('data_gdp_agri.csv', skiprows=4)
data = data.drop(['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 65', '2020'], axis=1)
data = data.melt(id_vars='Country Name', var_name='Year', value_name='gdp_agri')
gdp_agri = data
gdp_agri['Year'] = gdp_agri['Year'].astype('int')

# Clean GDP database
data = pd.read_csv('data_gdp.csv', skiprows=4)
data = data.drop(['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 65', '2020'], axis=1)
data = data.melt(id_vars='Country Name', var_name='Year', value_name='gdp')
gdp = data
gdp['Year'] = gdp['Year'].astype('int')

# Add employment and logistics
comb = log.merge(emp_long, right_on=['Country Name', 'Year'], left_on=['country', 'year'], how='left')
comb = comb.drop(columns=['Country Name', 'Year'])

# Add income_group
comb = comb.merge(income_group, left_on=['country', 'year'], right_on=['country', 'Year'], how='left')
comb = comb.drop(columns=['Year'])

# Add population
comb = comb.merge(population, left_on=['country', 'year'], right_on=['Area', 'Year'], how='left')
comb = comb.drop(columns=['Area', 'Year'])

# Add gdp agri
comb = comb.merge(gdp_agri, left_on=['country', 'year'], right_on=['Country Name', 'Year'], how='left')
comb = comb.drop(columns=['Country Name', 'Year'])

# Add gdp
comb = comb.merge(gdp, left_on=['country', 'year'], right_on=['Country Name', 'Year'], how='left')
comb = comb.drop(columns=['Country Name', 'Year'])


# Add country id
count = pd.read_csv('country.csv')
comb = comb.merge(count, left_on='country', right_on='country_name')
comb = comb.drop(['country', 'region_id', 'country_name'], axis=1)
comb = comb.reset_index()
comb = comb.rename(columns={'index': 'country_stat_id'})
comb.to_csv('country_stat.csv', index=False)
