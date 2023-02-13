
from audioop import avg
from netCDF4 import Dataset
from numpy.core.fromnumeric import shape, size, transpose
from wrf import getvar,interplevel,latlon_coords
import numpy as np
import math
import csv
import os

from xarray import Coordinate
from all_functions import list_ncfiles, create_file
import glob


#check the output folder!!!!

Output_Dir = '/project/momen/Lmatak/WRF_CHEM/output_files/'
Input_Dir = '/project/momen/Lmatak/WRF_CHEM/YSU_to_LES_chem_10/wrf_run/'

#what you wanna get:?
var="Hourly_LES_outputs"
#at what altitude?
alt=50

CAMS1_pos=([71],[104])
CAMS55_pos=([59],[91])
CAMS35_pos=([101],[67])
CAMS695_pos=([32],[85])
CAMS416_pos=([47],[73])

measuring_stations=[CAMS1_pos,CAMS55_pos,CAMS35_pos,CAMS695_pos,CAMS416_pos]


domain=3
time_idx=0
os.chdir(Input_Dir)
ncfiles = []
########## list to hold the wrfout files ##########
for file in glob.glob(Input_Dir+'wrfout_d0'+str(domain)+'*'):
    ncfiles.append(file)

surface_temperature_list=[]
PM_list=[]
NO_list=[]
NO2_list=[]
WSPD_list=[]





print(ncfiles)

########## STARTS THE LOOP THROUGH THE OUTPUT FILES ##########              ####if changing Tiime_Idx var, make sure to exclued last ncfile!!!
for ncfile in ncfiles:
                surface_temperature_per_file=[]
                pm_per_file=[]
                no_per_file=[]
                no2_per_file=[]
                wspd_per_file=[]
        

                ########## load the data ##########
                data = Dataset(ncfile)

                height = getvar(data, "height_agl",time_idx)
                # get_contour_var = getvar(data, "PM2_5_DRY",time_idx)
                # PM_vals=interplevel(get_contour_var,height,alt)
                wspd=getvar(data, "wspd",time_idx)
                u10=getvar(data, "U10",time_idx)
                v10=getvar(data, "V10",time_idx)
                # nitric_oxide=getvar(data, "no",time_idx)
                # nitric_oxide=interplevel(nitric_oxide,height,alt)
                # nitric_dioxide=getvar(data, "no2",time_idx)
                # nitric_dioxide=interplevel(nitric_dioxide,height,alt)
                outdoor_temperature=getvar(data, "T2",time_idx)

                for measur_station in measuring_stations:

                    wspd=math.sqrt(u10[measur_station]**2+v10[measur_station]**2)
                #     pm_per_file.append(float(PM_vals[measur_station]))
                #     ##1000 multiplier to go from ppm to ppb
                #     no_per_file.append(1000*float(nitric_oxide[measur_station]))
                #     no2_per_file.append(1000*float(nitric_dioxide[measur_station]))


                    wspd_per_file.append(float(wspd))
                    surface_temperature_per_file.append(float(outdoor_temperature[measur_station]))
                surface_temperature_list.append(np.mean(surface_temperature_per_file))    
                # PM_list.append(np.mean(pm_per_file))  
                # NO_list.append(np.mean(no_per_file))  
                # NO2_list.append(np.mean(no2_per_file))  
                WSPD_list.append(np.mean(wspd_per_file))  

                







        ##############################
        # Exporting the simulated data #
        ##############################
print('##########################################################################################')
print('                                   FINISHED EXTRACTION!')
print('##########################################################################################')


########### create the output file      ###################
######################################
create_file (Output_Dir,"LES_outputs_hourly_domain_"+str(domain))
Path = os.getcwd()
MyFile=open('%s.csv' %var,'w')
##write the var name, top left corner
MyFile.write ("LES_hourly_domain"+str(domain)+ "\n")
# MyFile.write ("Temperature,PM2_5,NO,NO2,WSPD\n")
MyFile.write ("Temperature,WSPD\n")

##write longitudes in first row
for hour in range(len(ncfiles)):

##final longitude, swithc to lower row
        MyFile.write(str(surface_temperature_list[hour])+",")
        # MyFile.write(str(PM_list[hour])+",")
        # MyFile.write(str(NO_list[hour])+",")
        # MyFile.write(str(NO2_list[hour])+",")
        MyFile.write(str(WSPD_list[hour])+"\n")

                      

MyFile.close()