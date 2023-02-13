
import numpy as np
import matplotlib.pyplot as plt
from all_functions import Extract_by_name, Extract_the_shit2
import glob
import os
import pandas as pd



def avg_values(d, key):

    #for averaging out keys in a dict
    values = d[key]
    avg = sum(values) / len(values)
    return avg

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



## figure definition

fig, ax = plt.subplots(nrows=3, ncols=3,figsize=(19.3, 9.7))


# Calculate the mean absolute error for each month

simulations_dir='/Users/lmatak/Downloads/URBAN_TIME_SERIES_MAE/'
real_dir='/Users/lmatak/Desktop/WRF_CHEM_obs_data/whole_year_reports/'
urb=['MYJ_Default_No_Urb','MYJ_Default_BEM','MYJ_Default_SLUC','MYJ_Ustar_10_SLUC', \
     'MYJ_Increased_Buildings','MYJ_Decreased_Buildings','MYJ_cd_0.5','MYJ_cd_2.0','MYJ_cd_3.0','MYJ_cd_4.0',\
        'MYJ_Mom_0.2','MYJ_Mom_0.5','MYJ_Mom_2.0','MYJ_Mom_5.0' ]

# HOW MANY MONTHS IN CALCULATION, SHOULD ALWAYS BE 12, UNLESS DEBUGGING !!!
months = 12

# CAMS stations taken into consideration
cams_stations=['CAMS35_WSPD','CAMS416_WSPD','CAMS1_WSPD','CAMS55_WSPD','CAMS169_WSPD','CAMS53_WSPD','CAMS1052_WSPD']

#lists needed for gathering data of observed and simulated
wspd_sim=[]


#a counter used for plotting, do not delete!
run_number=0

#Initialize the main data holder, the dictionary with the values to plot
error_dict={}


#dictionary used for plotting the averaged error over all the cams
dict_for_averaging_all_cams = {}


