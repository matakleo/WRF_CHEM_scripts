from cmath import nan
from turtle import right
from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)
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

fig, ax = plt.subplots(nrows=2, ncols=3,subplot_kw={'projection': crs.PlateCarree()},figsize=(16.3, 8.3))

my_cmap1 = copy.copy(mpl.cm.get_cmap('bwr')) # copy the default cmap
my_cmap1.set_bad((0,0,0))


# dirs=['BEM_default','BEP_default',]#'clz_1000','clz_100']
# dirs=['BEM_z0_0.0001','BEM_default','BEM_z0_10'] #,'BEM_ust_10_in_LSM',]#'clz_1000','clz_100']
dirs=['BEM_change_mom_10','BEM_default','BEM_change_tke_100']
# dirs=['BEM_z0_0.0001','BEM_default'] #,'BEM_z0_10']
dir_num=0
i=0
file_in_dir=10
height_lvl=0
# var_to_plot='TKE'
var_to_plot='wspd'


mid_downtown_lon=-95.3621823
mid_downtown_lat=29.7585786


three_dom_lats=np.array([29.67430877685547,29.771469116210938,29.739097595214844,29.68511199951172,29.717498779296875])
three_dom_lons=np.array([-95.1346435546875,-95.22166442871094,-95.25896453857422,-95.29625701904297,-95.34598541259766])


col=0

row=0
for dir in dirs:
    ZNT=[]
    Input_Dir = '/Users/lmatak/Downloads/URBAN_SCHEME_CONTOURING/'+dir
    # Input_Dir = '/Users/lmatak/Downloads/URBAN_SCHEME_CONTOURING/different_times/'+dir
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)
    print('the directory is: ',Input_Dir)
    idx=0
    # print(ncfiles[file_in_dir])
    # print(ncfiles[file_in_dir][-8:-6])
    # print(int(ncfiles[file_in_dir][-8:-6])-5)

    Data = Dataset(ncfiles[file_in_dir])
    print('the ncfile is: ',ncfiles[file_in_dir])
    print('----------------------------')
    LAI=np.array(getvar(Data, "LANDMASK", timeidx = idx))
    lakemask=np.array(getvar(Data, "LAKEMASK", timeidx = idx))
    ZNT=np.array(getvar(Data, "U10", timeidx = idx))
    TEMP=np.array(getvar(Data, "AKHS", timeidx = idx))
    TKE=np.array(getvar(Data, "TKE_PBL", timeidx = idx))
    z0=np.array(getvar(Data, "Z0", timeidx = idx))
    wspd=np.array(getvar(Data, "wspd", timeidx = idx))
    # ust=np.array(getvar(Data, "tke", timeidx = idx))
    MASKING=np.array(getvar(Data, "LU_INDEX", timeidx = idx))
    u10=getvar(Data, "U10", timeidx = idx)
    v10=getvar(Data, "V10", timeidx = idx)
    momentum=getvar(Data, "EXCH_H", timeidx = idx)
    ##time of the day$$
    time_of_the_day=(int(ncfiles[file_in_dir][-8:-6])-5)
    if time_of_the_day<0:
        time_of_the_day=24-abs(time_of_the_day)


    tke_to_plot=np.log(TKE[height_lvl])
    # tke_to_plot=momentum[height_lvl]
    tke_min=tke_to_plot.min()
    tke_max=tke_to_plot.max()
    tke_label='log of TKE [m^2/s^2]'

    total_wind=wspd[height_lvl]
    vmin_set=3
    vmax_set=8
    label='WSPD [m/s]'

    height = (getvar(Data, "height_agl",timeidx = idx))
    lats1, lons1 = latlon_coords(height[0])
    height=int(np.mean(height[height_lvl]))

    tke_to_plot[MASKING!=13]=nan
    total_wind[MASKING!=13]=nan


    print('min wspd=',float(np.min(total_wind)),'max wspd=',float(np.max(total_wind)), 'avg total_wind=',float(np.mean(total_wind)))

    

   

    

    ax[0,col].contourf(to_np(lons1),to_np(lats1), (total_wind), 250,  vmin=vmin_set,vmax=vmax_set,     transform=crs.PlateCarree(), 
        cmap=my_cmap1)    

    ax[0,col].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    ax[0,col].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    ax[0,col].set_title(dirs[dir_num][4:]+' z= '+str(height)+'m, time of day:'+str(time_of_the_day)+':00 h')
    ax[1,col].set_title(dirs[dir_num][4:]+', z= '+str(height)+'m, time of day: '+str(time_of_the_day)+':00 h')
    ax[0,col].background_patch.set_facecolor('black')  


    ax[1,col].contourf(to_np(lons1),to_np(lats1), (tke_to_plot), 250,  vmin=tke_min,vmax=tke_max,     transform=crs.PlateCarree(), 
        cmap=my_cmap1)    

    ax[1,col].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    ax[1,col].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    # ax[1,col].set_title(dirs[dir_num]+' at height: '+str(height)+'m')
    ax[1,col].background_patch.set_facecolor('black') 
    dir_num+=1
    col+=1

    


norm1 = mpl.colors.Normalize(vmin=vmin_set,vmax=vmax_set)
norm2=mpl.colors.Normalize(vmin=tke_min,vmax=tke_max)

                #xstart ystart x_length ylength#
                
                #upper
cax1= plt.axes([0.83, 0.54, 0.01, 0.31])  
                #lower             
cax2 = plt.axes([0.83, 0.05, 0.01, 0.33])

plt.subplots_adjust(bottom=0, right=0.8, top=0.9)

cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1),
cax=cax1, orientation='vertical',  extend='max', fraction=0.03,
label=var_to_plot)

cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=my_cmap1),
cax=cax2, orientation='vertical',  extend='max', fraction=0.03,
label=tke_label)

plt.show()