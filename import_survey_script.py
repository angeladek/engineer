import os
import psycopg2 # database communicatie

# Stap 1: Ophalen waardes uit bestand
csv_bestand = open('data\H00741A_metadata.txt')

# Inlezen bestand
rijen = csv_bestand.readlines()

# Itereer over rijen
values =[]
for rij in rijen :
    variable_name = rij.split(':')[0]
    value = rij.split(':')[1].strip()
    values.append(value)

# Sluit bestand
csv_bestand.close()

# Stap 2: Insert in database

# Open database
db_connection = psycopg2.connect(host="localhost", port="5433", database="engineer", user="postgres", password="postgres")
cur = db_connection.cursor()

# Execute SQL
sql = 'INSERT INTO public.survey(survey_name, survey_date, survey_type, survey_contractor) VALUES (%s, %s, %s, %s)'
cur.execute(sql,(values[0],[1],[2],[3]))

# Close database
db_connection.close()