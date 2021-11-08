import psycopg2
from osgeo import ogr

file_name = 'provinciegrenzen_nl\provinciegrenzen_nl.shp'

# Open connection
db_connection = psycopg2.connect(host="localhost", port ="5432", database="engineer_eindopdracht", user="postgres", password="postgres")
cur = db_connection.cursor()

# Open shape file
driver = ogr.GetDriverByName('ESRI Shapefile')
dataSource = driver.Open(file_name, 0)
layer = dataSource.GetLayer()

# Itereer over features
for feature in layer: 

    # Ophalen attribuutwaardes en geometry
    provincie = feature.GetField("provincien")
    geom = feature.GetGeometryRef()
    geom_wkt = geom.ExportToWkt()

    # insert
    sql = 'INSERT INTO public.provinciegrenzen(provincie, geom)	VALUES (%s, ST_GeometryFromText(%s,28992))'
    cur.execute(sql,(provincie, geom_wkt))

# Sla op
db_connection.commit()

# Close database
db_connection.close()

# Start
# import_product_grenzen('provinciegrenzen_nl\provinciegrenzen_nl.shp')