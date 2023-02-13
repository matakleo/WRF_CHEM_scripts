from tokenize import Ignore
from all_functions import Extract_by_name,Extract_Track_Data,list_csv_files_0, calculate_distance_error,calculate_intensity_error,calculate_intensity_error_slp
import matplotlib.gridspec as gridspec
import os
import numpy as np
import matplotlib.pyplot as plt

def gimme_errors(PBL):
    Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
    Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
    HNS = ['Igor','Lorenzo','Iota','Dorian','Maria']
    GSS = ['2km','8km','32km']
    TM = 'NoTurb'
    PBLS = PBL
    CLS = ['1.0']
    wind_20_percentile=[]
    wind_80_percentile=[]
    track_20_percentile=[]
    track_80_percentile=[]
    list_of_wind_errors=[]
    wind_percentile_20=[]
    wind_percentile_80=[]
    track_percentile_20=[]
    track_percentile_80=[]
    list_of_track_errors=[]
    for GS in GSS:
        all_hurs_track_error_list=[]
        all_hurs_wind_intensity_error_list=[]
        all_hurs_min_slp_error_list=[]
        List_for_CSV_files=[]
        for CL in CLS:
            List_for_CSV_files.append(PBL+'_hpbl_'+CL)

        for HN in HNS:

            Hurricane_Dir =Input_Dir + '/' + HN + '/' + GS + '/' + TM +'/Standard/'  
            Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'

            Real_Lats = []
            Real_Longs = []
            Real_Lats = Extract_Track_Data (Real_data_dir, Real_Lats, 'Lat',HN)
            Real_Longs = Extract_Track_Data (Real_data_dir, Real_Longs, 'Lon',HN)

            Real_slp=[]
            Real_slp = Extract_by_name(Real_Hurricane_Data,Real_slp,'Pressure (mb) ')

            Real_Winds=[]
            Real_Winds = Extract_by_name(Real_Hurricane_Data,Real_Winds,'Wind Speed(kt)')

            csv_files=list_csv_files_0(Hurricane_Dir,List_for_CSV_files)
            
            error_list_track=[]
            error_list_wind_intensity=[]
            error_list_min_slp=[]
            for csv_file in csv_files:

                Eye_Lats=[]
                Eye_Longs=[]
                simulated_wind_intensities=[]
                simulated_min_slp=[]

                Eye_Lats=Extract_by_name(csv_file,Eye_Lats,'min_lat')
                Eye_Longs=Extract_by_name(csv_file,Eye_Longs,'min_long')
                simulated_wind_intensities=Extract_by_name(csv_file,simulated_wind_intensities,'All_Max_WND_SPD_10')
                simulated_min_slp=Extract_by_name(csv_file,simulated_min_slp,'min_slp')

                number = (int((len(Eye_Lats)-1)/(len(Real_Lats)-1)))
                if number == 0:
                    number =1
                Eye_Lats2=[]
                Eye_Longs2=[]
                simulated_wind_intensities2=[]
                simulated_min_slp2=[]
                for i in range(len(Eye_Lats)):


                    Eye_Lats2.append(Eye_Lats[i*number])
                    Eye_Longs2.append(Eye_Longs[i*number])
                    simulated_wind_intensities2.append(simulated_wind_intensities[i*number])
                    simulated_min_slp2.append(simulated_min_slp[i*number])



                error_list_track.append(calculate_distance_error(Eye_Lats2, Eye_Longs2, Real_Lats[0:len(Eye_Lats2)], Real_Longs[0:len(Eye_Lats2)]))
        
                error_list_wind_intensity.append(calculate_intensity_error(simulated_wind_intensities2,Real_Winds))
                error_list_min_slp.append(calculate_intensity_error_slp(simulated_min_slp2,Real_slp))
            # print('error_list_track:',error_list_track)
            all_hurs_track_error_list.append(error_list_track)
            all_hurs_wind_intensity_error_list.append(error_list_wind_intensity)
            all_hurs_min_slp_error_list.append(error_list_min_slp)
        # print('bla',all_hurs_track_error_list)
        all_hurs_min_slp_error_list=np.array(all_hurs_min_slp_error_list)       
        all_hurs_wind_intensity_error_list=np.array(all_hurs_wind_intensity_error_list)
        all_hurs_track_error_list=np.array(all_hurs_track_error_list)
        

        #PERCENTILE ERRORS
        wind_percentile_20.append(np.percentile(all_hurs_wind_intensity_error_list,20))
        wind_percentile_80.append(np.percentile(all_hurs_wind_intensity_error_list,80))
        # wind_80_percentile.append(np.percentile(all_hurs_wind_intensity_error_list,80))
        track_percentile_20.append(np.percentile(all_hurs_track_error_list,20))
        track_percentile_80.append(np.percentile(all_hurs_track_error_list,80))
       

        
        # print('yay')
        # print(all_hurs_track_error_list)

        #plotting#

        avg_track=[]
        avg_wind=[]
        avg_slp=[]

        for i in range(len(error_list_track)):
            # print('i=',i)
            avg_track.append(np.average(all_hurs_track_error_list[:,i]))
            avg_wind.append(np.average(all_hurs_wind_intensity_error_list[:,i]))
            avg_slp.append(np.average(all_hurs_min_slp_error_list[:,i]))

        list_of_wind_errors.append(avg_wind)
        list_of_track_errors.append(avg_track)
        
    wind_percentile=[]
    track_percentile=[]
    for i in range(len(wind_percentile_20)):
        wind_percentile.append([[float(list_of_wind_errors[i]-wind_percentile_20[i])],[float(wind_percentile_80[i]-list_of_wind_errors[i])]])
        track_percentile.append([[float(list_of_track_errors[i]-track_percentile_20[i])],[float(track_percentile_80[i]-list_of_track_errors[i])]])
    print(PBL+' track percentil 80: ',track_percentile_80)
    print(PBL+' track percentil 20: ',track_percentile_20)
    # print('tarck percentila',track_percentile)
    # print('Wind percentile 80',wind_percentile)
    return(list_of_wind_errors,list_of_track_errors,wind_percentile,track_percentile)
 
# gimme_errors('MYJ')