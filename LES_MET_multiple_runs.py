
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2
import glob

dir='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data/'

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
# print(real_data)
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

temperature_list=np.array(temperature_list)
winds_list=np.array(winds_list)


# print(temperature_list)
fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(17,8)) 




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

# sim_file='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_LES_data/Hourly_LES_outputs_domain_3_april_feedback.csv'
sim_filez_dir='/Users/lmatak/Downloads/test_domain/'
sim_filez=[]
labels=['']
for file in glob.glob(sim_filez_dir+'*.csv'):
    sim_filez.append(file)
for file in sim_filez:

    sim_temp=[]
    sim_wspd=[]
    sim_temp=Extract_by_name(file,sim_temp,"Temperature")
    # print('sim temp lengt ',len(sim_temp))
    sim_wspd=Extract_by_name(file,sim_wspd,"WSPD")
    
    dom_avg_sim_temp=Extract_by_name(file,dom_avg_sim_temp,"dom_avg_Temperature")

    dom_avg_sim_wspd=Extract_by_name(file,dom_avg_sim_wspd,"dom_avg_WSPD")

    print(file[-22:-6])
    axes[0].plot(sim_temp[5:],label=file[-22:-6],linewidth='3') #,color='green')
    axes[1].plot(sim_wspd[5:],linewidth='3') #,color='green')


    
    # hours=np.arange(0,100,12)
    # axes[1].set_xticks(hours)
    # axes[0].set_xticks(hours)
    # axes[0].set_xticklabels(['midnight','noon','midnight','noon','midnight','noon','midnight','noon','midnight'])
    # axes[0].grid(axis='x')
    # axes[1].set_xticklabels(['midnight','noon','midnight','noon','midnight','noon','midnight','noon','midnight'])
    # axes[1].grid(axis='x')  
    # axes[1].set_xticklabels([0,1,2])
print('temppppp is: ')
print('temppppp is: ',temperature_list.mean(axis=0))
axes[0].plot(temperature_list.mean(axis=0)[:len(sim_wspd)-5],label='obs data',color='black')
axes[0].set_title('Temperature in Farenheit')
axes[1].plot(winds_list.mean(axis=0)[:len(sim_wspd)-5],color='black')
axes[1].set_title('winds mph')

fig.legend()

plt.show()