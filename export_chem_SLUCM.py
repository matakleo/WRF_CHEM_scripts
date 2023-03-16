
from audioop import avg
from netCDF4 import Dataset
from numpy.core.fromnumeric import shape, size, transpose
from wrf import getvar,interplevel,latlon_coords,rh,tk
import numpy as np
import math
import csv
import os

from xarray import Coordinate
from all_functions import list_ncfiles, create_file
import glob

#check the output folder!!!!
Output_Dir = '/project/momen/Lmatak/WRF_CHEM/output_files/CHEM_TIME_SERIES/'

#what you wanna get:?
#at what altitude?
alt=28

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

stations_dict={}
### these are only the ones with chem###
# keys_for_dict = ['CAMS1052','CAMS695','CAMS53','CAMS409','CAMS416','CAMS8','CAMS1','CAMS603','CAMS403']
# measuring_stations=[CAMS1052_pos,CAMS695_pos,CAMS53_pos,CAMS409_pos,CAMS416_pos,CAMS8_pos,CAMS1_pos,CAMS603_pos,CAMS403_pos,]

###these are all####
measuring_stations=[CAMS404_pos,CAMS1052_pos,CAMS695_pos,CAMS53_pos,CAMS409_pos,CAMS8_pos,CAMS416_pos,CAMS1_pos,\
    CAMS603_pos,CAMS403_pos,CAMS167_pos,CAMS1029_pos,CAMS169_pos,CAMS670_pos,CAMS1020_pos,CAMS1049_pos] 

keys_for_dict = ['CAMS404','CAMS1052','CAMS695','CAMS53','CAMS409','CAMS8','CAMS416','CAMS1','CAMS603','CAMS403','CAMS167','CAMS1029',\
    'CAMS169','CAMS670','CAMS1020','CAMS1049']


keys_for_chems=['WSPD','temperature','pm25','ozone','nitric_oxide','nitrogen_dioxide','carbon_monoxide','relative_humidity','PBLH']

