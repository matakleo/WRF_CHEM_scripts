import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
def average_array_elements(input_array,chunk):
    chunk_size = chunk
    reshaped_array = input_array.reshape(-1, chunk_size)
    averaged_array = np.mean(reshaped_array, axis=1)

    return averaged_array

def calculate_pressure_change(height_change):
    density_air = 1.2  # kg/m³ (approximate value for dry air near sea level)
    gravitational_acceleration = 9.8  # m/s²

    pressure_change = density_air * gravitational_acceleration * height_change
    return pressure_change

# Example usage
def calculate_potential_temperature(temperature, pressure):
    reference_pressure = 100000.0  # 1000 hPa or 100,000 Pa
    gas_constant = 287.04
    specific_heat_capacity = 1005.0


    potential_temperature = temperature * (reference_pressure / pressure) ** (gas_constant / specific_heat_capacity)
    return potential_temperature


# Example usage
def calculate_potential_temperature_approx(temperature, altitude):



    potential_temperature = temperature + 0.0098*altitude
    return potential_temperature



def calculate_heat_flux(w_theta,w,theta,minutes_of_avg):
     time_to_average=minutes_of_avg*300
     w_theta_five_min=average_array_elements(w_theta,time_to_average)
     theta_five_min=average_array_elements(theta,time_to_average)
     w_five_min=average_array_elements(w,time_to_average)

     print('w_th',len(w_theta_five_min),'theta',len(theta_five_min),'wind',len(w_five_min))

     return w_theta_five_min-theta_five_min*w_five_min



dir_with_files='/Users/lmatak/Downloads/data_from_station/Renamed_data'
os.chdir(dir_with_files)
print(dir_with_files)
long_list_with_all=[]
# Read the .dat file into a DataFrame, skipping the first three rows
file_num=6
sonic_files=[]
temperature_files=[]
for file in glob.glob(dir_with_files+'/Winds*'+'.csv'):

        sonic_files.append(file)
for file in glob.glob(dir_with_files+'/T_RH*'+'.csv'):

        temperature_files.append(file)

        ## names of the variables in the csv file ##
col_uz = "Uz"
sonic_temp="SonTemp"
temp_deg="AirTC"
rel_hum="RH"

to_average_all_data=[]

average_in_min=2

for i in range(len(sonic_files)):
    ##load the csv##
    sonic_data = pd.read_csv(sonic_files[i], skiprows=1,low_memory=False)  # Assuming tab-separated values
    temperature_data=pd.read_csv(sonic_files[i], skiprows=1,low_memory=False)

    # Access the column containing the data you want to plot, skip first two rows, not numbers ##
    column_data_uz = np.array(sonic_data[col_uz][2:],dtype=float)
    column_data_temp_deg = np.array(temperature_data[sonic_temp][2:],dtype=float)

    temperature_kelvin = column_data_temp_deg + 273.15  # Convert temperature to Kelvin

    height_of_anemometar=3

    ##calculate potential temperature in two ways##
    # potential_temp = calculate_potential_temperature(temperature_kelvin, 100000-calculate_pressure_change(height_of_anemometar))
    potential_temp2=calculate_potential_temperature_approx(temperature_kelvin,height_of_anemometar)

    ##check the potential temp differences
    # print(potential_temp[25],potential_temp2[25],column_data_temp_deg[25]+273.15,)  # Output: Potential temperature in Kelvin


    ##average the sonic data of 5 per second to 1 per minuteto match the temperature reading
    # one_min_sonic_avg=(average_array_elements(column_data_uz,300))
    # print(len(potential_temp2),len(column_data_uz))
    try:
        w_theta=potential_temp2*column_data_uz
        heat_flux=calculate_heat_flux(w_theta,column_data_uz,potential_temp2,average_in_min)
        to_average_all_data.append(heat_flux)
    except:
         print(sonic_files[i]," failed")
         continue

    
    


# column_data_rel_hum = np.array(data[rel_hum][3:],dtype=float)

# column_data_rel_hum
plt.plot(np.mean(to_average_all_data,axis=0),label='vectorial sum')
plt.xlabel('time')
plt.ylabel("w'theta'")
plt.title('time average of '+str(average_in_min)+" min")
# plt.grid(True)
# plt.legend()
plt.show()
