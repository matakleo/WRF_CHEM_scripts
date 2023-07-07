import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def copy_file(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.write(f_in.read())

dir_with_files='/Users/lmatak/Downloads/data_from_station'
os.chdir(dir_with_files)
print(dir_with_files)
long_list_with_all=[]
time_stamp="TIMESTAMP"
# Read the .dat file into a DataFrame, skipping the first three rows
temp_and_rh_files=[]
sonic_winds_files=[]
for file in glob.glob(dir_with_files+'/TOA5_HygroVUE*'+'.dat'):

        temp_and_rh_files.append(file)
for file in temp_and_rh_files:
# Read the .dat file into a DataFrame, skipping the first three rows
        data = pd.read_csv(file, skiprows=1)  # Assuming tab-separated values
        time_stamping = str(data[time_stamp][2])
        name_to_save="T_RH_"+time_stamping[0:10]+".csv"


        copy_file(file,name_to_save)

for file in glob.glob(dir_with_files+'/TOA5_SonicData*'+'.dat'):

        sonic_winds_files.append(file)
for file in sonic_winds_files:
# Read the .dat file into a DataFrame, skipping the first three rows
        data = pd.read_csv(file, skiprows=1)  # Assuming tab-separated values
        time_stamping = str(data[time_stamp][2])
        name_to_save="Winds_"+time_stamping[0:10]+".csv"


        copy_file(file,name_to_save)

