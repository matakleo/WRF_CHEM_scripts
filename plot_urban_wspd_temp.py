
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2
import glob

urban_names=['BEM','WRF_BEM_cd_0.5','WRF_BEM_cd_2.0']
PBLS=["MYJ"]
simulations_dir='/Users/lmatak/Downloads/URBAN_TIME_SERIES_MAE/'
real_dir='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data/real_data_per_month/'


# months=['Jan','Feb']#,'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
months=['May','Jun']#,'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(16,10)) 

real_data = []

row=0
col=0


for month in months:
 
    first_num=0
    last_num=first_num+24
    last_num=-1
    for PBL in PBLS:

        for urban in urban_names:
            print(urban)
            if urban!='BEM' and PBL=='BouLac':continue
            if urban=='YSU_SLUCM_Default':
                urban_sim_dir=simulations_dir+"/"+urban+'/'
                sim_data=urban_sim_dir+"SLUCM_Default_"+month+'.csv'
            else:
                urban_sim_dir=simulations_dir+"/MYJ_"+urban+'/'
                sim_data=urban_sim_dir+urban+"_"+month+'.csv'
            # print()
            temp_sim=[]
            wspd_sim=[]
            
            # print(sim_data)

  
            temp_sim=Extract_by_name(sim_data,temp_sim,'Temperature')
            wspd_sim=Extract_by_name(sim_data,wspd_sim,'WSPD')
            temp_sim=temp_sim[first_num:]

            wspd_sim=wspd_sim[first_num:]
            # if month == 'Feb' and urban=='BEP':
            #     continue
            axes[row,col].plot(np.arange(0,len(temp_sim),1),temp_sim,linewidth=2,)
            axes[row,col+1].plot(np.arange(0,len(wspd_sim),1),wspd_sim,label=urban,linewidth=2,)



        ### THIS IS FOR CALCULATION, THE UPPER PART IS ONLY PLOTTING###
    if (month == 'Jan' or month =='Feb' or month =='Mar' or month =='Nov' or month =='Dec'):
        first_num=6
    else:
        first_num=5   

    temp_real=[]
    wspd_real=[]
    real_data=real_dir+'all_cams_'+month+'.csv'

    temp_real=Extract_the_shit2(real_data,temp_real,'Temperature')
    wspd_real=Extract_the_shit2(real_data,wspd_real,'WSPD')
    # print(len(temp_real))

    axes[row,col].plot(np.arange(first_num,first_num+24,1),temp_real,linewidth=3,color='black')
    axes[row,col+1].plot(np.arange(first_num,first_num+24,1),wspd_real,linewidth=3,color='black')
        
    axes[row,col].set_title('temperature timeseries - '+month)
    axes[row,col+1].set_title('wspd timeseries - '+month)
    corel_temp=np.corrcoef(temp_sim[first_num:first_num+24],temp_real)
    axes[row,col].annotate(corel_temp[0,1],[5,60],size=14)
    corel=np.corrcoef(wspd_sim[first_num:first_num+24],wspd_real)
    axes[row,col+1].annotate(corel[0,1],[5,8],size=14)

    axes[row,col].axvline(first_num,color='red')
    axes[row,col].axvline(first_num+23,color='red')

    axes[row,col+1].axvline(first_num,color='red')
    axes[row,col+1].axvline(first_num+23,color='red')

    row+=1

    print('REAL DATA:',real_data)

# plt.legend(['BEM','cd_2.0'])
plt.legend()
plt.show()
