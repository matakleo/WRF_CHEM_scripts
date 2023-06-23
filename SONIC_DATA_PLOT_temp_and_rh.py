import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

dir_with_files='/Users/lmatak/Downloads/data_from_station'
os.chdir(dir_with_files)
print(dir_with_files)
long_list_with_all=[]
# Read the .dat file into a DataFrame, skipping the first three rows
dat_files=[]
for file in glob.glob(dir_with_files+'/TOA5_HygroVUE*'+'.dat'):

        dat_files.append(file)
pick_a_file=14

fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(16,9),) 
# Read the .dat file into a DataFrame, skipping the first three rows
data = pd.read_csv(dat_files[pick_a_file], skiprows=1)  # Assuming tab-separated values

# Access the column containing the data you want to plot

temp_deg="AirTC"
rel_hum="RH"
# column_data_ux = np.array(data[col_ux][3:],dtype=float)
# column_data_uy = np.array(data[col_uy][3:],dtype=float)
# column_data_uz = np.array(data[col_uz][3:],dtype=float)
column_data_temp_deg = np.array(data[temp_deg][3:],dtype=float)
column_data_rel_hum = np.array(data[rel_hum][3:],dtype=float)
# sqrt_od_vels=(column_data_ux**2+column_data_uy**2+column_data_uz**2)**0.5

# column_data=column_data[::5]
# print(type(column_data))
# print(type(column_data[2]))
# Plot the data
# plt.plot(column_data[3:1000])
# plt.ylim(0,2)
# print(column_data_uz)
# plt.plot(column_data_uz,label='uz')
# plt.plot(column_data_uy,label='uy')
# plt.plot(column_data_ux,label='ux')
axes[0].plot(column_data_temp_deg,label='Temperature')
axes[1].plot(column_data_rel_hum,label='relative humidity %')
# column_data_rel_hum
# plt.plot(sqrt_od_vels,label='vectorial sum')
axes[0].set_xlabel('number of measure')
axes[0].set_ylabel('Temperature deg C')

axes[1].set_xlabel('number of measure')
axes[1].set_ylabel('relative humidity')
# plt.title('Plot of ' + column_name)
# plt.grid(True)
plt.legend()
plt.show()
