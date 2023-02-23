
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

Output_Dir = '/project/momen/Lmatak/WRF_CHEM/output_files/URBAN_SIMS/Time_Series_Winds/'

PBL="MYJ"
urban='BEM'
#for BEM uncomment this:
#Input_Dir = '/project/momen/Lmatak/WRF_CHEM/SLUCM_SCHEME_RUNS/simulation_runs/'

Input_Dir='/project/momen/Lmatak/WRF_CHEM/SLUCM_SCHEME_RUNS/simulation_runs/'

dir_names=['Default_SLUC','Ustar_10_SLUC','Ustar_20_SLUC','Ustar_5_SLUC' ]#,'WRF_BEM_change_momentum_1.5','WRF_BEM_change_tke_0.5','WRF_BEM_change_tke_1.5','WRF_BEM_change_momentum_0.5']
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
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
            two_same_stations_counter=0
            for measur_station in measuring_stations:
                
                    
                    # wspd is U10 V10 squared at monitoring site
                    wspd=math.sqrt(u10[measur_station]**2+v10[measur_station]**2)
         #           print('at surface wspd is ',float(wspd))
                    #404 19m
                    if measur_station==CAMS404_pos:
                        wspd=getvar(data, "wspd",time_idx)
                        wspd=wspd[0]
                        wspd=wspd[measur_station]*np.log(19/0.14)/np.log(10/0.14)
                    #409 18m
                    elif measur_station==CAMS409_pos:
                        
                        wspd=wspd*np.log(18/0.14)/np.log(10/0.14)
                        #8 24m
                    elif measur_station==CAMS8_pos:
                        wspd=getvar(data, "wspd",time_idx)
                        wspd=wspd[0]
                        wspd=wspd[measur_station]*np.log(24/0.14)/np.log(10/0.14)
                        #603 13m
                    elif measur_station==CAMS603_pos:
                        wspd=wspd*np.log(13/0.14)/np.log(10/0.14)
                        #403 13m
                    elif measur_station==CAMS403_pos:
                        wspd=wspd*np.log(13/0.14)/np.log(10/0.14)
                        #167 7m
                    elif measur_station==CAMS167_pos:
                        wspd=wspd*np.log(7/0.14)/np.log(10/0.14)
                        #1029 7m
                    elif measur_station==CAMS1029_pos:
                        wspd=wspd*np.log(7/0.14)/np.log(10/0.14)
                        #670 10m, although it's at 10m, I put it to 8 so it scales a little due to another stations
                        #at the same elevation, cams 169
                    elif measur_station==CAMS670_pos: 
                        # wspd=wspd*np.log(8/0.14)/np.log(10/0.14)  
                        print(two_same_stations_counter)
                        wspd=math.sqrt(u10[measur_station]**2+v10[measur_station]**2) 
                        two_same_stations_counter+=1
                        if two_same_stations_counter==1:
                        
                            wspd=wspd*np.log(6/0.14)/np.log(10/0.14) 



                        
                        #1020 11m
                    elif measur_station==CAMS1020_pos:
                        wspd=wspd*np.log(11/0.14)/np.log(10/0.14)
                        #1049 20m
                    elif measur_station==CAMS1049_pos:
                        wspd=getvar(data, "wspd",time_idx)
                        wspd=wspd[0]
                        wspd=wspd[measur_station]
                        wspd=wspd*np.log(20/0.14)/np.log(10/0.14)

                   # CAMS 1, 9m elevation
                    elif measur_station==CAMS1_pos:
                        wspd=wspd*np.log(9/0.14)/np.log(10/0.14)

                    # MOODY TOWER, CAMS 695, elevation ~73m
                    elif measur_station==CAMS695_pos:
                        wspd=getvar(data, "wspd",time_idx)
                        wspd= interplevel(wspd, height, 73)
                        wspd=wspd[measur_station]
                    # CAMS 416, at 10m elevation, no changes needed
                    elif measur_station==CAMS416_pos:
                        wspd=wspd
                    # CAMS 53, at 20m elevation
                    elif measur_station==CAMS53_pos:
                        wspd=getvar(data, "wspd",time_idx)
                        wspd=wspd[0]
                        wspd=wspd[measur_station]
                        wspd=wspd*np.log(20/0.14)/np.log(10/0.14)
                #       print('m here at cams 53')
                      
                    # CAMS 169, elevation 6m
                    elif measur_station==CAMS169_pos:
                        wspd=wspd*np.log(6/0.14)/np.log(10/0.14)    
                    # CAMS 1052, at 14m elevation
                    elif measur_station==CAMS1052_pos:

                        wspd=wspd*np.log(14/0.14)/np.log(10/0.14)    

                    # wspd=math.sqrt(u10[measur_station]**2+v10[measur_station]**2)
                    wspd_per_file.append(2.23693629*float(wspd))
                    surface_temperature_per_file.append(float(outdoor_temperature[measur_station]*9/5-459.67))



                    
                    stations_dict[keys_for_dict[stations_counter]].append(2.23693629*float(wspd))
                    stations_counter+=1

            surface_temperature_list.append(np.mean(surface_temperature_per_file))    
            # PM_list.append(np.mean(pm_per_file))  
            # NO_list.append(np.mean(no_per_file))  
            # NO2_list.append(np.mean(no2_per_file))  
            WSPD_list.append(np.mean(wspd_per_file))  


        var=dir_name+"_"+month
        os.chdir(Output_Dir+PBL+"_"+dir_name)
        MyFile=open('%s.csv' %var,'w')
        ##write the var name, top left corner
        MyFile.write ("Urban_schemes_"+str(domain)+ "\n")
        # MyFile.write ("Temperature,PM2_5,NO,NO2,WSPD\n")
        MyFile.write ("Temperature,CAMS404_WSPD,CAMS1052_WSPD,CAMS695_WSPD,CAMS53_WSPD,CAMS409_WSPD,CAMS8_WSPD,CAMS416_WSPD,CAMS1_WSPD,CAMS603_WSPD,CAMS403_WSPD,CAMS167_WSPD,CAMS1029_WSPD,CAMS169_WSPD,CAMS670_WSPD,CAMS1020_WSPD,CAMS1049_WSPD,ALL_CAMS_AVG\n")  
        ##write longitudes in first row
        for hour in range(len(ncfiles)-1):

        ##final longitude, swithc to lower row
                MyFile.write(str(surface_temperature_list[hour])+",")
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
                MyFile.write(str(stations_dict['CAMS1049'][hour])+",")
                MyFile.write(str(WSPD_list[hour])+"\n")


                            

        MyFile.close()

                        












