
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
    CAMS1_pos=([64],[73])
    CAMS55_pos=([61],[70])
    CAMS35_pos=([55],[80])
    CAMS695_pos=([59],[63])
    CAMS416_pos=([56],[67])
    CAMS53_pos= ([57],[51])
    CAMS169_pos=([58],[70])
    CAMS1052_pos=([68],[60])

measuring_stations=[CAMS1_pos,CAMS55_pos,CAMS35_pos,CAMS695_pos,CAMS416_pos,CAMS53_pos,CAMS169_pos,CAMS1052_pos]

stations_dict={}



time_idx=0



#check the output folder!!!!

Output_Dir = '/project/momen/Lmatak/WRF_CHEM/output_files/URBAN_SIMS/Time_Series/'

PBL="MYJ"
urban='BEM'
#for BEM uncomment this:
#Input_Dir = '/project/momen/Lmatak/WRF_CHEM/SLUCM_SCHEME_RUNS/simulation_runs/'

Input_Dir='/project/momen/Lmatak/WRF_CHEM/URBAN_SCHEME_RUNS/simulation_runs/'

#dir_names=['Default_BEM','cd_0.5','cd_2.0','cd_3.0','cd_4.0','Decreased_Buildings','Default_No_Urb','Increased_Buildings','Mom_0.2','Mom_5.0','Mom_2.0','Mom_0.5']
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
dir_names=['cd_4.0','Decreased_Buildings','Default_No_Urb','Increased_Buildings','Mom_0.2','Mom_5.0','Mom_2.0','Mom_0.5']
#at what altitude?
alt=50
keys_for_dict = ['CAMS1','CAMS55','CAMS35','CAMS695','CAMS416','CAMS53','CAMS169','CAMS1052']

for dir_name in dir_names:
    ##create file is for creating a directory
    create_file(Output_Dir,PBL+"_"+dir_name)
    for month in months:
       

        stations_dict['CAMS1']=[]
        stations_dict['CAMS55']=[]
        stations_dict['CAMS35']=[]
        stations_dict['CAMS695']=[]
        stations_dict['CAMS416']=[]
        stations_dict['CAMS53']=[]
        stations_dict['CAMS169']=[]
        stations_dict['CAMS1052']=[]


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
        #    print('workin on: ',ncfile)
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
                
                    # wspd is U10 V10 squared at monitoring site
                    wspd=math.sqrt(u10[measur_station]**2+v10[measur_station]**2)
         #           print('at surface wspd is ',float(wspd))

                    # CAMS 1, 9m elevation
                    if measur_station==([64],[73]):
                        wspd=wspd*np.log(9/0.14)/np.log(10/0.14)
                    # CAMS 55, 13m elevation
                    elif measur_station==([61],[70]):
                        wspd=getvar(data, "wspd",time_idx)
                        wspd= interplevel(wspd, height, 13)
                        wspd=wspd[measur_station]
                    # CAMS 35, elevation 6m
                    elif measur_station==([55],[80]):
                        wspd=wspd*np.log(6/0.14)/np.log(10/0.14)
                    # MOODY TOWER, CAMS 695, elevation ~73m
                    elif measur_station==([59],[63]):
                        wspd=getvar(data, "wspd",time_idx)
                        wspd= interplevel(wspd, height, 73)
                        wspd=wspd[measur_station]
                    # CAMS 416, at 10m elevation, no changes needed
                    elif measur_station==([56],[67]):
                        wspd=wspd
                    # CAMS 53, at 20m elevation
                    elif measur_station==([57],[51]):
                        wspd=getvar(data, "wspd",time_idx)
                        wspd= interplevel(wspd, height, 20)
                        wspd=wspd[measur_station]
                    # CAMS 169, elevation 6m
                    elif measur_station==([58],[70]):
                        wspd=wspd*np.log(6/0.14)/np.log(10/0.14)    
                    # CAMS 1052, at 14m elevation
                    elif measur_station==([68],[60]):
                        wspd=getvar(data, "wspd",time_idx)
                        wspd= interplevel(wspd, height, 14)
                        wspd=wspd[measur_station]
                    


                    wspd_per_file.append(2.23693629*float(wspd))
                    surface_temperature_per_file.append(float(outdoor_temperature[measur_station]*9/5-459.67))



                    
                    stations_dict[keys_for_dict[stations_counter]].append(2.23693629*float(wspd))
                    stations_counter+=1

            surface_temperature_list.append(np.mean(surface_temperature_per_file))    
            # PM_list.append(np.mean(pm_per_file))  
            # NO_list.append(np.mean(no_per_file))  
            # NO2_list.append(np.mean(no2_per_file))  
            WSPD_list.append(np.mean(wspd_per_file))  

        print(month)
       # print(stations_dict['CAMS1'])
        var=dir_name+"_"+month
        os.chdir(Output_Dir+PBL+"_"+dir_name)
        MyFile=open('%s.csv' %var,'w')
        ##write the var name, top left corner
        MyFile.write ("Urban_schemes_"+str(domain)+ "\n")
        # MyFile.write ("Temperature,PM2_5,NO,NO2,WSPD\n")

        MyFile.write ("Temperature,CAMS1_WSPD,CAMS55_WSPD,CAMS35_WSPD,CAMS695_WSPD,CAMS416_WSPD,CAMS53_WSPD,CAMS169_WSPD,CAMS1052_WSPD,ALL_CAMS_AVG\n")
        ##write longitudes in first row
        for hour in range(len(ncfiles)-1):

        ##final longitude, swithc to lower row
                MyFile.write(str(surface_temperature_list[hour])+",")
                MyFile.write(str(stations_dict['CAMS1'][hour])+",")
                MyFile.write(str(stations_dict['CAMS55'][hour])+",")
                MyFile.write(str(stations_dict['CAMS35'][hour])+",")
                MyFile.write(str(stations_dict['CAMS695'][hour])+",")
                MyFile.write(str(stations_dict['CAMS416'][hour])+",")
                MyFile.write(str(stations_dict['CAMS53'][hour])+",")
                MyFile.write(str(stations_dict['CAMS169'][hour])+",")
                MyFile.write(str(stations_dict['CAMS1052'][hour])+",")
                # MyFile.write(str(NO_list[hour])+",")
                # MyFile.write(str(NO2_list[hour])+",")
                MyFile.write(str(WSPD_list[hour])+"\n")


                            

        MyFile.close()

                        












