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
import glob

from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import cartopy.feature as cfeature
import copy

fig, ax = plt.subplots(nrows=1, ncols=3,subplot_kw={'projection': crs.PlateCarree()},figsize=(16.3, 8.3))

my_cmap1 = copy.copy(mpl.cm.get_cmap('bwr')) # copy the default cmap
my_cmap1.set_bad((0,0,0))



dir_num=0
i=0
file_in_dir=0
height_lvl=0
# var_to_plot='TKE'


##### WHAT TO PLOT #####
var_to_plot='o3'


mid_downtown_lon=-95.3621823
mid_downtown_lat=29.7585786
three_dom_lats=np.array([29.67430877685547,29.771469116210938,29.739097595214844,29.68511199951172,29.717498779296875])
three_dom_lons=np.array([-95.1346435546875,-95.22166442871094,-95.25896453857422,-95.29625701904297,-95.34598541259766])


col=0

row=0
idx=0
ncfiles_dom_1=[]
ncfiles_dom_2=[]
ncfiles_dom_3=[]
Input_Dir = '/Users/lmatak/Downloads/all/WRF_CHEM_CONTOURING/no_temp_change/'
os.chdir(Input_Dir)
for file in glob.glob('/Users/lmatak/Downloads/all/WRF_CHEM_CONTOURING/no_temp_change/wrfout_d01*'):
    ncfiles_dom_1.append(file)
for file in glob.glob('/Users/lmatak/Downloads/all/WRF_CHEM_CONTOURING/no_temp_change/wrfout_d02*'):
    ncfiles_dom_2.append(file)
for file in glob.glob('/Users/lmatak/Downloads/all/WRF_CHEM_CONTOURING/no_temp_change/wrfout_d03*'):
    ncfiles_dom_3.append(file)
print(ncfiles_dom_3)
for time_step in range(len(ncfiles_dom_3)):




    Data_dom1 = Dataset(ncfiles_dom_1[time_step])
    Data_dom2 = Dataset(ncfiles_dom_2[time_step])
    Data_dom3 = Dataset(ncfiles_dom_3[time_step])



    var_to_plot_dom1=getvar(Data_dom1, var_to_plot, timeidx = idx)
    var_to_plot_dom2=getvar(Data_dom2, var_to_plot, timeidx = idx)
    var_to_plot_dom3=getvar(Data_dom3, var_to_plot, timeidx = idx)

    print(len(np.shape(var_to_plot_dom1)))


    ##time of the day$$
    time_of_the_day=(int(ncfiles_dom_3[file_in_dir][-8:-6])-5)
    if time_of_the_day<0:
        time_of_the_day=24-abs(time_of_the_day)



    height_dom1 = (getvar(Data_dom1, "height_agl",timeidx = idx))
    height_dom2 = (getvar(Data_dom2, "height_agl",timeidx = idx))
    height_dom3 = (getvar(Data_dom3, "height_agl",timeidx = idx))

    lats_dom1, lons_dom1 = latlon_coords(height_dom1[0])
    lats_dom2, lons_dom2 = latlon_coords(height_dom2[0])
    lats_dom3, lons_dom3 = latlon_coords(height_dom3[0])
    height=int(np.mean(height_dom1[height_lvl]))

    vmin_set=np.mean(var_to_plot_dom3)-2*np.std(var_to_plot_dom3)
    vmax_set=np.mean(var_to_plot_dom3)+2*np.std(var_to_plot_dom3)



    ax[0].contourf(to_np(lons_dom1),to_np(lats_dom1), (var_to_plot_dom1), 25,  vmin=vmin_set,vmax=vmax_set,     transform=crs.PlateCarree(), 
        cmap=my_cmap1)    

    ax[0].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    ax[0].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    ax[0].set_title(var_to_plot+' Domain 1, at: '+str(height)+'m, : '+str(time_of_the_day)+':00 h')



    ax[1].contourf(to_np(lons_dom2),to_np(lats_dom2), (var_to_plot_dom2), 25,  vmin=vmin_set,vmax=vmax_set,     transform=crs.PlateCarree(), 
    cmap=my_cmap1)    

    ax[1].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    ax[1].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    ax[1].set_title(var_to_plot+' Domain 2, at: '+str(height)+'m, : '+str(time_of_the_day)+':00 h')

    ax[2].contourf(to_np(lons_dom3),to_np(lats_dom3), (var_to_plot_dom3), 25,  vmin=vmin_set,vmax=vmax_set,     transform=crs.PlateCarree(), 
    cmap=my_cmap1)    

    ax[2].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    ax[2].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    ax[2].set_title(var_to_plot+' Domain 2, at: '+str(height)+'m, : '+str(time_of_the_day)+':00 h')

  


    norm1 = mpl.colors.Normalize(vmin=vmin_set,vmax=vmax_set)

                    #xstart ystart xend yend#
                    
    cax = plt.axes([0.83, 0.050, 0.01, 0.81])
    plt.subplots_adjust(bottom=0.001, right=0.8, top=0.9)

    cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1),
    cax=cax, orientation='vertical',  extend='max', fraction=0.03,
    label=var_to_plot)

plt.show()