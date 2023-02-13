
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
# Read in the CSV file and store it in a Pandas DataFrame
os.chdir('/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/')
df = pd.read_excel('/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/CAMS1_whole_year_nitric_oxide.xlsx')
# date_to_plot = ' 2019-01-01 00:00:00'
df['Date'] = pd.to_datetime(df['Date'])

# Set the date column as the index of the DataFrame
df = df.set_index('Date')

# Specify the date for which you want to retrieve data
month='Aug'


if month =='Jan':
    month_num='01'
elif month=='Feb':
    month_num='02'
elif month=='Mar':
    month_num='03'
elif month=='Apr':
    month_num='04'
elif month=='May':
    month_num='05'
elif month=='Jun':
    month_num='06'
elif month=='Jul':
    month_num='07'
elif month=='Aug':
    month_num='08'
elif month=='Sep':
    month_num='09'
elif month=='Oct':
    month_num='10'
elif month=='Nov':
    month_num='11'
elif month=='Dec':
    month_num='12'

target_date = '2019-'+month_num+'-01'
target_date2= '2019-'+month_num+'-02'
target_date3='2019-'+month_num+'-03'

# Retrieve data for the target date
# target_data = np.array(df.loc[target_date],df.loc[target_date2]df.loc[target_date3])

col1 = np.array(df.loc[target_date])
col2 = np.array(df.loc[target_date2])
col3 = np.array(df.loc[target_date3])

target_data=(np.concatenate((col1,col2,col3),axis=0))
# # Concatenate the columns into one DataFrame


times_on_x_axis=[]


for i in range(3):
    times_on_x_axis.extend(list(range(0,24,4)))


print(times_on_x_axis)
# Display the data
print(target_data)
x=np.arange(0,72,1)
plt.plot(x,target_data,marker='o')
plt.xticks(np.arange(0, 72, 4), x[::4])

plt.show()