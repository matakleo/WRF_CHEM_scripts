
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from all_functions import Extract_by_name, Extract_the_shit2
import glob
import os
import pandas as pd
fig, axes = plt.subplots(nrows=5, ncols=3,figsize=(16,9),) 



urban_names=['old_WRF_urb_sims_no_chem_MYJ'] #'SLUC_ust10_YSU'] #,'No_Urb_CLDCHEM','No_Urb_CHEM_IN_OPT','No_Urb_IO_STYL','No_Urb_anth']
# urban_names=['NU_MYJ','BEM_MYJ','BEM_MYJ_change_urban',] #'BEM_MYJ','BEM_YSU','No_Urb_old_emiss','SL_MYJ','SL_YSU'] #'SLUC_ust10_YSU'] #,'No_Urb_CLDCHEM','No_Urb_CHEM_IN_OPT','No_Urb_IO_STYL','No_Urb_anth']

PBLS=["MYJ"]
simulations_dir='/Users/lmatak/Downloads/temp_foold/all/URBAN_TIME_SERIES_MAE/'

real_dir='/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/'

def check_longer(sim,real):
    if len(sim)>=len(real):
        a=len(real)
    else:a=len(sim)
    return a

def get_corr_coeff(real_data,sim_data):
    real_data_cleaned=np.copy(real_data)

    string_indices = [i for i, x in enumerate(real_data) if isinstance(x, str)]
    print(string_indices)
    real_data_cleaned[string_indices] = None
    # np.corrcoef(x[mask], y[mask], rowvar=False)[0, 1]
    # real_data=np.ma.masked_invalid(real_data.astype(np.nan))
    # real_data = np.where(mask, np.nan)

    # moving_avg_real = moving_average(real_data_cleaned, 6)

    moving_avg_real = real_data_cleaned

    # print(len(moving_avg_real))
    # print('sim ',simulation_month)
    moving_avg_sim=sim_data


    
    #append the mae seperately to different keys, for each month!
    #this is what will be getting plotted!!
    # error_dict[cams_name_for_real_data].append(mae)

    #for debugging, this print line is very useful
    # print(urban_simulation,month_number,cams_station,mae)

    #calculate the CORRCOEFF
    # ma.corrcoef(ma.masked_invalid(A), ma.masked_invalid(B)))

    p,corr= np.ma.corrcoef((moving_avg_sim, moving_avg_real.tolist()))
    corr=corr[0]

    return corr


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
    real_tmp=np.copy(real)
    sim_tmp=np.copy(simulation)
    real_tmp=real_tmp[0:len(sim_tmp)]

    for index, a in enumerate(real_tmp):
        # print(index,a)
        if index in check_numbers(real_tmp):
            # print('Im skipping?')
            continue
        p = sim_tmp[index]
        error += abs(a - p)
        count += 1

    if count==0:
        return -1
    return error / count



def get_real_data_chem(cams_station,month,chem_name):
    os.chdir('/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/')
    df = pd.read_excel('/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/'+cams_station+'whole_year_'+chem_name+'.xlsx')
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
    # target_date4='2019-'+month_num+'-04'
    # target_date5='2019-'+month_num+'-05'
    # target_date6='2019-'+month_num+'-06'
    # target_date7 = '2019-'+month_num+'-07'
    # target_date8= '2019-'+month_num+'-08'
    # target_date9 = '2019-'+month_num+'-09'
    # target_date10 = '2019-'+month_num+'-10'
    # target_date11= '2019-'+month_num+'-11'
    # target_date12= '2019-'+month_num+'-12'
    # target_date13= '2019-'+month_num+'-13'
    # target_date14= '2019-'+month_num+'-14'
    # target_date15= '2019-'+month_num+'-15'
    # target_date16= '2019-'+month_num+'-16'
    # target_date17= '2019-'+month_num+'-17'
    # target_date18= '2019-'+month_num+'-18'
    # target_date19= '2019-'+month_num+'-19'
    # target_date20= '2019-'+month_num+'-20'


    # Retrieve data for the target date
    # target_data = np.array(df.loc[target_date],df.loc[target_date2]df.loc[target_date3])

    col1 = np.array(df.loc[target_date])
    col2 = np.array(df.loc[target_date2])
    col3 = np.array(df.loc[target_date3])
    # col4 = np.array(df.loc[target_date4])
    # col5 = np.array(df.loc[target_date5])
    # col6 = np.array(df.loc[target_date6])
    # col7 = np.array(df.loc[target_date7])
    # col8 = np.array(df.loc[target_date8])
    # col9 = np.array(df.loc[target_date9])
    # col10 = np.array(df.loc[target_date10])
    # col11 = np.array(df.loc[target_date11])
    # col12 = np.array(df.loc[target_date12])
    # col13 = np.array(df.loc[target_date13])
    # col14 = np.array(df.loc[target_date14])
    # col15 = np.array(df.loc[target_date15])
    # col16 = np.array(df.loc[target_date16])
    # col17 = np.array(df.loc[target_date17])
    # col18 = np.array(df.loc[target_date18])
    # col19 = np.array(df.loc[target_date19])
    # col20 = np.array(df.loc[target_date20])

    target_data=(np.concatenate((col1,col2,col3),axis=0))
    # target_data=(np.concatenate((col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14,col15,col16,col17,col18,col19,col20),axis=0))
    # # Concatenate the columns into one DataFrame


    return target_data




