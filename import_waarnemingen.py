# Import libraries
import os
import psycopg2

# Open database connection
conn = psycopg2.connect("dbname=proeftoets_angela user=postgres password=postgres")
cur = conn.cursor()

# Open file
# os.chdir('C:/Temp')
csv_file = open('Data practicum Engineer 1\waarnemingen.csv')

# Loop through file and insert into database
lijn_nummer = 0
for lijn in csv_file :
    
    if lijn_nummer >= 0 :
        
        # Get attributes from line
        kolom_nummer = 1
        for kolom in lijn.split(';') :
            if kolom_nummer == 1 :
                id_waarneming = int(kolom)
            if kolom_nummer == 2 :
                date = str(kolom)
            if kolom_nummer == 3 :
                temp = float(kolom)
            kolom_nummer = kolom_nummer + 1
            
        # Insert into database
        insert_stmt = 'insert into waarnemingen ( id_waarneming, date, temp ) values ( %s, %s, %s)' 
        cur.execute ( insert_stmt, ( id_waarneming, date, temp ) )
    
    lijn_nummer = lijn_nummer + 1

print (str(lijn_nummer) + ' lijnen opgeslagen in database')

# Close file
csv_file.close()

# Commit and close database connection
conn.commit()
conn.close()

print('End of script')

