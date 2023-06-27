import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import metpy.calc as mpcalc
from metpy.units import units


def average_array_elements(input_array,chunk):
    chunk_size = chunk
    reshaped_array = input_array.reshape(-1, chunk_size)
    averaged_array = np.mean(reshaped_array, axis=1)

    return averaged_array

def comapre_hfxs(measured_hfx,dir='/Users/lmatak/Downloads/temp_foold/all/WRF_CHEM_TIME_SERIES/BEM_MYJ/',file='BEM_MYJ_Jul_2.csv'):
    measured_hfx=measured_hfx
    ##load the csv##
    read_data_from_wrf = pd.read_csv(dir+file, skiprows=1,low_memory=False)  # Assuming tab-separated values
    to_plot_from_wrf=np.array(read_data_from_wrf['CAMS695_HFX'][2:],dtype=float)
    plt.plot(to_plot_from_wrf[0:24])
    plt.plot(average_array_elements(measured_hfx,6))
    plt.legend(['WRF output HFX - 01 - Jul 2019','measured HFX - 01 - Jun 2023'])

    return
def plot_virtual_theta_timeseries(virtual_theta_timeseries):
    plt.title('Virtual potnetial TEMP')
    plt.plot(virtual_theta_timeseries)
    plt.xlabel('record --60s freq')
    plt.ylabel('virtual theta in K')
    
    return

def plot_theta_timeseries(pot_temp_data):
    plt.title('POTENETIAL TEMP')
    plt.plot(average_array_elements(pot_temp_data,300))
    plt.xlabel('record --60s avg freq')
    plt.ylabel('theta in K')
    
    return
def plot_heat_flux(heat_flux):
    plt.title('HeAT FLUX TEMP')
    plt.plot(heat_flux)
    plt.xlabel('time')
    plt.ylabel("w'theta' W/m2")
    plt.title('time average of '+str(average_in_min)+" min")
    
    return
def calculate_virtual_potential_temperature(temperature, relative_humidity):
    # Convert temperature to Kelvin
    temperature_kelvin = temperature

    pressure=1013.25 # amospheric pressure in hPa
    
    # Calculate saturation vapor pressure (es) using Magnus-Tetens equation
    es = 6.112 * np.exp((17.67 * temperature) / (temperature + 243.5))
    
    # Calculate vapor pressure (e) using relative humidity (RH)
    e = (relative_humidity / 100) * es
    
    # Calculate specific humidity (qv)
    qv = 0.622 * (e/ (pressure - 0.378 * e))
    
    # Calculate virtual potential temperature (θv)
    theta_v = temperature_kelvin * (1 + 0.61 * qv)
    
    return theta_v


def calculate_pressure_change(height_change):
    density_air = 1.2  # kg/m³ (approximate value for dry air near sea level)
    gravitational_acceleration = 9.8  # m/s²

    pressure_change = density_air * gravitational_acceleration * height_change
    return pressure_change
def calculate_potential_temperature(temperature, pressure):
    reference_pressure = 100000.0  # 1000 hPa or 100,000 Pa
    gas_constant = 287.04
    specific_heat_capacity = 1005.0


    potential_temperature = temperature * (reference_pressure / pressure) ** (gas_constant / specific_heat_capacity)
    return potential_temperature
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
file_num=3
sonic_files=[]
temperature_files=[]
for file in glob.glob(dir_with_files+'/Winds*'+'.csv'):

        sonic_files.append(file)
# sonic_files=sonic_files.sort()
print(sorted(sonic_files)[file_num])    
sonic_files=sorted(sonic_files) 
for file in glob.glob(dir_with_files+'/T_RH*'+'.csv'):

        temperature_files.append(file)
print(sorted(temperature_files)[file_num])
temperature_files=sorted(temperature_files)

        ## names of the variables in the csv file ##
col_uz = "Uz"
sonic_temp="SonTemp"
temp_deg="AirTC"
rel_hum="RH"
##load the csv##
sonic_data = pd.read_csv(sonic_files[file_num], skiprows=1,low_memory=False)  # Assuming tab-separated values
temperature_data=pd.read_csv(sonic_files[file_num], skiprows=1,low_memory=False)
one_minute_relative_humid=pd.read_csv(temperature_files[file_num], skiprows=1)
print('sonic file: ',sonic_files[file_num])
print('not sonic file: ',temperature_files[file_num])
column_data_relative_humid=np.array(one_minute_relative_humid[rel_hum][2:],dtype=float)

# Access the column containing the data you want to plot, skip first two rows, not numbers ##
column_data_uz = np.array(sonic_data[col_uz][2:],dtype=float)
column_data_temp_deg = np.array(temperature_data[sonic_temp][2:],dtype=float)


temperature_kelvin = column_data_temp_deg + 273.15  # Convert temperature to Kelvin
one_min_sonictemp_avg=(average_array_elements(temperature_kelvin,300))

height_of_anemometar=3+15.24

##calculate potential temperature in two ways##
potential_temp2=calculate_potential_temperature_approx(temperature_kelvin,height_of_anemometar)
# virtual_potential_temp=calculate_virtual_potential_temperature(one_min_sonictemp_avg,column_data_relative_humid,)

##check the potential temp differences
# print(potential_temp[25],potential_temp2[25],column_data_temp_deg[25]+273.15,)  # Output: Potential temperature in Kelvin

##average the sonic data of 5 per second to 1 per minuteto match the temperature reading

# print(len(potential_temp2),len(column_data_uz))


average_in_min=10

potential_temp_from_metpy=mpcalc.potential_temperature(990*units.hPa,temperature_kelvin*units.degK)
w_theta=potential_temp_from_metpy*column_data_uz
heat_flux=1231*calculate_heat_flux(w_theta,column_data_uz,potential_temp_from_metpy,average_in_min)

mixing_ratio=mixing_ratio=mpcalc.mixing_ratio_from_relative_humidity(990 * units.hPa, one_min_sonictemp_avg*units.degK, column_data_relative_humid).to('g/kg')
virtual_potential_temp=mpcalc.virtual_potential_temperature(990 * units.hPa,one_min_sonictemp_avg*units.degK,mixing_ratio*units('g/kg'))
# plot_heat_flux(heat_flux)
# plot_theta_timeseries(potential_temp_from_metpy)
# plot_virtual_theta_timeseries(virtual_potential_temp)
# plt.plot(column_data_relative_humid)
comapre_hfxs(heat_flux)
plt.show()
