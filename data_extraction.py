# Imports
from factbook_cols import relevant_factbook_cols as rfc

import pandas as pd

# Read in the data
df = pd.read_json("data/factbook.json")

# Check the index
df.index

# Create country list
country_list = df.index[1:-4]

# Check columns
df.columns

# Flatten the json file
flattened_df = pd.json_normalize(df['countries']['world']['data'])

# Create empty DataFrame
new_df = pd.DataFrame(columns = flattened_df.columns)

# Loop over all countries and add them to the empty DataFrame
for country in country_list:
    temp = pd.json_normalize(df['countries'][country]['data'])
    new_df = pd.concat([new_df, temp], ignore_index=True)
    
# Filter out only relevant columns
df_filtered = new_df.filter(rfc)

# Renaming columns to include measurement units
df_filtered.rename(columns={
    'geography.area.total.value':'area.total.sqkm',
    'people.infant_mortality_rate.total.value':'infant_mortality_rate.deaths_per_1000_live_births',
    'people.literacy.total_population.value':'literacy.total_population(%)',
    'economy.labor_force.by_occupation.occupation.agriculture.value':'labor_force.agriculture(%)',
    'economy.labor_force.by_occupation.occupation.industry.value':'labor_force.industry(%)',
    'economy.labor_force.by_occupation.occupation.services.value':'labor_force.services(%)',
    'economy.budget.revenues.value':'economy.revenues(USD)',
    'economy.budget.expenditures.value':'economy.expenditures(USD)',
    'geography.land_use.by_sector.agricultural_land_total.value':'land_use.agricultural(%)',
    'geography.land_use.by_sector.arable_land.value':'land_use.arable_land(%)',
    'geography.land_use.by_sector.permanent_crops.value':'land_use.permanent_crops(%)',
    'geography.land_use.by_sector.permanent_pasture.value':'land_use.permanent_pasture(%)',
    'geography.land_use.by_sector.forest.value':'land_use.forest(%)',
    'geography.land_use.by_sector.other.value':'land_use.other(%)',
    'economy.population_below_poverty_line.value':'population_below_poverty_line(%)',
    'economy.gdp.purchasing_power_parity.annual_values':'gdp.purchasing_power_parity(USD)',
    'economy.gdp.real_growth_rate.annual_values':'gdp.real_growth_rate(%)',
    'economy.gdp.per_capita_purchasing_power_parity.annual_values':'gdp_per_capita.purchasing_power_parity(USD)',
    'economy.gross_national_saving.annual_values':'gross_national_saving(%_of_gdp)',
    'economy.unemployment_rate.annual_values':'unemployment_rate(%)',
    'economy.public_debt.annual_values':'public_debt(%_of_gdp)',
    'economy.inflation_rate.annual_values':'inflation_rate(%)',
    'economy.current_account_balance.annual_values':'current_account_balance(USD)',
}, inplace=True)

# Drop redundant columns with units
df_filtered = df_filtered.drop(columns=[
    'geography.area.total.units',
    'people.infant_mortality_rate.total.units',
    'people.literacy.total_population.units',
    'economy.labor_force.by_occupation.occupation.agriculture.units',
    'economy.labor_force.by_occupation.occupation.industry.units',
    'economy.labor_force.by_occupation.occupation.services.units',
    'economy.budget.revenues.units',
    'economy.budget.expenditures.units',
    'geography.land_use.by_sector.agricultural_land_total.units',
    'geography.land_use.by_sector.arable_land.units',
    'geography.land_use.by_sector.permanent_crops.units',
    'geography.land_use.by_sector.permanent_pasture.units',
    'geography.land_use.by_sector.forest.units',
    'geography.land_use.by_sector.other.units',
    'economy.population_below_poverty_line.units',
])

# Extract values from nested dicts
def extract_values(x):
    return x[0]['value'] if isinstance(x, list) else x


# Create list of all columns with nested dicts
cols_with_nested_dicts = [
    'gdp.purchasing_power_parity(USD)',
    'gdp.real_growth_rate(%)',
    'gdp_per_capita.purchasing_power_parity(USD)',
    'gross_national_saving(%_of_gdp)',
    'unemployment_rate(%)',
    'public_debt(%_of_gdp)',
    'inflation_rate(%)',
    'current_account_balance(USD)',
]

# Apply function to all columns with nested dicts
for col in cols_with_nested_dicts:
    df_filtered[col] = df_filtered[col].apply(extract_values)


# Create copy for export
df_final = df_filtered.copy()

# Export to CSV
df_final.to_csv('data/factbook_clean.csv')
