# Imports
from factbook_cols import relevant_factbook_cols as rfc

import pandas as pd
import numpy as np

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
final_df = new_df.filter(rfc)

