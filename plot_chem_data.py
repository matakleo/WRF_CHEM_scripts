
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2
import glob
import os
import pandas as pd


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
    mae = sum(abs(s - r) for s, r in zip(simulation, real)) / len(simulation)
    return mae

def get_real_data_chem(cams_station,month,chem_name):
    os.chdir('/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/')
    df = pd.read_excel('/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/'+cams_station+'_whole_year_'+chem_name+'.xlsx')
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




fig, axes = plt.subplots(nrows=3, ncols=2,figsize=(17,8)) 
fig.subplots_adjust(hspace=0.5)
row=0
col=0
#REAL DATA


real_data_vars_to_plot=["pm25","nitric_oxide","nitrogen_dioxide","wind","ozone"]

CAMS='CAMS8'
    


## SIM DATA ##
sim_dir='/Users/lmatak/Downloads/WRF_CHEM_TIME_SERIES/'
sim_files=[]
for file in glob.glob(sim_dir+'*.csv'):
    sim_files.append(file)
sim_files.sort()
print(sim_files)

##PLOTTING ##
sims_to_plot=['BEM','No_URB','SLUC'] #,'without_dry_dep',]
vars_to_plot=real_data_vars_to_plot


dict_for_error_sims={}
dict_for_error_real={}


sim_file_number=0
for sim_file in sim_files:
    print(sim_file)
    for tmp_var in vars_to_plot:

        
        
        tmp_list=[]
        tmp_list=Extract_by_name(sim_file,tmp_list,CAMS+'_'+tmp_var)


        # tmp_list=tmp_list[5:-2]

        if tmp_var in dict_for_error_sims:
            dict_for_error_sims[tmp_var].append(tmp_list)
        else:
            dict_for_error_sims[tmp_var]=[]
            dict_for_error_sims[tmp_var].append(tmp_list)


        print(len(tmp_list))    
        axes[row,col].plot(tmp_list,label=sims_to_plot[sim_file_number])
        axes[row,col].set_title(tmp_var)
        axes[row,col].set_xticks(ticks=np.arange(0,72,4))
        axes[row,col].set_xticklabels(np.arange(0,72,4))
        print('row',row,'col',col)
        col+=1
        if col==2:
            row+=1
            col=0
        if row==2 and col==1:
            row=0
            col=0
            sim_file_number+=1




print(dict_for_error_sims.keys())
# calculate_mae


for real_data_var in real_data_vars_to_plot:
    print('real data var',real_data_var)
    try:
        tmp_list=[]
        tmp_list=get_real_data_chem(CAMS,'Jun',real_data_var)

        a=check_numbers(tmp_list)
        tmp_list[a]=None


        axes[row,col].plot(tmp_list,label='OBS data', linewidth=3,color='black')
        print(real_data_var)
        col+=1
        if col==2:
            row+=1
            col=0
        if row==2 and col==1:
            row=0
            col=0
            sim_file_number+=1  
        # print(len(tmp_list.tolist()))
        # print(len(dict_for_error_sims[real_data_var][0]))
        # print(calculate_mae(dict_for_error_sims[real_data_var][0],tmp_list.tolist()))

        
    except:
        col+=1
        if col==2:
            row+=1
            col=0
        if row==2 and col==1:
            row=0
            col=0
            sim_file_number+=1   


fig.suptitle(CAMS,size=20)
fig.legend(['BEM','No_URB','SLUCM'])
plt.show()