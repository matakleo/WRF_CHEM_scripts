
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
Input_Dir = '/project/momen/Lmatak/WRF_CHEM/Jun_No_urb_3_dom/'
#what you wanna get:?
#at what altitude?
alt=30

## SELECT DOMAIN ##
domain=3
############
var="Jun_no_urb"+str(domain)

if domain == 4:
### this is for four domain run!
    CAMS1_pos=([120],[72])
    CAMS55_pos=([105],[58])
    CAMS35_pos=([75],[109])
    CAMS695_pos=([97],[24])
    CAMS416_pos=([83],[43])
# theser are for three domain run:
elif domain == 3:
    CAMS1_pos=([64],[73])
    CAMS55_pos=([61],[70])
    CAMS35_pos=([55],[80])
    CAMS695_pos=([59],[63])
    CAMS416_pos=([56],[67])

elif domain ==1:
    CAMS1_pos=([49],[49])
    CAMS55_pos=([49],[49])
    CAMS35_pos=([49],[49])
    CAMS695_pos=([49],[49])
    CAMS416_pos=([49],[49])


## these are for two domain run
elif domain == 2:
    CAMS1_pos=([67],[69])
    CAMS55_pos=([67],[69])
    CAMS35_pos=([66],[71])
    CAMS695_pos=([66],[67])
    CAMS416_pos=([66],[68])

##for three domain run ##

measuring_stations=[CAMS1_pos,CAMS55_pos,CAMS35_pos,CAMS695_pos,CAMS416_pos]


time_idx=0
os.chdir(Input_Dir)
ncfiles = []

#name of the excel output file#
#var="pbl_pbl_LES_chem_d"+str(domain)
########## list to hold the wrfout files ##########
for file in glob.glob(Input_Dir+'wrfout_d0'+str(domain)+'*'):
    ncfiles.append(file)
ncfiles.sort()

### this is for what I find real data ##
surface_temperature_list=[]
PM_list=[]
Ozone_list=[]
NO_list=[]
NO2_list=[]
NO2_list=[]
WSPD_list=[]

dom_avg_surface_temperature_list=[]
dom_avg_PM_list=[]
dom_avg_NO_list=[]
dom_avg_NO2_list=[]
dom_avg_Ozone_list=[]
dom_avg_WSPD_list=[]




for ncfile in ncfiles:
                print('workin on: ',ncfile)
                surface_temperature_per_file=[]
                pm_per_file=[]
                no_per_file=[]
                no2_per_file=[]
                wspd_per_file=[]
                ozone_per_file=[]

                dom_avg_surface_temperature_per_file=[]
                dom_avg_pm_per_file=[]
                dom_avg_no_per_file=[]
                dom_avg_no2_per_file=[]
                dom_avg_ozone_per_file=[]
                dom_avg_wspd_per_file=[]
        

                ########## load the data ##########
                data = Dataset(ncfile)

                height = getvar(data, "height_agl",time_idx)

                #chem variabsl#
                pm_2_5 = getvar(data, "PM2_5_DRY",time_idx)
                pm_2_5=interplevel(pm_2_5,height,alt)
                
                ozone=getvar(data, "o3",time_idx)
                ozone=interplevel(ozone,height,alt)
                nitric_oxide=getvar(data, "no",time_idx)
                nitric_oxide=interplevel(nitric_oxide,height,alt)
                nitric_dioxide=getvar(data, "no2",time_idx)
                nitric_dioxide=interplevel(nitric_dioxide,height,alt)
                #met variabls#

                u10=getvar(data, "U10",time_idx)
                v10=getvar(data, "V10",time_idx)
                outdoor_temperature=getvar(data, "T2",time_idx)

                for measur_station in measuring_stations:

                    wspd=math.sqrt(u10[measur_station]**2+v10[measur_station]**2)
                    dom_avg_wspd=math.sqrt(np.mean(u10)**2+np.mean(v10)**2)

                    pm_per_file.append(float(pm_2_5[measur_station]))
                #     ##1000 multiplier to go from ppm to ppb
                    no_per_file.append(1000*float(nitric_oxide[measur_station]))
                    no2_per_file.append(1000*float(nitric_dioxide[measur_station]))
                    ozone_per_file.append(1000*float(ozone[measur_station]))

                    wspd_per_file.append(2.23693629*float(wspd))
                    surface_temperature_per_file.append(float(outdoor_temperature[measur_station]*9/5-459.67))



                    dom_avg_wspd_per_file.append(2.23693629*float(dom_avg_wspd))
                    dom_avg_surface_temperature_per_file.append(float(np.mean(outdoor_temperature)*9/5-459.67))
                print('temp =',(np.mean(surface_temperature_per_file)))
                surface_temperature_list.append(np.mean(surface_temperature_per_file))  
                WSPD_list.append(np.mean(wspd_per_file)) 

                #chem vars  
                PM_list.append(np.mean(pm_per_file))  
                NO_list.append(np.mean(no_per_file))  
                NO2_list.append(np.mean(no2_per_file))  
                Ozone_list.append(np.mean(ozone_per_file))
                #domain averages
                dom_avg_PM_list.append(float(np.mean(pm_2_5)))
                dom_avg_NO_list.append(float(np.mean(nitric_oxide)))
                dom_avg_NO2_list.append(float(np.mean(nitric_dioxide)))
                dom_avg_Ozone_list.append(float(np.mean(ozone)))

                dom_avg_surface_temperature_list.append(np.mean(dom_avg_surface_temperature_per_file))    
                dom_avg_WSPD_list.append(np.mean(dom_avg_wspd_per_file))  

                







        ##############################
        # Exporting the simulated data #
        ##############################
print('##########################################################################################')
print('                                   FINISHED EXTRACTION!')
print('##########################################################################################')


########### create the output file      ###################
######################################
# create_file (Output_Dir,"LES_outputs_hourly_domain_"+str(domain))
# Path = os.getcwd()
os.chdir(Output_Dir)
MyFile=open('%s.csv' %var,'w')
##write the var name, top left corner
MyFile.write (var+ "\n")
# MyFile.write ("Temperature,PM2_5,NO,NO2,WSPD\n")
MyFile.write ("pm25,no,no2,ozone,dom_avg_pm25,dom_avg_no,dom_avg_no2,dom_avg_ozone,WSPD,Temperature,dom_avg_Temperature,dom_avg_WSPD\n")

##write longitudes in first row
for hour in range(len(ncfiles)):

##CHEMICAL VARS##
        
        MyFile.write(str(PM_list[hour])+",")
        MyFile.write(str(NO_list[hour])+",")
        MyFile.write(str(NO2_list[hour])+",")
        MyFile.write(str(Ozone_list[hour])+",")
        MyFile.write(str(dom_avg_PM_list[hour])+",")
        MyFile.write(str(dom_avg_NO_list[hour])+",")
        MyFile.write(str(dom_avg_NO2_list[hour])+",")
        MyFile.write(str(dom_avg_Ozone_list[hour])+",")
        
##MET VARS##
        MyFile.write(str(WSPD_list[hour])+",")
        MyFile.write(str(surface_temperature_list[hour])+",")
        MyFile.write(str(dom_avg_surface_temperature_list[hour])+",")
        MyFile.write(str(dom_avg_WSPD_list[hour])+"\n")

                      

MyFile.close()
