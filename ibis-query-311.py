"""
Docker image: irose/citywide-civis-lab
Docker image tag: e69270a2a7dc
Civis requires database credentials
"""
import intake_civis

# Get into the postgres catalog
cat = intake_civis.open_postgres_catalog()

# See what's in there - the public schema is where 311 data is
list(cat)

# Save the 311 table as an ibis object
df = cat.public.import311.to_ibis()

# This will show us the SQL query behind it
df

# Subset and select the rows that meet certain condition for requesttype 
street_repair = ['Barricade Removal', 'Bus Pad/Landing', 'Curb Repair', 
                 'Flooding', 'General Street Inspection', 'Guard/Warning Rail Maintenance',  'Gutter Repair',
                 'Land/Mud Slide',  'Pothole - Small Asphalt Repair', 'Resurfacing', 
                 'Sidewalk Repair', 'Street Sweeping']

# Subset by columns
cols = ['srnumber', 'requesttype', 'createddate']

# Ex 1: select rows that meet condition and some columns
street = df[df.requesttype.isin(street_repair)][cols]

# Printing this object will show a preview of the SQL query you want to execute
street

# Ex 2: additionally, subset by date
street = street[street.createddate.cast('date') >= '2018-01-01']

# Execute the query and return a pandas dataframe
new_df = street.execute()