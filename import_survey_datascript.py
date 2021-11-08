import psycopg2
import file_helper
import glob # database communicatie

# Function to import xyz data
def import_survey_data(file_name):

    # Ophalen survey_name
    survey_name = file_helper.get_file_name_without_path_and_extension(file_name)
    print(survey_name)

    db_connection = psycopg2.connect(host="localhost", port ="5432", database="engineer", user="postgres", password="postgres")
    cur = db_connection.cursor()

# Select sql
    sql = 'select survey_id from survey where survey_name = %s'
    cur.execute(sql,(survey_name,))

    # Ophalen rij
    row = cur.fetchone()
    survey_id = row[0]
    print(survey_id)

    # Open csv file
    csv_file = open(file_name)
    lines = csv_file.readlines()

    # Itereer over lijnen
    for line in lines: 
        x = line.split()[0]
        y = line.split()[1]
        z = line.split()[2]

        # insert
        sql = 'INSERT INTO public.sounding(depth, geom, survey_id)	VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s),4326), %s)'
        cur.execute(sql,(z,x,y,survey_id))

    # Sla op
    db_connection.commit()

    # Close database
    db_connection.close()

# Start

import_survey_data('data\H06995.xyz')

for filepath in glob.iglob('engineer-2021---2022-MarkTerlien\data\*.xyz'):
    print(filepath)
    import_survey_data(filepath)