domain=2

# months=['Apr']#,'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# months=['Jul','Aug','Sep','Oct','Nov','Dec']
# months=['Aug','Dec','Jan','Oct','May','Nov']


fig.subplots_adjust(hspace=0.25,bottom=0.1)

real_data = []

dict_for_avgs={}
dict_for_avgs['real_vals']=[]

row=0
col=0
for_mae=[]
# chem_comp='wind'
chem_comp='wind'
month='Aug'


if chem_comp=='ozone':
    cams_stations=['CAMS695_ozone','CAMS53_ozone','CAMS409_ozone','CAMS8_ozone',\
        'CAMS416_ozone','CAMS603_ozone','CAMS1_ozone','CAMS403_ozone','CAMS698_ozone']
elif chem_comp=='nitric_oxide':
    cams_stations=['CAMS1052_nitric_oxide','CAMS53_nitric_oxide','CAMS8_nitric_oxide','CAMS416_nitric_oxide',\
        'CAMS1_nitric_oxide','CAMS603_nitric_oxide','CAMS403_nitric_oxide']
elif chem_comp=='nitrogen_dioxide':
    cams_stations=['CAMS1052_nitrogen_dioxide','CAMS53_nitrogen_dioxide','CAMS8_nitrogen_dioxide','CAMS416_nitrogen_dioxide',\
        'CAMS1_nitrogen_dioxide','CAMS603_nitrogen_dioxide','CAMS403_nitrogen_dioxide']
elif chem_comp=='pm25':
    cams_stations=['CAMS8_pm25','CAMS416_pm25',\
        'CAMS1_pm25','CAMS403_pm25']
elif chem_comp=='carbon_monoxide':
    cams_stations=['CAMS1052_carbon_monoxide','CAMS695_carbon_monoxide',\
        'CAMS403_carbon_monoxide']
elif chem_comp=='relative_humidity':
    cams_stations=['CAMS8_relative_humidity','CAMS416_relative_humidity','CAMS695_relative_humidity',\
        'CAMS403_relative_humidity']
elif chem_comp=='wind':
    cams_stations=['CAMS404_WSPD','CAMS1052_WSPD','CAMS695_WSPD',\
    'CAMS53_WSPD','CAMS409_WSPD','CAMS8_WSPD','CAMS416_WSPD',\
        'CAMS1_WSPD','CAMS603_WSPD','CAMS403_WSPD','CAMS167_WSPD'\
            ,'CAMS1029_WSPD','CAMS169_WSPD','CAMS670_WSPD','CAMS1020_WSPD','CAMS1049_WSPD']
elif chem_comp=='temperature':
    cams_stations=['CAMS1_temperature', 'CAMS404_temperature','CAMS1052_temperature' \
    ,'CAMS409_temperature',\
    'CAMS416_temperature','CAMS603_temperature',\
        'CAMS403_temperature','CAMS167_temperature','CAMS1029_temperature',\
    'CAMS169_temperature','CAMS1020_temperature',]
