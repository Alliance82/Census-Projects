# Created by Alliance82
# Created on 12/29/2023
# This is to create a local database of the NAICS codes and corresponding information from a census.gov excel file
# NAICS is the North American Industry Classification System
# The data is then stored in a local sqlite db for analysis
# This script will kill and fill naics.db
# More info here https://www.census.gov/naics/
import sqlite3
import json, urllib.request, time, datetime as DT
import numpy as np
import pandas as pd
import sys
import struct


# The below is to cleanup data later
whitespace_table = str.maketrans({' ': '', '\t': '', '\n': '', '\r': ''})

# Reading the NAICS Codes from the Excel file
nc = pd.read_excel('NAICS_CODES.xlsx', sheet_name='NAICS_CODES')

# Stroing in a data frame and turning it into a tuple
nc = pd.DataFrame(nc)

print(nc.head())
#nc = nc.to_numpy()
#nc = [tuple(sub_array) for sub_array in nc]

# Creating a connection to the database and creating naics table if it does not exist
connection = sqlite3.connect('naics.db')
cursor = connection.cursor()

# Wipe out any existing data in the naics table so it can be loaded with the current data
try:
    cursor.execute('CREATE TABLE if not exists naics (SEQ TEXT, NAICS_CD INT, NAICS_TITLE TEXT)')
    connection.commit()
    cursor.execute('DELETE FROM naics where id = 1')
    cursor.execute('SELECT * FROM naics')
    data = cursor.fetchall()
    print("This is the initial return from the naics.db:")
    print(data)
except:
    print("An issue creating the table or delete the table contents may have occured. Verify the data.")
else:
    print("An issue creating the table or delete the table contents may have occured. Verify the data.")

print("Before for Loop")
# Loops through all of the data in the NAICS code tuple
for x in range(len(nc)):
    # Store all of the varaibles that are going to be set into the sql db naics.db
    seq = nc.loc[x]['SEQ']
    seq = str(seq)
    seq.translate(whitespace_table)
    naics_cd = nc.loc[x]['NAICS_CD']
    naics_title = nc.loc[x]['NAICS_TITLE']
    print(f"SEQ: {seq} | NAICS CODE: {naics_cd} | TITLE: {naics_title}")
    
    # SQL to insert the variables into the naics.db table
    cursor.execute("insert into naics (SEQ, NAICS_CD, NAICS_TITLE) values (?,?,?)", (seq, naics_cd, naics_title))

# Prints the data that was selected into the sql database and closes the connection
print("This is the final result from the naics.db:")
cursor.execute('SELECT * FROM naics')
data = cursor.fetchall()
print(data)
connection.close()