### the loop goes like this: MYJ_Default_No_Urb --> each month --> each cams station, then MYJ_Default_BEM --> each month --> each cams station,
for urban_simulation in urb:
    print('urban directory number:',run_number+1,'/',len(urb))

    #the list that would hold the csvs of the simulated data, clean it each loop so it doesn't accumulate, that is why it is here
    sim_data=[]

    #Clean all the keys of the dictionary for each urban_sim run. That way the error is calculated correctly
    error_dict['CAMS1']=[]
    error_dict['CAMS55']=[]
    error_dict['CAMS35']=[]
    # error_dict['CAMS695']=[]
    error_dict['CAMS416']=[]
    error_dict['CAMS169']=[]
    error_dict['CAMS53']=[]
    error_dict['CAMS1052']=[]


    turb_sim_dir=simulations_dir+urban_simulation
    # Collect all the simulation CSVs (12 months = 12 csvs), adn sort them
    for file in glob.glob(turb_sim_dir+'/*.csv'):
            sim_data.append(file)
    sim_data.sort()

    #once we have all the simulated data gathered in a list, we loop through the months
    #variable months is just a number, and should always be set to 12
    for month_number in range(months):
        #the mae calculation starts from zero for each month
        mae=0
        for cams_station in cams_stations:

            ################################################################
            ###### to test out some specific month, set the variable 'months' to 1, and then edit here:####
                                    # month_number=11


            # empty the list for winds for each iteration
            wspd_sim=[]
            
            #get the SIMULATED data for specific month and specific station
            #actual wspd points from simulation
            simulation_month=(Extract_by_name(sim_data[month_number],wspd_sim,cams_station))


            
            #for the real data, parse the name of the cams station, and the name of the month
            cams_name_for_real_data=cams_station[0:-5]
            month_name_for_real_data=sim_data[month_number][-7:-4]

            ##this is necessart to adjust the difference between UTC and WRF time
            if (month_name_for_real_data== 'Jan' or month_name_for_real_data=='Feb' or month_name_for_real_data=='Mar' or month_name_for_real_data=='Dec'):

                simulation_month=simulation_month[6:]
            else:

                simulation_month=simulation_month[5:-1]

            #get the real data
            real_data=get_real_data(cams_name_for_real_data,month_name_for_real_data)

            
            #append the mae seperately to different keys, for each month!
            #this is what will be getting plotted!!
            # error_dict[cams_name_for_real_data].append(mae)

            #for debugging, this print line is very useful
            # print(urban_simulation,month_number,cams_station,mae)

            #calculate the CORRCOEFF
            p,corr= np.corrcoef(simulation_month, real_data.tolist())
            #manipulate a little to get a single numbber
            corr=corr[0]

            error_dict[cams_name_for_real_data].append(float(corr))

      


            ##THIS IS USED FOR AVERAGING OUT ALL THE CAMS STATIONS!!##
            #if the key exists, e.g. MYJ_Increased_Buildings, just append the mae, if not create the key and append the mae
            if urban_simulation in dict_for_averaging_all_cams:
                dict_for_averaging_all_cams[urban_simulation].append(corr)
            else:
                dict_for_averaging_all_cams[urban_simulation]=[]
                dict_for_averaging_all_cams[urban_simulation].append(corr)

            

    ################################################################
    ############################ PLOTTING ##########################
    ################################################################

    #some x axis value
    bar_x = 0

    #for the first run 
    if run_number==0:
          
        ax[0,0].bar(bar_x,avg_values(error_dict,'CAMS1'),width=0.3,label=urb[run_number][4:],edgecolor='black')
        ax[0,1].bar(bar_x,avg_values(error_dict,'CAMS55'),width=0.3,edgecolor='black')
        ax[1,0].bar(bar_x,avg_values(error_dict,'CAMS35'),width=0.3,edgecolor='black')
        ax[1,1].bar(bar_x,avg_values(error_dict,'CAMS416'),width=0.3,edgecolor='black')
        ax[2,0].bar(bar_x,avg_values(error_dict,'CAMS169'),width=0.3,edgecolor='black')
        ax[2,1].bar(bar_x,avg_values(error_dict,'CAMS53'),width=0.3,edgecolor='black')
        ax[2,2].bar(bar_x,avg_values(error_dict,'CAMS1052'),width=0.3,edgecolor='black')
        
        ax[0,0].set_title('CAMS1')
        ax[0,1].set_title('CAMS55')
        ax[1,0].set_title('CAMS35')
        ax[1,1].set_title('CAMS416')
        ax[2,0].set_title('CAMS169')
        ax[2,1].set_title('CAMS53')
        ax[2,2].set_title('CAMS1052')
       
        

     #after the first run, offset the bars 
    else:
        bar_x_offset = [bar_x + run_number]  
        ax[0,0].bar(bar_x_offset,avg_values(error_dict,'CAMS1'),width=0.3,label=urb[run_number][4:],edgecolor='black')
        ax[0,1].bar(bar_x_offset,avg_values(error_dict,'CAMS55'),width=0.3,edgecolor='black')
        ax[1,0].bar(bar_x_offset,avg_values(error_dict,'CAMS35'),width=0.3,edgecolor='black')
        ax[1,1].bar(bar_x_offset,avg_values(error_dict,'CAMS416'),width=0.3,edgecolor='black')
        ax[2,0].bar(bar_x_offset,avg_values(error_dict,'CAMS169'),width=0.3,edgecolor='black')
        ax[2,1].bar(bar_x_offset,avg_values(error_dict,'CAMS53'),width=0.3,edgecolor='black')
        ax[2,2].bar(bar_x_offset,avg_values(error_dict,'CAMS1052'),width=0.3,edgecolor='black')


    # put the horizontal lines
    if urban_simulation =='MYJ_Default_No_Urb':
        ax[0,0].axhline(y = avg_values(error_dict,'CAMS1'), color = 'b', linestyle = '--')
        ax[0,1].axhline(y = avg_values(error_dict,'CAMS55'), color = 'b', linestyle = '--')
        ax[1,0].axhline(y = avg_values(error_dict,'CAMS35'), color = 'b', linestyle = '--')
        ax[1,1].axhline(y = avg_values(error_dict,'CAMS416'), color = 'b', linestyle = '--')
        ax[2,0].axhline(y = avg_values(error_dict,'CAMS169'), color = 'b', linestyle = '--')
        ax[2,1].axhline(y = avg_values(error_dict,'CAMS53'), color = 'b', linestyle = '--')
        ax[2,2].axhline(y = avg_values(error_dict,'CAMS1052'), color = 'b', linestyle = '--')
    elif urban_simulation =='MYJ_Default_BEM':

        ax[0,0].axhline(y = avg_values(error_dict,'CAMS1'), color = 'orange', linestyle = ':')
        ax[0,1].axhline(y = avg_values(error_dict,'CAMS55'), color = 'orange', linestyle = ':')
        ax[1,0].axhline(y = avg_values(error_dict,'CAMS35'), color = 'orange', linestyle = ':')
        ax[1,1].axhline(y = avg_values(error_dict,'CAMS416'), color = 'orange', linestyle = ':')
        ax[2,0].axhline(y = avg_values(error_dict,'CAMS169'), color = 'orange', linestyle = ':')
        ax[2,1].axhline(y = avg_values(error_dict,'CAMS53'), color = 'orange', linestyle = ':')
        ax[2,2].axhline(y = avg_values(error_dict,'CAMS1052'), color = 'orange', linestyle = ':')
    elif urban_simulation =='MYJ_Default_SLUC':

        ax[0,0].axhline(y = avg_values(error_dict,'CAMS1'), color = 'g', linestyle = '-.')
        ax[0,1].axhline(y = avg_values(error_dict,'CAMS55'), color = 'g', linestyle = '-.')
        ax[1,0].axhline(y = avg_values(error_dict,'CAMS35'), color = 'g', linestyle = '-.')
        ax[1,1].axhline(y = avg_values(error_dict,'CAMS416'), color = 'g', linestyle = '-.')
        ax[2,0].axhline(y = avg_values(error_dict,'CAMS169'), color = 'g', linestyle = '-.')
        ax[2,1].axhline(y = avg_values(error_dict,'CAMS53'), color = 'g', linestyle = '-.')
        ax[2,2].axhline(y = avg_values(error_dict,'CAMS1052'), color = 'g', linestyle = '-.')

            
    
    run_number+=1

    #####################################################################################
    ############################ PLOTTING THE AVERAGE BARPLOTS ##########################
    #####################################################################################