# elif chem_comp=='temperature':
#     cams_stations=[
#         'CAMS403_temperature']
no_obs_data=['PBLH','HFX','QFX','LH']
if chem_comp in no_obs_data:
    cams_stations=['CAMS403_'+chem_comp]
# if chem_comp=='QFX':
#     cams_stations=['CAMS403_QFX']
# if chem_comp=='QFX':
#     cams_stations=['CAMS403_QFX']    


start=72-72
stop=-1
num_to_analyze=0

tick_laels=np.arange(0,80,1)

if chem_comp not in no_obs_data:

    # print('chem comp is',chem_comp)

    for cams in cams_stations:

            
            real_winds=np.array(get_real_data_chem(cams[0:-len(chem_comp)],month,chem_comp))
            real_winds=np.append([None,None,None,None,None,None,], real_winds)
            # print(real_winds)
            a=check_numbers(real_winds)
            real_winds[a]=None
            real_winds=real_winds[start:]
          
            # real_winds[a]=None
            if row<4:

                axes[row,col].plot(tick_laels[0:len(real_winds)],real_winds,label='obs',linewidth=3,color='black')
           
                axes[row,col].set_title(cams)
            some_counter=0

            dict_for_avgs['real_vals'].append(real_winds)

            # axes[row,col].set_ylim([0,100])
            for urban in urban_names:
                if urban not in dict_for_avgs.keys():
                    dict_for_avgs[urban]=[]
   
                    
                sim_data=simulations_dir+'/'+urban+'/'+urban+"_"+month+'_'+str(domain)+'.csv'
                

                temp_sim=[]
                wspd_sim=[]
                
                # print(sim_data)

 
                # if chem_comp=='wind':
                #     cams=cams+'WSPD'
                # print(cams)
                wspd_sim=np.array(Extract_by_name(sim_data,wspd_sim,cams))
                print(urban,'len of field',len(wspd_sim))
                

                # print(wspd_sim)
                if chem_comp=='carbon_monoxide':
                    wspd_sim=np.array(wspd_sim)/1000
                
                # print(len(wspd_sim),sim_data,cams)

                # if (month== 'Jan' or month=='Feb' or month=='Mar' or month=='Dec'):

                #     wspd_sim=wspd_sim[6+start:]
                # else:

                #     wspd_sim=wspd_sim[5+start:-1]
                # wspd_sim=wspd_sim[24:]
                # print(wspd_sim)
                
                if row<4:
                    axes[row,col].plot(wspd_sim[0:stop],label=urban,linewidth=2,)
                    # axes[row,col].set_xticks(np.arange(0,80,6))
                    # axes[row,col].set_xticklabels([18,24,6,12,18,24,6,12,18,24,6,12,18,24])
                    axes[row,col].set_xticks(np.arange(0,80,5))
                    # axes[row,col].set_ylim(0,50)
                    axes[row,col].set_xticklabels(np.arange(0,80,5))
                

                # axes[row,col].xaxis.set_major_locator(ticker.NullLocator())
                len_of_shortest=check_longer(wspd_sim,real_winds)
                # print(len_of_shortest)
                wspd_sim=wspd_sim[0:len_of_shortest]
                real_winds=real_winds[0:len_of_shortest]
                if len(a)>0:

                    a=check_numbers(real_winds)
                    mask = np.ones(len(real_winds), dtype=bool)
                    mask[a] = False
                    real_winds = real_winds[mask,...]
                    # wspd_sim=wspd_sim[mask,...]
                # print(cams[0:-len(chem_comp)])
                
                if cams[0:-len(chem_comp)-1]=='CAMS403':
                    wspd_sim=np.array(Extract_by_name(sim_data,wspd_sim,cams))
                    # num_to_analyze=0
                    # print('at point ',num_to_analyze,chem_comp,urban,wspd_sim[num_to_analyze])
                    # print('at point ',num_to_analyze,chem_comp,urban,wspd_sim[num_to_analyze])
                    # print(urban,wspd_sim)

                dict_for_avgs[urban].append(wspd_sim)

                # axes[row,col].annotate((urban,str(round(calculate_mae(wspd_sim,real_winds), 2))),
                # xy=(-0.2, -0.2), xycoords='axes points',
                # xytext=(150,-20+some_counter*(-25) ), textcoords='offset points',
                
                # horizontalalignment='right', verticalalignment='bottom')

                # print('corr',str(round(correlation, 2)))

                # axes[row,col].plot(moving_average(wspd_sim,6),label=urban[4:],linewidth=2,)
                # if chem_comp!='wind'or'temperature':
                #     wspd_sim=wspd_sim[24:]
                


                
                some_counter+=1

            col+=1
            if col==3:
                row+=1
                col=0
            


            ### THIS IS FOR CALCULATION, THE UPPER PART IS ONLY PLOTTING###
        

                # print('REAL DATA:',real_data)

