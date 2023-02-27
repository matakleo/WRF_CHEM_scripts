
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

domain =3

#if domain=='LES':
#    CAMS1_pos=([250],[297])
#    CAMS55_pos=([235],[283])
#    CAMS35_pos=([205],[334])
#    CAMS695_pos=([227],[249])
#    CAMS416_pos=([213],[268])



if domain ==4:
#    CAMS1_pos=([120],[72])
#    CAMS55_pos=([105],[58])
#    CAMS35_pos=([75],[109])
#    CAMS695_pos=([97],[24])
#    CAMS416_pos=([83],[43])

    ##FOR LES ONLY##

    CAMS1_pos=([250],[297])
    CAMS55_pos=([235],[283])
    CAMS35_pos=([205],[334])
    CAMS695_pos=([227],[249])
    CAMS416_pos=([213],[268])


# theser are for three domain run:
elif domain == 3:
    CAMS404_pos=( [67] , [67] )
    CAMS1052_pos=([68],[60])
    CAMS695_pos=([59],[63])
    CAMS53_pos= ([57],[51])
    CAMS409_pos=( [50] , [53] )
    CAMS8_pos=( [76] , [65] )
    CAMS416_pos=([56],[67])
    CAMS1_pos=([64],[73])
    CAMS603_pos=( [63] , [76] )
    CAMS403_pos=( [61] , [70] )
    CAMS167_pos=( [61] , [72] )
    CAMS1029_pos=( [59] , [70] )
    CAMS169_pos=([58],[70])
    CAMS670_pos=( [58] , [70] )
    CAMS1020_pos=( [56] , [70] )
    CAMS1049_pos=( [58] , [73] )

measuring_stations=[CAMS404_pos,CAMS1052_pos,CAMS695_pos,CAMS53_pos,CAMS409_pos,CAMS8_pos,CAMS416_pos,CAMS1_pos,\
    CAMS603_pos,CAMS403_pos,CAMS167_pos,CAMS1029_pos,CAMS169_pos,CAMS670_pos,CAMS1020_pos,CAMS1049_pos] 



stations_dict={}
keys_for_dict = ['CAMS404','CAMS1052','CAMS695','CAMS53','CAMS409','CAMS8','CAMS416','CAMS1','CAMS603','CAMS403','CAMS167','CAMS1029',\
    'CAMS169','CAMS670','CAMS1020','CAMS1049']



time_idx=0



#check the output folder!!!!

Output_Dir = '/project/momen/Lmatak/WRF_CHEM/output_files/URBAN_SIMS/Time_Series_Temperature/'

PBL="MYJ"
urban='SLUCM'
#for BEM uncomment this:
Input_Dir = '/project/momen/Lmatak/WRF_CHEM/SLUCM_SCHEME_RUNS/simulation_runs/'

#Input_Dir='/project/momen/Lmatak/WRF_CHEM/URBAN_SCHEME_RUNS/simulation_runs/'

#dir_names=['Default_BEM','Decreased_Buildings','Default_No_Urb','Increased_Buildings','cd_0.5','cd_2.0','cd_3.0','cd_4.0','Mom_0.2','Mom_5.0','Mom_2.0','Mom_0.5']
dir_names=['Default_SLUC','Ustar_10_SLUC','Ustar_20_SLUC','Ustar_5_SLUC' ]
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#dir_names=['Default_BEM','Decreased_Buildings','Default_No_Urb','Increased_Buildings'] #,'Mom_0.2','Mom_5.0','Mom_2.0','Mom_0.5']
#at what altitude?
alt=50


for dir_name in dir_names:
    ##create file is for creating a directory
    create_file(Output_Dir,PBL+"_"+dir_name)
    for month in months:
        
        for d in keys_for_dict:
            #initialize the dictionary with keys as empty lists
            stations_dict[d]=[]



            ## UNCOMMENT FOR DEFAULT  ##
        
        #working_dir=Input_Dir+PBL+  "/" +dir_name + "/" +PBL+"_"+dir_name+"_"+month 
        working_dir=Input_Dir+  "/" +dir_name + "/" +PBL+"/"+month
        print('working dir = '+working_dir)

        os.chdir(working_dir)
        ncfiles = []

