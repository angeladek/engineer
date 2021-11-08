import psycopg2
from osgeo import ogr

# Function to import xyz data
def import_product_grens(file_name):

   # Open connection
    db_connection = psycopg2.connect(host="localhost", port ="5432", database="engineer", user="postgres", password="postgres")
    cur = db_connection.cursor()

    # Open shape file
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(file_name, 0)
    layer = dataSource.GetLayer()
    

    # Itereer over features
    for feature in layer: 

        # Ophalen attribuutwaardes en geometry
        name = feature.GetField("name")
        geom = feature.GetGeometryRef()
        geom_wkt = geom.ExportToWkt()

        # insert
        sql = 'INSERT INTO public.product_boundary(name, boundary)	VALUES (%s, ST_GeometryFromText(%s,4326))'
        cur.execute(sql,(name, geom_wkt))

    # Sla op
    db_connection.commit()

    # Close database
    db_connection.close()

# Start
import_product_grens('product_boundaries_data\product_boundaries.shp')