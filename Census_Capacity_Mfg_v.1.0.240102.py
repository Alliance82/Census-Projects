# Created By Alliance82
# Created On 01/01/2024
# This was created to compile, store, and plot the monthly capacity rates
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# Setting the initial variables that will be used
capacity_arr = []
base_file_name = "-qtr-table-final-q"
file_loc = "C:\\Users\\brett\\OneDrive\\Documents\\Census Project\\Capacity Data\\"

# Loop to read through all the files and append the data so a single array
for i in range(2021, 2024):
    for q in range (1, 5):
        file_name = str(i) + base_file_name + str(q) + ".xlsx"
        file_path = file_loc + file_name
        print(file_name)
        try:
            
            # Reads into the file, drops the header and footer and then any additional completely blank rows
            df = pd.read_excel(file_path, sheet_name='FULL Utilization Rates', usecols="A, D, E", skiprows=4)
            
            # Cleaning the data, filling in blanks, removing blank rows, removing whitespace from data fields, and applying short names
            df = df.dropna(how='all')
            df = df.fillna(0)
            df.rename(columns={'NAICS Code(s)': 'NAICS', 'Utilization rate': 'UTIL_RATE', 'Standard error ': 'STD_ERR'}, inplace=True)
            df = df.replace("\s+", "", regex=True)
            
            # Filter the Data for 31-33: Manufacturing, 334413: Semiconductor, 3315: Foundries
            df = df.loc[df["NAICS"].isin(['31-33', '334413', '3315'])]
            for y, row in df.iterrows():
                try: 
                    naics = row.get('NAICS')
                    util_rate = row.get('UTIL_RATE')
                    
                except:
                    pass
                rpt_pd = str(i) + "-Q" + str(q)
                capacity_arr.append([rpt_pd, naics, util_rate])
                
        except:
            pass

# Forming a DataFrame and preparing it for the plot by grouping the DataFrame
df = pd.DataFrame(capacity_arr, columns=['rpt_pd', 'naics', 'util_rate'])
df = df.groupby(['rpt_pd', 'naics'])['util_rate'].sum().unstack()

# Creating a dictionairy to map the naics codes to naics names
naics_list = df.columns
naics_dict = {
    '31-33': 'Manufacturing',
    '334413': 'Semiconductor',
    '3315': 'Foundries'
}
naics_legend = [naics_dict[code] for code in naics_list]

# Plotting the Utilization Rate vs Reporting Quarter and specifying settings for the plot
plt.plot(df)
plt.legend(naics_legend)
plt.xticks(rotation=45)
plt.xlabel('Reporting Quarter')
plt.ylabel('Utilization Rate')
plt.title('Manufacturing Utilization Rates 2021-2023')
plt.show()