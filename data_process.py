import pandas as pd

# Load the datasets
sat_data = pd.read_csv('aggregated_sat_data.csv')
country_data = pd.read_csv('country_long_lat.csv')

# Function to check and add Longitude, Latitude based on Country, Alpha-2 code, or Alpha-3 code match
def get_coordinates(row, country_data):
    match = country_data[
        (country_data['Country'] == row['Country']) | 
        (country_data['Code1'] == row['Country']) | 
        (country_data['Code2'] == row['Country'])
    ]
    if not match.empty:
        return pd.Series([match.iloc[0]['Longitude'], match.iloc[0]['Latitude']])
    else:
        return pd.Series([None, None])

# Apply the function to add Longitude, Latitude to sat_data
sat_data[['Longitude', 'Latitude']] = sat_data.apply(get_coordinates, country_data=country_data, axis=1)

# Separate the rows where Longitude and Latitude are missing (i.e., no match found)
unmatched_data = sat_data[sat_data['Longitude'].isna() & sat_data['Latitude'].isna()]

# For unmatched rows, rename 'Country' to 'Countries/Organisations' and keep only 'Country' and 'Total_Satellites'
unmatched_data = unmatched_data[['Country', 'Total_Satellites', 'Total_Mass']].rename(columns={'Country': 'Countries/Organisations'})

# Save the unmatched data to a new file
unmatched_data.to_csv('unmatched_countries_organisations.csv', index=False)

# Remove the unmatched rows from the original sat_data
matched_data = sat_data.dropna(subset=['Longitude', 'Latitude'])

# Save the matched data to a new file
matched_data.to_csv('merged_sat_data.csv', index=False)

print("Matched data saved as 'merged_sat_data.csv' and unmatched countries/organisations saved as 'unmatched_countries_organisations.csv'.")
