import os
import glob
import psycopg2 # database communicatie

# Functie om survey data te importeren
def import_survey_metadata_file (file_name) :

    # Stap 1: Ophalen waardes uit bestand
    print('Import ' + str(file_name))
    csv_bestand = open(file_name)

    # Inlezen bestand
    rijen = csv_bestand.readlines()

    # Itereer over bestand
    values =[]
    for rij in rijen :
        variable_naam = rij.split(':')[0]
        value = rij.split(':')[1].strip()
        values.append(value)

    # SLuit het bestand
    csv_bestand.close()


    # Stap 2: Insert in database

    # Open database
    db_connection = psycopg2.connect(host="localhost", port="5432", database="engineer", user="postgres", password="postgres")
    cur = db_connection.cursor()

    # Execute SQL
    sql = 'INSERT INTO public.survey(survey_name, survey_date, survey_type, survey_contractor)VALUES (%s, %s, %s, %s)'
    try: 
        cur.execute(sql,(values[0],values[1],values[2],values[3]))
    except :
        print('Survey ' + values[0] + ' kan niet toegevoegd worden')

    # Sla up
    db_connection.commit()

    # Close database
    db_connection.close()

    # https://www.postgresqltutorial.com/postgresql-python/insert/

# Aanroep functie
for filepath in glob.iglob('data\*_metadata.txt'):
    import_survey_metadata_file(filepath)


#import_survey_metadata_file
#('data\H03032_metadata.txt')
