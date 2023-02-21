
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2
import glob
import os
import pandas as pd

urban_names=['MYJ_Ustar_20_SLUC','MYJ_Default_SLUC']
PBLS=["MYJ"]
simulations_dir='/Users/lmatak/Downloads/URBAN_TIME_SERIES_MAE/'

real_dir='/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/'

def moving_average(arr, window_size):
    """
    Calculates the moving average of an array with a given window size.
    """
    weights = np.repeat(1.0, window_size) / window_size
    ma = np.convolve(arr, weights, 'valid')
    return ma

# Example usage:

def check_numbers(lst):
    indices = []
    for index, item in enumerate(lst):
        if not isinstance(item, (int, float)):
            indices.append(index)
    return indices

def calculate_mae(simulation, real):
    """
    Calculates the mean absolute error between simulation and real data

    Parameters:
        simulation (list): A list of simulated data
        real (list): A list of real data

    Returns:
        mae (float): The mean absolute error
    """
    error=0
    count=0

    for index, a in enumerate(real):
        # print(index,a)
        if index in check_numbers(real):
            # print('Im skipping?')
            continue
        p = simulation[index]
        error += abs(a - p)
        count += 1

        if count==0:
            return
    return error / count



def get_real_data(cams_station,month):
    os.chdir('/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/')
    df = pd.read_excel('/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/'+cams_station+'_whole_year_wind.xlsx')
    # date_to_plot = ' 2019-01-01 00:00:00'
    df['Date'] = pd.to_datetime(df['Date'])
    # Set the date column as the index of the DataFrame
    df = df.set_index('Date')
    # Specify the date for which you want to retrieve data
   
    if month =='Jan':
        month_num='01'
    elif month=='Feb':
        month_num='02'
    elif month=='Mar':
        month_num='03'
    elif month=='Apr':
        month_num='04'
    elif month=='May':
        month_num='05'
    elif month=='Jun':
        month_num='06'
    elif month=='Jul':
        month_num='07'
    elif month=='Aug':
        month_num='08'
    elif month=='Sep':
        month_num='09'
    elif month=='Oct':
        month_num='10'
    elif month=='Nov':
        month_num='11'
    elif month=='Dec':
        month_num='12'

    target_date = '2019-'+month_num+'-01'
    target_date2= '2019-'+month_num+'-02'
    target_date3='2019-'+month_num+'-03'

    # Retrieve data for the target date
    # target_data = np.array(df.loc[target_date],df.loc[target_date2]df.loc[target_date3])

    col1 = np.array(df.loc[target_date])
    col2 = np.array(df.loc[target_date2])
    col3 = np.array(df.loc[target_date3])

    target_data=(np.concatenate((col1,col2,col3),axis=0))
    # # Concatenate the columns into one DataFrame


    return target_data






# months=['Jan','Feb']#,'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# months=['Jan','Feb','Mar','Apr','May','Jun']
months=['Jul','Aug','Sep','Oct','Nov','Dec']

fig, axes = plt.subplots(nrows=2, ncols=3,figsize=(16,10)) 

real_data = []

row=0
col=0
for_mae=[]
cams='CAMS416_WSPD'

for month in months:
        real_winds=get_real_data(cams[0:-5],month)
        # axes[row,col].plot(moving_average(real_winds,6),label='obs',linewidth=3,color='black')
        axes[row,col].plot(moving_average(real_winds,6),label='obs',linewidth=3,color='black')
        for urban in urban_names:
            print(urban)

            sim_data=simulations_dir+'/'+urban+'/'+urban[4:]+"_"+month+'.csv'
            # print()
            temp_sim=[]
            wspd_sim=[]
            
            # print(sim_data)

  
            temp_sim=Extract_by_name(sim_data,temp_sim,'Temperature')
            wspd_sim=Extract_by_name(sim_data,wspd_sim,cams)

            if (month== 'Jan' or month=='Feb' or month=='Mar' or month=='Dec'):

                wspd_sim=wspd_sim[6:]
            else:

                wspd_sim=wspd_sim[5:-1]
            

            # if month == 'Feb' and urban=='BEP':
            #     continue
            # print(real_winds,wspd_sim)
            for_mae.append(calculate_mae(wspd_sim,real_winds))
            # axes[row,col].plot(moving_average(wspd_sim,6),label=urban[4:],linewidth=2,)
            axes[row,col].plot(moving_average(wspd_sim,6),label=urban[4:],linewidth=2,)

            axes[row,col].set_title(month)

        col+=1
        if col==3:
            row=1
            col=0


        ### THIS IS FOR CALCULATION, THE UPPER PART IS ONLY PLOTTING###
    

            # print('REAL DATA:',real_data)

# plt.legend(['BEM','cd_2.0'])
print(np.mean(for_mae))
fig.suptitle(cams,size=20)

# plt.bar(['wrf','log'],[2.827,2.9043])
plt.legend()
plt.show()
