import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the .dat file into a DataFrame, skipping the first three rows
data = pd.read_csv('/Users/lmatak/Downloads/test_data1/TOA5_HygroVUE_Data14.dat', skiprows=1)  # Assuming tab-separated values
print(data.head)
# Access the column containing the data you want to plot
col_uz = "Uz"
col_ux="Ux"
col_uy="Uy"
temp_deg="AirTC"
rel_hum="RH"
# column_data_ux = np.array(data[col_ux][3:],dtype=float)
# column_data_uy = np.array(data[col_uy][3:],dtype=float)
# column_data_uz = np.array(data[col_uz][3:],dtype=float)
# column_data_temp_deg = np.array(data[temp_deg][3:],dtype=float)
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
# plt.plot(column_data_temp_deg,label='Temperature')
plt.plot(column_data_rel_hum,label='relative humidity %')
# column_data_rel_hum
# plt.plot(sqrt_od_vels,label='vectorial sum')
plt.xlabel('X-axis label')
plt.ylabel('Y-axis label')
# plt.title('Plot of ' + column_name)
# plt.grid(True)
plt.legend()
plt.show()
