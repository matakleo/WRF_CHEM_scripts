
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2
import glob

dir='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data_october/'

real_data = []
########## list to hold the wrfout files ##########
for file in glob.glob(dir+'*.csv'):
    real_data.append(file)

nitrix_oxide_list=[]
nitrix_dioxide_list=[]
ozone_list=[]
temperature_list=[]
PM2_5_list=[]
winds_list=[]
print(real_data)
for file in real_data:
    nitrix_oxide=[]
    nitrix_dioxide=[]
    ozone=[]
    temperature=[]
    PM2_5=[]
    winds=[]
    # nitrix_oxide_list.append(Extract_the_shit2(file,nitrix_oxide,'NO'))

    # nitrix_dioxide_list.append(Extract_the_shit2(file,nitrix_dioxide,'NO2'))
    # ozone_list.append(Extract_the_shit2(file,ozone,'O3'))
    temperature_list.append(Extract_the_shit2(file,temperature,'Temperature'))
    # PM2_5_list.append(Extract_the_shit2(file,PM2_5,'PM2.5'))
    winds_list.append(Extract_the_shit2(file,winds,'WSPD'))
# print(temperature_list)
    
# # nitrix_oxide_list=np.array(nitrix_oxide_list)
# # nitrix_dioxide_list=np.array(nitrix_dioxide_list)
temperature_list=np.array(temperature_list)
# # PM2_5_list=np.array(PM2_5_list)
# # ozone_list=np.array(ozone_list)
winds_list=np.array(winds_list)

print(temperature_list)
fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(17,8)) 

# # axes[0,0].plot(nitrix_oxide_list.mean(axis=0)[6:11],label='obs data',color='black')
# # axes[0,0].set_title('NO in ppm')
# # axes[0,1].plot(nitrix_dioxide_list.mean(axis=0)[6:11],label='obs data',color='black')
# # axes[0,1].set_title('NO2 in ppm')
axes[0].plot(temperature_list.mean(axis=0)[:-27],label='obs data',color='black')
axes[0].set_title('Temperature in Farenheit')
# # axes[1,1].plot(PM2_5_list.mean(axis=0)[6:11],label='obs data',color='black')
# # axes[1,1].set_title('PM2_5 ug/m^3')
# # axes[2,0].plot(ozone_list.mean(axis=0)[6:11],label='obs data',color='black')
# # axes[2,0].set_title('Ozone in ppm')
axes[1].plot(winds_list.mean(axis=0)[:-27],label='obs data',color='black')
axes[1].set_title('winds mph')



sim_pm_25=[]
sim_temp=[]
sim_no=[]
sim_no2=[]
sim_wspd=[]
sim_o3=[]


dom_avg_sim_pm_25=[]
dom_avg_sim_temp=[]
dom_avg_sim_no=[]
dom_avg_sim_no2=[]
dom_avg_sim_wspd=[]
dom_avg_sim_o3=[]

sim_file='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_LES_data/Hourly_LES_outputs_domain_3_oct_feedback.csv'
# # sim_pm_25=Extract_by_name(sim_file,sim_pm_25,"PM2_5")
sim_temp=Extract_by_name(sim_file,sim_temp,"Temperature")
# # sim_no=Extract_by_name(sim_file,sim_no,"NO")
# # sim_no2=Extract_by_name(sim_file,sim_no2,"NO2")
sim_wspd=Extract_by_name(sim_file,sim_wspd,"WSPD")
# # sim_o3=Extract_by_name(sim_file,sim_o3,"O3")

# dom_avg_sim_pm_25=Extract_by_name(sim_file,dom_avg_sim_pm_25,"dom_avg_PM2_5")
dom_avg_sim_temp=Extract_by_name(sim_file,dom_avg_sim_temp,"dom_avg_Temperature")
# dom_avg_sim_no=Extract_by_name(sim_file,dom_avg_sim_no,"dom_avg_NO")
# dom_avg_sim_no2=Extract_by_name(sim_file,dom_avg_sim_no2,"dom_avg_NO2")
dom_avg_sim_wspd=Extract_by_name(sim_file,dom_avg_sim_wspd,"dom_avg_WSPD")
# dom_avg_sim_o3=Extract_by_name(sim_file,dom_avg_sim_o3,"dom_avg_O3")
print(dom_avg_sim_temp)

# # axes[0,0].plot(sim_no,label='stations avg',color='green')
# # axes[0,1].plot(sim_no2,label='stations avg',color='green')
axes[0].plot(sim_temp,label='stations avg',color='green')
# # axes[1,1].plot(sim_pm_25,label='stations avg',color='green')
# # axes[2,0].plot(sim_o3,label='stations avg',color='green')
axes[1].plot(sim_wspd,label='stations avg',color='green')
# print(dom_avg_sim_no)
# # axes[0,0].plot(dom_avg_sim_no,label='domain avg',color='red')
# # axes[0,1].plot(dom_avg_sim_no2,label='domain avg',color='red')
axes[0].plot(dom_avg_sim_temp,label='domain avg',color='red')
# # axes[1,1].plot(dom_avg_sim_pm_25,label='domain avg',color='red')
# # axes[2,0].plot(dom_avg_sim_o3,label='domain avg',color='red')
axes[1].plot(dom_avg_sim_wspd,label='domain avg',color='red')
hours=np.arange(0,100,12)
axes[1].set_xticks(hours)
axes[0].set_xticks(hours)
axes[0].set_xticklabels(['midnight','noon','midnight','noon','midnight','noon','midnight','noon','midnight'])
axes[0].grid(axis='x')
axes[1].set_xticklabels(['midnight','noon','midnight','noon','midnight','noon','midnight','noon','midnight'])
axes[1].grid(axis='x')  
# axes[1].set_xticklabels([0,1,2])
plt.legend()

plt.show()