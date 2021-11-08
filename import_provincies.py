# Import bibliotheken
import os, sys
import psycopg2

# Import ogr to read shapefile
from osgeo import ogr

# Get driver for file type (list of codes: http://www.gdal.org/ogr_formats.html)
driver = ogr.GetDriverByName('ESRI Shapefile')

# Make database connection
conn = psycopg2.connect("dbname=proeftoets_angela user=postgres password=postgres")

# Get cursor
cur = conn.cursor()

# Go to directory
# os.chdir('C:/Temp')

# Open shape file
fIn = driver.Open('Data practicum Engineer 1\provincies.shp', 0)

# Get layer from shape file
layer = fIn.GetLayer(0)

# Loop over features
i = 0
for feature in layer:

    # Get attribute values
    i = i + 1
    id = feature.GetFieldAsInteger('id')
    naam = feature.GetFieldAsString('naam')
    geometrie = feature.GetGeometryRef()
    wkt_geometrie = str(geometrie.ExportToWkt())
    
    # Insert row into database, convert wkt from epsg 28992 to 4326
    insert_stmt = 'insert into provincies3 ( id, naam, geom ) values ( %s, %s, ST_GeomFromText(%s, 28992) )' 
    cur.execute ( insert_stmt, ( id, naam, wkt_geometrie ) )
    print ('Provincie ' + str(naam) + ' inserted')

    # Destroy feature and get next feature
    feature.Destroy()

# Close file
fIn.Destroy()    

# Commit and close database connection
conn.commit()
conn.close()

print('End of script')


