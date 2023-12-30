# Created by Alliance82
# Created on 12/29/2023
# This is to create a local database of the state fips codes and corresponding information from a census.gov excel file
# The data is then stored in a local sqlite db for analysis
# This script will kill and fill state_codes.db
# More info here https://www.census.gov/programs-surveys/bds.html
import sqlite3
import json, urllib.request, time, datetime as DT
import numpy as np
import pandas as pd

# Reading the State Codes from the Excel file
sc = pd.read_excel('STATE_CODES.xlsx', sheet_name='STATE_CODES')

# Stroing in a data frame and turning it into a tuple
sc = pd.DataFrame(sc)
sc = sc.to_numpy()
sc = [tuple(sub_array) for sub_array in sc]

# Creating a connection to the database and creating state_codes table if it does not exist
connection = sqlite3.connect('state_codes.db')
cursor = connection.cursor()
# Wipe out any existing data in the state_codes table so it can be loaded with the current data
cursor.execute('DELETE FROM state_codes')
cursor.execute('SELECT * FROM state_codes')
data = cursor.fetchall()
print("This is the initial return from the state_codes.db:")
print(data)

cursor.execute('CREATE TABLE if not exists state_codes (statefp TEXT, stateabb TEXT, statens TEXT, state_name TEXT)')
connection.commit()

# Loops through all of the data in the state code tuple
for x in range(len(sc)):
    # Store all of the varaibles that are going to be set into the sql db state_codes.db
    statefp = sc[x][1]
    stateabb = sc[x][0]
    statens = sc[x][2]
    state_name = sc[x][3]
    
    # SQL to insert the variables into the state_codes.db table
    cursor.execute("insert into state_codes (statefp, stateabb, statens, state_name) values (?,?,?,?)", (statefp, stateabb, statens, state_name))

# Prints the data that was selected into the sql database and closes the connection
print("This is the final result from the state_codes.db:")
cursor.execute('SELECT * FROM state_codes')
data = cursor.fetchall()
print(data)
connection.close()