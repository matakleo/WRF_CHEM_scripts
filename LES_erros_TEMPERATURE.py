
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2
import glob

# turb_names=['YSU_LES3D_TKE','YSU_SMAG_SMAG','YSU_LES3D_SMAG','YSU_SMAG_TKE','YSU_TKE_SMAG','YSU_TKE_TKE']
turb_names=['YSU_SMAG_SMAG','MYJ_TKE_TKE']

simulations_dir='/Users/lmatak/Downloads/'
real_dir='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data/real_data_per_month/'

def error_func_temp(real_data,sim_data):
    temp_real=[]
    temp_sim=[]
    temp_real.append(Extract_the_shit2(real_data,temp_real,'Temperature'))

    temp_sim.append(Extract_by_name(sim_data,temp_sim,'Temperature'))
    if (sim_data[-7:-4]== 'Jan' or 'Feb' or 'Mar' or 'Dec'):
        temp_sim=temp_sim[6:30]
    else:
        temp_sim=temp_sim[5:29]
    # print(sim_data)
    

    temp_error=0
    for i in range(len(temp_sim)):
        temp_error+=abs(temp_sim[i]-temp_real[i])
    
    
    return temp_error/12
error_temp=[]
real_data = []

whole_year_error_temperature=[]
########## list to hold the wrfout files ##########
for file in glob.glob(real_dir+'all_cams*.csv'):
    real_data.append(file)
real_data.sort()

for turb in turb_names:
    turb_sim_dir=simulations_dir+turb
    # print(turb_sim_dir)
    error_temp=[]
    sim_data=[]
    for file in glob.glob(turb_sim_dir+'/*.csv'):
        sim_data.append(file)
    sim_data.sort()
    for i in range(len(sim_data)):

        error_temp.append(error_func_temp(real_data[i],sim_data[i]))
    # print(np.mean(error_temp))
    whole_year_error_temperature.append(np.mean(error_temp))

plt.bar(turb_names,whole_year_error_temperature)
plt.title('MAE temperature')
plt.show()
