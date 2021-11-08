# Hydrographic soundings files are categorized. File statistics (counts and sizes) are provided in terms of these categories. Queries and orders can filter on these categories, giving some degree of control over the content of an order. The most basic query provided for sounding datasets is the ability to get a list of these categories. To obtain a list of all file categories issue a GET request having the following URL pattern:

# URL: https://www.ngdc.noaa.gov/next-web/docs/guide/catalog.html

# https://www.ngdc.noaa.gov/next-catalogs/rest/sounding/catalog/survey?geometry=-71,42,-69,44
# https://www.ngdc.noaa.gov/next-catalogs/rest/sounding/catalog/survey?surveys=H09010

# Courses:
# https://www.w3schools.com/python/python_lists.asp
# https://www.w3schools.com/python/python_dictionaries.asp

# Import libraries
import requests
import json
import psycopg2

# Function to get survey polygon
def get_survey_polygon(survey_name) :

    # Build URL
    url = 'https://www.ngdc.noaa.gov/next-catalogs/rest/sounding/catalog/survey?surveys=' + str(survey_name)

    # Execute HTTP request
    response = requests.get(url)

    # Get result
    if response.status_code == 200 :
        print ('Request OK')
        # print(json.dumps(response.json(), indent=8, sort_keys=True))
        # Get geometry from JSON
        geom_wkt = response.json()['items'][0]['geometry']
        print(geom_wkt)
        return geom_wkt
    else :
        print ('Request failed with :' + str(response.status_code))

# Function to update survey boundary
def update_survey_boundary(survey_name, boundary_wkt):

    # Open connection
    db_connection = psycopg2.connect(host="localhost", port ="5432", database="engineer", user="postgres", password="postgres")
    cur = db_connection.cursor()

    # Execute update
    sql = 'update survey set survey_geom = ST_GeomFromText(%s,4326) where survey_name = %s'
    cur.execute(sql,(boundary_wkt,survey_name))

    # Sla op
    db_connection.commit()

    # Close database
    db_connection.close()

# Run function
geom_wkt_uit = get_survey_polygon('H09010')
update_survey_boundary('H09010', geom_wkt_uit)
print('Survey geometry updated')

