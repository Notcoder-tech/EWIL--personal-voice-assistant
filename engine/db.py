import csv
import sqlite3

conn = sqlite3.connect("ewil.db")
cursor = conn.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null,'discord', 'C:\\Users\\Jatin\\AppData\\Local\\Discord\\app-1.0.9211\\Discord.exe')"
#cursor.execute(query)
#conn.commit()

#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO web_command VALUES (null,'hotstar', 'https://www.hotstar.com/in/onboarding/profile?ref=%2Fin%2Fhome')"
#cursor.execute(query)
#conn.commit()

#cursor.execute("DELETE FROM web_command WHERE id = ?", (23,))
#conn.commit()

#Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL, address VARCHAR(255) NULL)''')

#desired_columns_indices = [0, 18]

## Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
     #csvreader = csv.reader(csvfile)
     #for row in csvreader:
        # selected_data = [row[i] for i in desired_columns_indices]
         #cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
#conn.commit()
#conn.close()
