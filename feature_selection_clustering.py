# Imports
import pandas as pd

# Read in the data
data = pd.read_csv("data/factbook_clean.csv")

# Features to use in clustering analysis
features = [
    'name',
    'geography.map_references',
    'people.population_growth_rate.growth_rate',
    'people.birth_rate.births_per_1000_population',
    'people.death_rate.deaths_per_1000_population',
    'people.maternal_mortality_rate.deaths_per_100k_live_births',
    'infant_mortality_rate.deaths_per_1000_live_births',
    'people.life_expectancy_at_birth.total_population.value',
    'people.total_fertility_rate.children_born_per_woman',
    'people.hiv_aids.people_living_with_hiv_aids.total',
    'people.hiv_aids.deaths.total',
    'literacy.total_population(%)',
    'gdp_per_capita.purchasing_power_parity(USD)',
    'unemployment_rate(%)',
    'inflation_rate(%)',
    'people.adult_obesity.percent_of_adults',
    'population_below_poverty_line(%)',
]

# New DataFrame with only selected features
data_feats = data[features]

# Column names simplified
col_names = [
    'country',
    'region',
    'pop_growth',
    'birth_rate',
    'death_rate',
    'maternal_mort_rate',
    'infant_mort_rate',
    'life_expectancy',
    'total_fert_rate',
    'living_with_hiv',
    'hiv_deaths',
    'literacy',
    'gdp_per_capita',
    'unemployment',
    'inflation',
    'adult_obesity',
    'pop_below_poverty',    
]

# Apply simple columns names
data_feats.columns = col_names

# Create final copy for export
factbook_cluster = data_feats.copy()

# Export to CSV
factbook_cluster.to_csv('data/factbook_cluster.csv', index=False)
