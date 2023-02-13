
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2
import glob

# turb_names=['YSU_LES3D_TKE','YSU_SMAG_SMAG','YSU_LES3D_SMAG','YSU_SMAG_TKE','YSU_TKE_SMAG','YSU_TKE_TKE']
# urb_names=['MYJ_BEM','MYJ_BEP','MYJ_NO_URBAN','MYJ_SLUCM']
# urb_names=['MYJ_NO_URBAN','MYJ_BEM','MYJ_SLUCM','MYJ_WRF_BEM_change_momentum_0.1','MYJ_WRF_BEM_change_momentum_0.2','MYJ_WRF_BEM_change_momentum_0.5','MYJ_WRF_BEM_change_momentum_1.5','MYJ_WRF_BEM_change_momentum_5','MYJ_WRF_BEM_change_momentum_10',\
#     'MYJ_decreased_building','MYJ_increased_building_heights','MYJ_WRF_BEM_cd_0.25','MYJ_WRF_BEM_cd_0.5','MYJ_WRF_BEM_cd_2.0','MYJ_WRF_BEM_cd_4.0']
# urb_names=['MYJ_BEM','MYJ_WRF_BEM_change_tke_0.01','MYJ_WRF_BEM_change_tke_100','MYJ_WRF_BEM_ustar_0.1_in_NOAHDRV','MYJ_WRF_BEM_ustar_10_in_NOAHDRV']

urb_names=['MYJ_NO_URBAN','MYJ_BEM','MYJ_SLUCM','MYJ_WRF_LES_NO_URB','MYJ_SLUCM_USTAR_10'] #,'MYJ_SLUCM_z0_0.001','MYJ_SLUCM_USTAR_0.1','MYJ_SLUCM_USTAR_10','MYJ_SLUCM_USTAR_100']



# names=['no_urb','BEM','SLUC','mom_0.1','mom_0.2','mom_0.5','mom_1.5','mom_5.0','mom_10','decr_build','incr_build','cd_0.25','cd_0.5',\
#     'cd_2.0','cd_4.0'] #,'ust_0.0001']
# names=['No Urb','BEM','SLUC','LES_NO_URB','MYJ_SLUCM_z0_0.001','MYJ_SLUCM_USTAR_0.1','MYJ_SLUCM_USTAR_10','MYJ_SLUCM_USTAR_100']
names=['No_Urb','BEM','SLUC','LES','SLUC_ust_10']
show='WSPD' #or Temperature or WSPD
months=['Jan','Feb','Mar','Apr','May','Jun'] #,'Jul','Aug','Sep','Oct','Nov','Dec']

simulations_dir='/Users/lmatak/Downloads/URBAN_TIME_SERIES_MAE/older_1_day_runs/'
real_dir='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data/real_data_per_month/'

def error_func_wspd(real_data,sim_data): 
    wspd_sim=[]
    wspd_real=[]
    wspd_real=(Extract_the_shit2(real_data,wspd_real,show))
    wspd_sim=(Extract_by_name(sim_data,wspd_sim,show))
    if (sim_data[-7:-4]== 'Jan' or sim_data[-7:-4]=='Feb' or sim_data[-7:-4]=='Mar' or sim_data[-7:-4]=='Dec'):

        wspd_sim=wspd_sim[6:30]
    else:

        wspd_sim=wspd_sim[5:29]




    temp_error=0

    for i in range(len(wspd_sim)):
        temp_error+=abs(wspd_sim[i]-wspd_real[i])
    
    
    return temp_error/len(wspd_real)

def correlation_coef(real_data,sim_data): 
    wspd_sim=[]
    wspd_real=[]
    wspd_real=(Extract_the_shit2(real_data,wspd_real,show))
    wspd_sim=(Extract_by_name(sim_data,wspd_sim,show))
    if (sim_data[-7:-4]== 'Jan' or sim_data[-7:-4]=='Feb' or sim_data[-7:-4]=='Mar' or sim_data[-7:-4]=='Dec'):

        wspd_sim=wspd_sim[6:30]
    else:
        
        wspd_sim=wspd_sim[5:29]
    # if sim_data[-7:-4]== 'Jan':
        # print(wspd_real)
    corr_coef=np.corrcoef(wspd_sim,wspd_real)

    print('for ',(sim_data[-7:-4]),'coeff is',corr_coef[0,1])
    return corr_coef


error_wspd=[]
real_data = []
month_counter=0
whole_year_error_wspd=[]
########## list to hold the wrfout files ##########
bar_counter=0

all_corr_coeffs=[]


for urb in urb_names:
    real_data=[]
    corelation_coeff=0
    month_counter=0
    sim_data=[]
    turb_sim_dir=simulations_dir+urb
    for file in glob.glob(turb_sim_dir+'/*.csv'):
            sim_data.append(file)
    sim_data.sort()
    

    for file in glob.glob(real_dir+'all_cams_*.csv'):
            real_data.append(file)
    real_data.sort()
  
    error_wspd=0  
    for month in months:
        print(real_data[month_counter])
        print(sim_data[month_counter])
        # print('calculating for '+real_data[month_counter],sim_data[month_counter])
        # error_wspd.append(error_func_wspd(real_data[month_counter],sim_data[month_counter]))
        error_wspd+=error_func_wspd(real_data[month_counter],sim_data[month_counter])/len(months)
        corr_coef=correlation_coef(real_data[month_counter],sim_data[month_counter])

       
        corelation_coeff+=corr_coef[0,1]
        print(corelation_coeff)
        month_counter+=1
        # print(error_wspd)
        # print(np.mean(error_temp))
        
    # print(error_wspd)
    to_write_on_plot=("%.2f" % (corelation_coeff/len(months)))
    all_corr_coeffs.append(corelation_coeff/len(months))
    # plt.annotate(to_write_on_plot,[bar_counter,error_wspd+0.1])
    # print(bar_counter,error_wspd+0.5)
    # print(corelation_coeff/len(months))
    bar_counter+=1
    whole_year_error_wspd.append((error_wspd))


plt.axhline(y = whole_year_error_wspd[0], color = 'r', linestyle = '-')
plt.axhline(y = whole_year_error_wspd[1], color = 'g', linestyle = '--')
# plt.bar(np.arange(0,len(whole_year_error_wspd),1),whole_year_error_wspd)
plt.bar(names,whole_year_error_wspd)
plt.title('MAE '+show)

plt.show()
    