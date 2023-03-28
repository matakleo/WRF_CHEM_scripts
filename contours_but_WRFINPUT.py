from cmath import nan
from turtle import right
from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, rh,tk)
from all_functions import Extract_Track_Data, hurricane_eye_3,list_ncfiles,Extract_the_shit2
from cartopy.mpl.gridliner import LongitudeFormatter, LATITUDE_FORMATTER
from cartopy.feature import NaturalEarthFeature
import matplotlib as mpl
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from netCDF4 import Dataset
import cartopy.crs as crs
import math
import numpy as np
import matplotlib.patches as mpatches


from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import cartopy.feature as cfeature
import copy

fig, ax = plt.subplots(nrows=2, ncols=2,subplot_kw={'projection': crs.PlateCarree()},figsize=(16.3, 8.3))

my_cmap1 = copy.copy(mpl.cm.get_cmap('bwr')) # copy the default cmap
my_cmap1.set_bad((0,0,0))


# dirs=['BEM_default','BEP_default',]#'clz_1000','clz_100']
dirs=['Dec_wrfinps','Jun_wrfinps'] #,'BEM_ust_10_in_LSM',]#'clz_1000','clz_100']
# dirs=['BEM_default','BEM_change_tke_100','BEM_change_mom_5',]
dir_num=0
i=0
file_in_dir=4
height_lvl=0
# var_to_plot='TKE'
var_to_plot='o3'


mid_downtown_lon=-95.3621823
mid_downtown_lat=29.7585786


three_dom_lats=np.array([29.67430877685547,29.771469116210938,29.739097595214844,29.68511199951172,29.717498779296875])
three_dom_lons=np.array([-95.1346435546875,-95.22166442871094,-95.25896453857422,-95.29625701904297,-95.34598541259766])



both_temps=[]
col=0

row=0
for dir in dirs:
    ZNT=[]
    Input_Dir = '/Users/lmatak/Downloads/all/WRF_CHEM_CONTOURING/'+dir
    # Input_Dir = '/Users/lmatak/Downloads/URBAN_SCHEME_CONTOURING/different_times/'+dir
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = os.listdir(Input_Dir)
    print('the directory is: ',Input_Dir)
    idx=0

    fh = Dataset(ncfiles[file_in_dir],mode='r')
    print('the ncfile is: ',ncfiles[file_in_dir])
    print('----------------------------')

    lons = fh.variables['XLONG'][0][0]
    lats = fh.variables['XLAT']
    lst2 = [item[0] for item in lats[0]]
    

    # pm25 = fh.variables['E_PM25I'][0][0][:]
    pm25 = fh.variables['o3'][0][0][:]
    print('lons=',np.shape(lons),'lats=',np.shape(lst2),'var to plot=',np.shape(pm25))




    # lon, lat = np.meshgrid(lons, lats)




    ##time of the day$$
    # time_of_the_day=(int(ncfiles[file_in_dir][-8:-6])-5)
    # if time_of_the_day<0:
    #     time_of_the_day=24-abs(time_of_the_day)



    # temperature=getvar(Data,'T2',0)
    # both_temps.append(np.array(temperature))








    # height = (getvar(Data, "height_agl",timeidx = idx))

    # height_one_lvl_more=int(np.mean(height[height_lvl+1]))



    
    # height=int(np.mean(height[height_lvl]))
    # PBLH=getvar(Data,'PBLH',0)

    # print(float(PBLH[24,12]))


#     qv=getvar(Data,"QVAPOR",0)
#     qv=interplevel(qv,height,54)

#     Pressure=getvar(Data,"P",0)
    

#     potential_temp=getvar(Data, "T",0)
    

#     # temperature=tk(Pressure,potential_temp,meta=True, units='K')
#     # temperature=interplevel(temperature,height,50)
#     # print(temperature)
#     # Pressure=interplevel(Pressure,height,54)
#     # potential_temp=interplevel(potential_temp,height,54)
#     # print(temperature)

#     # rel_hum=rh(qv,Pressure,temperature)



    
    both_temps.append(pm25)
    ax[0,col].contourf((lons),(lst2), (pm25), 250,  vmin=pm25.min(),vmax=pm25.max(),     transform=crs.PlateCarree(), 
        cmap=my_cmap1)    

    ax[0,col].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    ax[0,col].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    ax[0,col].set_title('ozone - domain 3')
    
    # ax[0,col].background_patch.set_facecolor('black')  

    # ax[1,col].contourf(to_np(lons1),to_np(lats1), (temperature), 250,  vmin=vmin_set,vmax=vmax_set,     transform=crs.PlateCarree(), 
    #     cmap=my_cmap1)    

    # ax[1,col].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    # ax[1,col].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    # ax[1,col].set_title('at height: '+str(height_one_lvl_more)+'m, at time: '+str(time_of_the_day)+':00 h')
    # ax[1,col].background_patch.set_facecolor('black')  
    dir_num+=1
    col+=1
    # if dir_num==3:
    #     dir_

vmin_set=0
vmax_set=2

diff_in_temp=both_temps[0]-both_temps[1]
ax[1,0].contourf((lons),(lst2),  (diff_in_temp), 255,  vmin=diff_in_temp.min(),vmax=diff_in_temp.max(),     transform=crs.PlateCarree(), 
        cmap=my_cmap1)

    


# norm1 = mpl.colors.Normalize(vmin=vmin_set,vmax=vmax_set)

#                 #xstart ystart xend yend#
                
# cax = plt.axes([0.83, 0.050, 0.01, 0.81])
# plt.subplots_adjust(bottom=0.001, right=0.8, top=0.9)

# cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1),
# cax=cax, orientation='vertical',  extend='max', fraction=0.03,
# label=var_to_plot)

plt.show()