import pandas as pd
from datetime import datetime

# Read the CSV file
df = pd.read_csv('clean_sat_data.csv')

# Function to standardize date format
def standardize_date(date_str):
    # Try parsing with two different formats
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return date_str  # Return original if no format matches

# Apply the function to the date column
# df['LaunchDate'] = df['LaunchDate'].apply(standardize_date)

# Replace 'LEo' with 'LEO' in the 'OrbitClass' column
df['OrbitClass'] = df['OrbitClass'].replace({'LEo': 'LEO'})

# Save the modified DataFrame back to a CSV file
df.to_csv('clean_sat_data2.csv', index=False)