########## list to hold the wrfout files ##########
        for file in glob.glob(working_dir+'/wrfout_d0'+str(domain)+'*'):
            ncfiles.append(file)
        ncfiles.sort()
        surface_temperature_list=[]
        PM_list=[]
        NO_list=[]
        NO2_list=[]
        WSPD_list=[]

        dom_avg_surface_temperature_list=[]
        dom_avg_PM_list=[]
        dom_avg_NO_list=[]
        dom_avg_NO2_list=[]
        dom_avg_WSPD_list=[]






#print(ncfiles)

########## STARTS THE LOOP THROUGH THE OUTPUT FILES ##########              ####if changing Tiime_Idx var, make sure to exclued last ncfile!!!
        for ncfile in ncfiles:
            print('workin on: ',ncfile)
            surface_temperature_per_file=[]
            pm_per_file=[]
            no_per_file=[]
            no2_per_file=[]
            wspd_per_file=[]

            dom_avg_surface_temperature_per_file=[]
            dom_avg_pm_per_file=[]
            dom_avg_no_per_file=[]
            dom_avg_no2_per_file=[]
            dom_avg_wspd_per_file=[]
    

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
            stations_counter=0
            for measur_station in measuring_stations:
                
                                     
                    surface_temperature_per_file=(float(outdoor_temperature[measur_station]*9/5-459.67))

                    print('value to be appended:',surface_temperature_per_file)

                    
                    #stations_dict[keys_for_dict[stations_counter]].append(2.23693629*float(wspd))
                    stations_dict[keys_for_dict[stations_counter]].append(surface_temperature_per_file)
                    stations_counter+=1


#        print(month)
#        print(stations_dict['CAMS53'])
        var=dir_name+"_"+month
        os.chdir(Output_Dir+PBL+"_"+dir_name)
        MyFile=open('%s.csv' %var,'w')
        ##write the var name, top left corner
        MyFile.write ("Urban_schemes_temperature_"+str(domain)+ "\n")
        # MyFile.write ("Temperature,PM2_5,NO,NO2,WSPD\n")

        MyFile.write ("CAMS404_temperature,CAMS1052_temperature,CAMS695_temperature,CAMS53_temperature,CAMS409_temperature,CAMS8_temperature,CAMS416_temperature,CAMS1_temperature,CAMS603_temperature,CAMS403_temperature,CAMS167_temperature,CAMS1029_temperature,CAMS169_temperature,CAMS670_temperature,CAMS1020_temperature,CAMS1049_temperature\n")  

        ##write longitudes in first row
        for hour in range(len(ncfiles)-1):

        ##final longitude, swithc to lower row

                MyFile.write(str(stations_dict['CAMS404'][hour])+",")
                MyFile.write(str(stations_dict['CAMS1052'][hour])+",")
                MyFile.write(str(stations_dict['CAMS695'][hour])+",")
                MyFile.write(str(stations_dict['CAMS53'][hour])+",")
                MyFile.write(str(stations_dict['CAMS409'][hour])+",")
                MyFile.write(str(stations_dict['CAMS8'][hour])+",")
                MyFile.write(str(stations_dict['CAMS416'][hour])+",")
                MyFile.write(str(stations_dict['CAMS1'][hour])+",")
                MyFile.write(str(stations_dict['CAMS603'][hour])+",")
                MyFile.write(str(stations_dict['CAMS403'][hour])+",")
                MyFile.write(str(stations_dict['CAMS167'][hour])+",")
                MyFile.write(str(stations_dict['CAMS1029'][hour])+",")
                MyFile.write(str(stations_dict['CAMS169'][hour])+",")
                MyFile.write(str(stations_dict['CAMS670'][hour])+",")
                MyFile.write(str(stations_dict['CAMS1020'][hour])+",")
                MyFile.write(str(stations_dict['CAMS1049'][hour])+"\n")
               


                            

        MyFile.close()

                        