bar_x = 0
for_plot_counter=0    
for urban_sim in urb:
    #if first plot just use x, for further ones offset by some value
    if for_plot_counter==0:
        ax[1,2].bar(bar_x,avg_values(dict_for_averaging_all_cams,urban_sim),width=0.4,edgecolor='black')
    else:
        bar_x_offset = [bar_x + for_plot_counter]
        ax[1,2].bar(bar_x_offset,avg_values(dict_for_averaging_all_cams,urban_sim),width=0.4,edgecolor='black')
            
    for_plot_counter+=1
#add the horizontal lines

ax[1,2].axhline(y = avg_values(dict_for_averaging_all_cams,'MYJ_Default_No_Urb'), color = 'b', linestyle = '--')
ax[1,2].axhline(y = avg_values(dict_for_averaging_all_cams,'MYJ_Default_BEM'), color = 'orange', linestyle = ':')
ax[1,2].axhline(y = avg_values(dict_for_averaging_all_cams,'MYJ_Default_SLUC'), color = 'green', linestyle = '-.')  
ax[1,2].set_title('all stations AVERAGE',size=15)    


#get the legend values from one of the axis
h, l = ax[0,0].get_legend_handles_labels()
plt.rc('legend',fontsize=13)
# legend_names1=legend_names

fig.suptitle('CORRELATION COEFFICIENT',size=20)

ax[0,2].axis("off")
ax[0,2].legend(h, l,ncol=2,frameon=False) 

# fig.legend()
plt.show()