months=['Jan','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
urb_dirs=['SLUC_ust10']


time_idx=0

ncfiles = []

#name of the excel output file#
#var="pbl_pbl_LES_chem_d"+str(domain)
########## list to hold the wrfout files ##########


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

for month in months:

    for urb in urb_dirs:
        # clean it every time, ncfiles
        ncfiles=[]
        Input_Dir='/project/momen/Lmatak/WRF_CHEM/C_RUNS_SLUC/'+month+'_'+urb+'/'
        
        #Input_Dir='/project/momen/Lmatak/WRF_CHEM/C_RUNS_SLUC/'+month+'_'+urb+'/'
        
        os.chdir(Input_Dir)

        for file in glob.glob(Input_Dir+'wrfout_d0'+str(domain)+'*'):
            ncfiles.append(file)
        ncfiles.sort()
        #initialize the dictionary with each station having each of the chems as empty lists, double nested   
        for d in keys_for_dict:
            # print('d',d)
            stations_dict[d]={}
            for c in keys_for_chems:
                # print('c',c)
            
                stations_dict[d][c]=[]

        for ncfile in ncfiles:
            print('workin on: ',ncfile)
            # surface_temperature_per_file=[]
            # pm_per_file=[]
            # no_per_file=[]
            # no2_per_file=[]
            # wspd_per_file=[]
            # ozone_per_file=[]


            ########## load the data ##########
            data = Dataset(ncfile)

            height = getvar(data, "height_agl",time_idx)

            carbon_monoxide=getvar(data, "co",time_idx)
            carbon_monoxide=carbon_monoxide[0]

            #chem variabsl#
            pm_2_5 = getvar(data, "PM2_5_DRY",time_idx)
            pm_2_5=pm_2_5[0]

            qv=getvar(data,"Q2",time_idx)


            Pressure=getvar(data,"PSFC",time_idx)

            pm10 = getvar(data, "PM10",time_idx)
            pm10=pm10[0]
            
            ozone=getvar(data, "o3",time_idx)
            ozone=ozone[0]

            PBLH=getvar(data,'PBLH',time_idx)

            nitric_oxide=getvar(data, "no",time_idx)
            nitric_oxide=nitric_oxide[0]

            nitric_dioxide=getvar(data, "no2",time_idx)
            nitric_dioxide=nitric_dioxide[0]
            #met variabls#

            u10=getvar(data, "U10",time_idx)
            v10=getvar(data, "V10",time_idx)
            outdoor_temperature=getvar(data, "T2",time_idx)
            stations_counter=0
            two_same_stations_counter=0
            #rel hum calculation
            rel_hum=rh(qv,Pressure,outdoor_temperature)

            for measur_station in measuring_stations:

                wspd=math.sqrt(u10[measur_station]**2+v10[measur_station]**2)

                ##station based wspd##
                
                    
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
                    qv=getvar(data,"QVAPOR",time_idx)
                    qv=interplevel(qv,height,73)

                    Pressure=getvar(data,"P",time_idx)
                    Pressure=interplevel(Pressure,height,73)

                    potential_temp=getvar(data, "T",time_idx)
                    potential_temp=interplevel(potential_temp,height,73)

                    temperature=tk(Pressure,potential_temp,meta=True, units='K')

                    rel_hum=rh(qv,Pressure,temperature)


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

                PBLH=PBLH[measur_station]

                pm_per_file=(float(pm_2_5[measur_station]))
                pm10_per_file=(float(pm10[measur_station]))
            #     ##1000 multiplier to go from ppm to ppb
                no_per_file=(1000*float(nitric_oxide[measur_station]))
                no2_per_file=(1000*float(nitric_dioxide[measur_station]))
                ozone_per_file=(1000*float(ozone[measur_station]))
                # print('ozone',1000*float(ozone[measur_station]))
                wspd_per_file=(2.23693629*float(wspd))
                ## CO IS WRONG!!!
                carbon_monoxide_per_file=(1000*float(carbon_monoxide[measur_station]))

                surface_temperature_per_file=(float(outdoor_temperature[measur_station]*9/5-459.67))
# keys_for_chems=['WSPD','pm25','ozone','nitric_oxide','nitrogen_dioxide','carbon_monoxide']
                # print('this is dict val',stations_dict[keys_for_dict[stations_counter]]['WSPD'])
                stations_dict[keys_for_dict[stations_counter]]['WSPD'].append(wspd_per_file)
                stations_dict[keys_for_dict[stations_counter]]['temperature'].append(surface_temperature_per_file)
                stations_dict[keys_for_dict[stations_counter]]['pm25'].append(pm_per_file)
                stations_dict[keys_for_dict[stations_counter]]['relative_humidity'].append(float(rel_hum[measur_station]))
                stations_dict[keys_for_dict[stations_counter]]['ozone'].append(ozone_per_file)
                stations_dict[keys_for_dict[stations_counter]]['nitric_oxide'].append(no_per_file)
                stations_dict[keys_for_dict[stations_counter]]['nitrogen_dioxide'].append(no2_per_file)
                stations_dict[keys_for_dict[stations_counter]]['carbon_monoxide'].append(carbon_monoxide_per_file)
                stations_dict[keys_for_dict[stations_counter]]['PBLH'].append(PBLH)



                stations_counter+=1
       
    # print(stations_dict[d])


                 ##############################
                # Exporting the simulated data #
                ##############################
        print('##########################################################################################')
        print('                                   FINISHED EXTRACTION!')
        print('##########################################################################################')


        ########### create the output file      ###################
        ######################################
        create_file (Output_Dir,urb)
        var=urb+'_'+month
        print('var',var)
        # Path = os.getcwd()
        os.chdir(Output_Dir+'/'+urb)
        MyFile=open('%s.csv' %var,'w')
        ##write the var name, top left corner
        MyFile.write (var+ "\n")
        # MyFile.write ("Temperature,PM2_5,NO,NO2,WSPD\n")
        # MyFile.write ("pm25,nitric_oxide,nitrogen_dioxide,ozone,dom_avg_pm25,dom_avg_no,dom_avg_no2,dom_avg_ozone,wind,Temperature,dom_avg_Temperature,dom_avg_WSPD\n")
        
        for d in keys_for_dict:
            for c in keys_for_chems:
                MyFile.write((d+'_'+c)+",")
                # print(d+'_'+c)
        MyFile.write("\n")
        # print('ncfiles len',len(ncfiles))
        for hour in range(len(ncfiles)-1):
            for d in keys_for_dict:
                for c in keys_for_chems:
                    # print('hour',hour,'station',d,'compound',c)
                    MyFile.write(str(stations_dict[d][c][hour])+",")
            MyFile.write("\n")        
                             
        MyFile.close()
