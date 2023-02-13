
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2
import glob

# turb_names=['MYJ_SMAG_SMAG','YSU_LES3D_TKE','YSU_SMAG_SMAG','YSU_LES3D_SMAG','YSU_SMAG_TKE','YSU_TKE_SMAG','YSU_TKE_TKE']
turb_names=['YSU_SMAG_SMAG','MYJ_TKE_TKE']
# months=['Jan','Feb','Mar','Jun']
# months=['May','Jun','Jul','Aug']
months=['Jan','Apr','Jul','Nov']
simulations_dir='/Users/lmatak/Downloads/'
real_dir='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data/real_data_per_month/'
first_num=5
last_num=first_num+24

fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(17,8)) 



real_data = []

whole_year_error_temperature=[]
row=0
col=0
for month in months:
    if (month == 'Jan' or 'Feb' or 'Mar' or 'Nov' or 'Dec'):
        first_num=6
    else:
        first_num=5
    last_num=first_num+24
    temp_real=[]
    real_data=real_dir+'all_cams_'+month+'.csv'
    temp_real=Extract_the_shit2(real_data,temp_real,'WSPD')
    print(temp_real)

    axes[row,col].plot(np.arange(0,24,1),temp_real,label='Real Data',linewidth=3,color='black')
    for turb in turb_names:
        turb_sim_dir=simulations_dir+turb
        temp_sim=[]
        
        sim_data=turb_sim_dir+'/'+turb+'_'+month+'.csv'
        temp_sim=Extract_by_name(sim_data,temp_sim,'WSPD')
        temp_sim=temp_sim[first_num:last_num]
        axes[row,col].plot(np.arange(0,24,1),temp_sim,label=turb,linewidth=2,)

    axes[row,col].set_title('WSPD timeseries - '+month)

    col+=1
    if col==2:
        row+=1
        col=0

plt.legend()
plt.show()
    