else:
    #CAMS169 e.g.
        # cams='CAMS403_PBLH'
    for cams in cams_stations:

        for urban in urban_names:
            
            sim_data=simulations_dir+'/'+urban+'/'+urban+"_"+month+'_'+str(domain)+'.csv'
            # print(sim_data)

            temp_sim=[]
            wspd_sim=[]
            
            # print(sim_data)



            if chem_comp=='wind':
                cams=cams+'WSPD'
            wspd_sim=np.array(Extract_by_name(sim_data,wspd_sim,cams))
            print(chem_comp,urban,wspd_sim[num_to_analyze])
            if chem_comp=='carbon_monoxide':
                wspd_sim=np.array(wspd_sim)/1000


            axes[0,0].set_xticks(np.arange(0,80,5))
            # axes[row,col].set_ylim(0,50)
            axes[0,0].set_xticklabels(np.arange(0,80,5))   
            
            # print(len(wspd_sim),sim_data,cams)

            # if (month== 'Jan' or month=='Feb' or month=='Mar' or month=='Dec'):

            #     wspd_sim=wspd_sim[6:]
            # else:

            #     wspd_sim=wspd_sim[5:-1]
            # wspd_sim=wspd_sim[24:]
            

            axes[row,col].plot(wspd_sim,label=urban,linewidth=2,)
            axes[row,col].set_title(month)
            axes[0,0].set_title(cams)

            # axes[row,col].xaxis.set_major_locator()
            # axes[row,col].xaxis.set_major_locator(ticker.NullLocator())




        col+=1
        if col==3:
            row+=1
            col=0

    # axes[row,col].set_xticks(np.arange(0,80,6))
    # axes[row,col].set_xticklabels([18,24,6,12,18,24,6,12,18,24,6,12,18,24])
        


# plt.legend(['BEM','cd_2.0'])
# print(np.mean(for_mae))
fig.suptitle(month+'_domain_'+str(domain),size=20)

# plt.bar(['wrf','log'],[2.827,2.9043])





# print(len(np.mean(dict_for_avgs['real_vals'],axis=0)))
# print(len(np.mean(dict_for_avgs['No_Urb'],axis=0)))
if chem_comp not in no_obs_data:
    for urban in urban_names:
        for i in range(len(dict_for_avgs[urban])):
            # print('urban is',urban,' i is ',i)
            ##for real avgs also:
            if len(dict_for_avgs['real_vals'][i])<72:
                dict_for_avgs['real_vals'][i]=np.pad(dict_for_avgs['real_vals'][i], (0, 72-len(dict_for_avgs['real_vals'][i])), mode='constant', constant_values=np.nan)

            if len(dict_for_avgs[urban][i])<72:
                dict_for_avgs[urban][i]=np.pad(dict_for_avgs[urban][i], (0, 72-len(dict_for_avgs[urban][i])), mode='constant', constant_values=np.nan)
    #     axes[4,1].plot(np.nanmean(dict_for_avgs[urban],axis=0),label=urban,linewidth=2,)
    # axes[4,1].plot(np.nanmean(dict_for_avgs['real_vals'],axis=0,dtype=float),label='obs',linewidth=3,color='black')
    urban_names.insert(0,'Observed')
axes[4,1].set_title('all stations AVERAGE')

plt.subplots_adjust(hspace=0.7)
fig.legend(urban_names)

plt.show()
