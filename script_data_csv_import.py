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
            naam = line.split(';')[1]
            cbscategor = line.split(';')[2]
            oorsprfunc = line.split(';')[3]
            subcatoms = line.split(';')[4]
            hfdcatoms = line.split(';')[5]
            bouwjaar = line.split(';')[6]
            gemeente = line.split(';')[7]
            provincie = line.split(';')[8]
            plaats = line.split(';')[9]
            situering = line.split(';')[10]
            straat = line.split(';')[11]
            huisnummer = line.split(';')[12]
            toevoeging = line.split(';')[13]
            postcode = line.split(';')[14]
            kich_url = line.split(';')[15]
            adres = line.split(';')[16]
            x_coord = line.split(';')[17]
            y_coord = line.split(';')[18]

            # Execute SQL
            sql = 'INSERT INTO rijksmonumenten_nl(rijksmonnr, naam, cbscategor, oorsprfunc, subcatoms, hfdcatoms, bouwjaar, gemeente, provincie, plaats, situering, straat, huisnummer, toevoeging, postcode, kich_url, adres, geom) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s),28992))'
            cur.execute(sql,(rijksmonnr, naam, cbscategor, oorsprfunc, subcatoms, hfdcatoms, bouwjaar, gemeente, provincie, plaats, situering, straat, huisnummer, toevoeging, postcode, kich_url, adres, x_coord, y_coord))

        i = i + 1

    # Sluit het bestand
    csv_bestand.close()

    # Sla up
    db_connection.commit()

    # Close database
    db_connection.close()

import_data('rijksmonumenten_nederland_compleet.csv')

# https://www.youtube.com/watch?v=oAFkPMbwRVY