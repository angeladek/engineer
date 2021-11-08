# Import libraries
import os
import psycopg2
import psycopg2
from osgeo import ogr

# Open database connection
conn = psycopg2.connect("dbname=proeftoets_angela user=postgres password=postgres")
cur = conn.cursor()

# Create new shapefile (see https://gdal.org/drivers/vector/index.html for formats)
# os.chdir('C:/Temp')
driver = ogr.GetDriverByName( 'ESRI Shapefile' )
fOut = driver.CreateDataSource('provincies_export2.shp')

# Create layer definition
outLayer = fOut.CreateLayer('provincies', geom_type=ogr.wkbPolygon)
outLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
outLayer.CreateField(ogr.FieldDefn('naam', ogr.OFTString))        
featureDefn = outLayer.GetLayerDefn()

# Select all rows from database
sql = 'select id, naam, ST_AsText(geom) from provincies2'
cur.execute(sql)
rows = cur.fetchall()
i = 0

# Loop through row, create feature and write to shapefile
for row in rows :
    id = int(row[0])
    naam = str(row[1])
    geom = str(row[2])
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetField('id', id)       
    outFeature.SetField('naam', naam)
    outFeature.SetGeometry(ogr.CreateGeometryFromWkt(geom))
    outLayer.CreateFeature(outFeature)
    i = i + 1

print(str(i) + ' rijen opgeslagen in shapefile')

# Close shapefile
fOut.Destroy()

# Close database connection
conn.close()

print('End of script')

