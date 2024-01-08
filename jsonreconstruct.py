import pandas
import folium
import os
import geopy
import json
from folium.plugins import HeatMap
import ast
from branca.colormap import linear

# Read in VIC Data from csv
vicdata = pandas.read_csv("vicdata.csv")

# Objective: Create a geojson object that has multiple properties
# Most importantly the ID or location attribute

jsonfile = []

# Rudimentary checklist
lgalist = vicdata['LGA Label'].unique().tolist()

# Create a function that takes in a number of attributes ns d
for index ,row in vicdata.iterrows():
    json_string = row['geom']
    json_dict = json.loads(json_string)
    json_dict = {'type': json_dict.pop('type'), **json_dict}

    lgacode = row['LGA']
    lganame = row['LGA Label']
    pop = row['POPULATION']
    metro = row['METRO']

    if lganame in lgalist:
        jsonfile.append({
            'type': "Feature",
            'id': lgacode,
            "properties": {
            'State_Label': lganame,
            'Population': pop,
            'Metro': metro
            },
            'geometry': json_dict
            })
        lgalist.remove(lganame)


# Create a dictionary or list as needed
result_dict = {
    "type" : 'FeatureCollection',
    "features": jsonfile}  # Example: Creating a dictionary with a key "data" and a list of JSON objects

# Convert the final dictionary to a JSON string
final_json = json.dumps(result_dict, indent=2)  # Use indent for pretty formatting


# Save to a file if needed
with open('index.json', 'w') as f:
    f.write(final_json)


# with open("index.json" , "w") as json_file:
#     json_file.write(json.dumps(jsonfile))

    