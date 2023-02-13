
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2,create_file
import os


months=['Jan','Feb','Mar','Apr','May','Jun'] #,'Jul','Aug','Sep','Oct','Nov','Dec']

real_dir='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data/real_data_per_month/'
stations=['CAMS1','CAMS35','CAMS55','CAMS416','CAMS695']

temp_list=[]
wspd_list=[]
# second_list_temp=[]
# second_list_wspd=[]

for month in months:
    second_list_temp=[]
    second_list_wspd=[]
    for station in stations:
        processing_data=real_dir+station+'_'+month+'.csv'
        temp_list=(Extract_the_shit2(processing_data,temp_list,'Temperature'))
        wspd_list=(Extract_the_shit2(processing_data,wspd_list,'WSPD'))
        second_list_temp.append(temp_list)
        second_list_wspd.append(wspd_list)
        temp_list=[]
        wspd_list=[]

    temperatures=list(np.mean(second_list_temp,axis=0))
    winds=list(np.mean(second_list_wspd,axis=0))
    

    print(month+' avg temp: ',np.mean(second_list_temp))


    ########## create the output file      ###################
#####################################
    os.chdir(real_dir)
    var='all_cams_'+month
    MyFile=open('%s.csv' %var,'w')

    # MyFile.write ("Temperature,PM2_5,NO,NO2,WSPD\n")
    MyFile.write ("Temperature,WSPD,\n")


    for i in range(len(temperatures[0])):

            MyFile.write(str(temperatures[0][i])+",")
            MyFile.write(str(winds[0][i])+",\n")

                        

    MyFile.close()


