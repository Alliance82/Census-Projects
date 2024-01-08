# Created by Alliance82
# Created on 12/29/2023
# This is to connect and pull back Business Dynamic data from the US Census Bureau
# The data is then stored in a local sqlite db for analysis
# More info here https://www.census.gov/programs-surveys/bds.html
# Updated to form a list of all of the combinations of API strings for states, NAICS, and year
import sqlite3
import json, urllib.request, time, datetime as DT
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

#The below is the path to the file that the API Key is kept in
api_key_path = r'Your API Key Path Goes Here'
sys.path.append(api_key_path)
from Census_API_Key import apiKey
apiKey = apiKey
sys.path.remove(api_key_path)

baseURL = url = "https://api.census.gov/data/timeseries/"
i=0
year = []
y = 1978
stateCode=[]

# Arrays that are used to modify the URL's for the API request
state_url = []
year_url = []
naics_url = []

# Array that stores all of the API calls
url_array = []

# This is the array that the API results for all states are stored in
businessDyanmics = []

# Array of the NAICS Codes that I am interested in
# 23 is construction; 31-33 is manufacturing;  54 is professional, technical, and scientific services
naics_api = ['23', '31-33', '54']

# Making an array for the years, data is available from 1978 to 2021
for y in range(1978, 2022):
    year.append(y)

# Loops through the state codes for the 56 State FIPS codes. Set to loop through just a couple states for example.
for i in range(1, 6):
    i=i+1
    if i < 10:
        stateCode.append("0"+str(i))
    else:
        stateCode=str(i)
    print(stateCode)

# Creating a 3D grid that has all combinations of state codes, year, and naics sectors
grid = np.meshgrid(stateCode, year, naics_api)
combinations = np.array(grid).T.reshape(-1, 3)

# Transforming the reshaped array into a DataFrame and changing it into a tuple that is straight forward to iterate through
combinations = pd.DataFrame(combinations)
combinations = combinations.to_numpy()
combinations = [tuple(sub_array) for sub_array in combinations]
print(combinations)

# Builds all of the url's and stores them in the url_array
for x in range(len(combinations)):
    state_url = combinations[x][0]
    year_url = combinations[x][1]
    naics_url = combinations[x][2]
    
    url = baseURL + "bds?get=JOB_CREATION&for=state:" + state_url + "&YEAR=" + year_url + "&NAICS=" + naics_url + "&key=" + apiKey
    url_array.append(url)

# Loops through all of the url's and uses those for the API requests, then stores the results in businessDynamics    
for y in range(len(url_array)):
    
    # Using exception handling in case some of the API calls fail or are unreachable
    try:
        print(url_array[y])
        response = urllib.request.urlopen(url_array[y])
        data = json.loads(response.read())
        data1=data[1]
        print(data1)
        businessDyanmics.append(data1)
    except: 
        print("Was not able to retrieve or translate the data")

# Display the resulting array produced by the API calls
print(businessDyanmics)

# Storing all of the data locally
# Connect to sqlite db
connection = sqlite3.connect('job_creation_state.db')
cursor = connection.cursor()
# Wipe out any existing data in the state_codes table so it can be loaded with the current data
cursor.execute('DELETE FROM job_creation_state')

# Create business dynamics sql db to store locally
cursor.execute('CREATE TABLE if not exists job_creation_state (JOB_CREATION INT, YEAR TEXT, NAICS_CD TEXT, STATE_CD TEXT)')
connection.commit()

# Loops through the array of results from the API and stores the data in job_creation_state.db locally
for x in range(len(businessDyanmics)):
    job_creation = businessDyanmics[x][0]
    year = businessDyanmics[x][1]
    naics_cd = businessDyanmics[x][2]
    state_cd = businessDyanmics[x][3]
    
    cursor.execute("insert into job_creation_state (JOB_CREATION, YEAR, NAICS_CD, STATE_CD) values (?,?,?,?)", (job_creation, year, naics_cd, state_cd))
    connection.commit()
    
print("Data has been inserted into the job_creation_state.db")
cursor.execute('SELECT * FROM job_creation_state')
cursor.execute("ATTACH DATABASE 'state_codes.db' AS state_codes")
cursor.execute("SELECT JOB_CREATION, YEAR, NAICS_CD, state_name FROM job_creation_state INNER JOIN state_codes ON job_creation_state.STATE_CD = state_codes.statefp")
connection.commit()
data = cursor.fetchall()
print("This is the joined data")
print(data)
connection.close()

# Turning the joined data into a DataFrame so that it can be plotted easily without loops
df = pd.DataFrame(data, columns=['JOB_CREATION', 'YEAR', 'NAICS_CD', 'STATE'])
df = df.groupby(['YEAR', 'STATE'])['JOB_CREATION'].sum().unstack()

# Plotting the DataFrame to show Job Creation by Year with States as a series
plt.plot(df, '-')
plt.xticks(range( 0, 45, 3), rotation=45)
plt.xlabel('Year')
plt.ylabel('Job Creation')
plt.legend(df.columns)
plt.show()
