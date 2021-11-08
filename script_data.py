import psycopg2
from osgeo import ogr

def import_data(file_name):
    print('Import ' + str(file_name))
   # Open connection
    db_connection = psycopg2.connect(host="localhost", port="5432", database="engineer_eindopdracht", user="postgres", password="postgres")
    cur = db_connection.cursor()

    # Ophalen waardes uit bestand
    csv_bestand = open(file_name)

    # Inlezen bestand
    lines = csv_bestand.readlines()

    i = 0

    # Insert in database
    # Itereer over lijnen
    for line in lines: 

        if i > 0 :
            rijksmonnr = line.split(';')[0]
            cbscategor = line.split(';')[1]
            gemeente = line.split(';')[2]
            provincie = line.split(';')[3]
            plaats = line.split(';')[4]
            x_coord = line.split(';')[5]
            y_coord = line.split(';')[6]

            # Execute SQL
            sql = 'INSERT INTO rijksmonumenten(rijksmonnr, cbscategor, gemeente, provincie, plaats, geom) VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s),28992))'
            cur.execute(sql,(rijksmonnr, cbscategor, gemeente, provincie, plaats, x_coord, y_coord))

        i = i + 1

    # Sluit het bestand
    csv_bestand.close()

    # Sla up
    db_connection.commit()

    # Close database
    db_connection.close()

import_data('rijksmonumenten_nederland_data.csv')

# https://www.youtube.com/watch?v=oAFkPMbwRVY