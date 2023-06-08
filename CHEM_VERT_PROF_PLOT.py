import matplotlib.pyplot as plt
import numpy as np
from all_functions import Extract_by_name, Extract_the_shit2
import glob
import os

winds_list=[]
height_list=[]
number_of_pts=11
urban_dirs=['Oct_BEM_MYJ','Oct_BEM_YSU','Oct_NU_MYJ','Oct_NU_YSU']

snapshot_nmbr=45

fig, axes = plt.subplots(nrows=2, ncols=4,figsize=(16,9),sharey='row') 
# fig.subplots_adjust(hspace=0.25,bottom=0.1)
# dir='/Users/lmatak/Downloads/URBAN_SCHEMES_VERT_PROFILES/no_modification/'+month+'/'

# labels=['BEM_def','BEM_decrease','BEM_increase',]
vars_to_plot=['no2','no','co','PM2_5_DRY','wspd','T','rh','o3']
labels=['Oct_BEM_vert_MYJ','cd_low','cd_high'] 
# labels=['z0r_decrease','building_decrease','default','ustar_0.01','z0r_increase',]
i=0
for urban in urban_dirs:
    files=[]
    dir='/Users/lmatak/Downloads/temp_foold/all/WRF_CHEM_VERTICAL_PROFILES/'+urban+'/'
    for file in glob.glob(dir+'*'+str(snapshot_nmbr)+'.csv'):
        files.append(file)
    for file in files:
        col=0
        row=0
        print(file)
        height_list=[]
        winds_list=[]
        no2_list=[]
        co_list=[]
        no_list=[]
        temperature_list=[]
        rh_list=[]
        pm25_list=[]
        height_list=Extract_by_name(file,height_list,'height')
        for var in vars_to_plot:
            print(var)
            list_to_plot=[]
            list_to_plot=Extract_by_name(file,list_to_plot,var)
            # print(list_to_plot)
            axes[row,col].plot(list_to_plot[:number_of_pts],height_list[:number_of_pts],marker=11)
            axes[row,col].set_yticks(height_list[:number_of_pts])
            axes[row,col].set_title(var)
            col+=1
            if col >3:
                row+=1
                col=0


        i+=1
plt.legend(urban_dirs)

# plt.yticks(height_list[:6])

plt.suptitle('at snapshot nmbr '+str(snapshot_nmbr),fontsize=28)
plt.show()

os.chdir(dir)


