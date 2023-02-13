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

fig, ax = plt.subplots(nrows=1, ncols=3,subplot_kw={'projection': crs.PlateCarree()},figsize=(16.3, 8.3))

my_cmap1 = copy.copy(mpl.cm.get_cmap('bwr')) # copy the default cmap
my_cmap1.set_bad((0,0,0))


# dirs=['BEM_default','BEP_default',]#'clz_1000','clz_100']
# dirs=['BEM_z0_0.0001','BEM_default','BEM_z0_10'] #,'BEM_ust_10_in_LSM',]#'clz_1000','clz_100']
dirs=['NO_URBAN','WRF_LES_domain_3','WRF_LES_domain_4']
label_names=['NO_URB','LES_dom_3','LES_dom_4']
dir_num=0
i=0
file_in_dir=0
height_lvl=0
# var_to_plot='TKE'
var_to_plot='wspd'


mid_downtown_lon=-95.3621823
mid_downtown_lat=29.7585786


three_dom_lats=np.array([29.67430877685547,29.771469116210938,29.739097595214844,29.68511199951172,29.717498779296875])
three_dom_lons=np.array([-95.1346435546875,-95.22166442871094,-95.25896453857422,-95.29625701904297,-95.34598541259766])


col=0

row=0


import os

# The path to the directory
path = '/Users/lmatak/Downloads/WRF_CHEM_CONTOURING/New_setup_1_dom/'

# Get all files in the directory
files = os.listdir(path)

# Filter for .nc files
wrfout_files = [file for file in files if 'wrfout' in file]
print(wrfout_files)
idx=0
file_num=0

for file in sorted(wrfout_files):
    os.chdir(path)
    ZNT=[]



    Data = Dataset(file)


    print('the ncfile is: ',file)
    print('----------------------------')
    nitrix_dioxide=np.array(getvar(Data, "no2", timeidx = idx))
    nitrix_oxide=np.array(getvar(Data, "no", timeidx = idx))
    PM_2=np.array(getvar(Data, "PM2_5_DRY", timeidx = idx))


    
    wspd=np.array(getvar(Data, "wspd", timeidx = idx))


    height = (getvar(Data, "height_agl",timeidx = idx))
    lats1, lons1 = latlon_coords(height[0])
    height=int(np.mean(height[height_lvl]))

    PM_2=PM_2[0,:,:]
    PM_2=np.log(PM_2)
    nitrix_oxide=nitrix_oxide[0,:,:]
    nitrix_oxide=np.log(nitrix_oxide)
    nitrix_dioxide=nitrix_dioxide[0,:,:]
    nitrix_dioxide=np.log(nitrix_dioxide)

    print((nitrix_dioxide))

    ax[0].contourf(to_np(lons1),to_np(lats1), (PM_2), 25,  vmin=PM_2.min(),
        vmax=PM_2.max(), 
        transform=crs.PlateCarree(), 
        cmap=my_cmap1)    
    ax[1].contourf(to_np(lons1),to_np(lats1), (nitrix_oxide), 25,  vmin=nitrix_oxide.min(),
        vmax=nitrix_oxide.max(), 
        transform=crs.PlateCarree(), 
        cmap=my_cmap1)    
    ax[2].contourf(to_np(lons1),to_np(lats1), (nitrix_dioxide), 25,  vmin=nitrix_dioxide.min(),
            vmax=nitrix_dioxide.max(), 
            transform=crs.PlateCarree(), 
            cmap=my_cmap1)    
    

    ax[0].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    ax[0].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    ax[1].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    ax[1].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    ax[2].scatter(mid_downtown_lon,mid_downtown_lat,s=15,c='black',transform=crs.PlateCarree())    
    ax[2].scatter(three_dom_lons,three_dom_lats,s=15,c='cyan',transform=crs.PlateCarree())
    ax[0].set_title('PM 2.5')
    ax[1].set_title('no')
    ax[2].set_title('no2')
    # ax[col].background_patch.set_facecolor('grey')  

    file_num+=1 
        
    plt.subplots_adjust(bottom=0.001, right=0.8, top=0.9)

    # norm1 = mpl.colors.Normalize(vmin=PM_2.max()/4,vmax=PM_2.max())

                    #xstart ystart xend yend#
    # if file_num==0:
    #     cax = plt.axes([0.1, 0.090, 0.75, 0.091])
        

    #     cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1),
    #     cax=cax, orientation='horizontal',  extend='max', fraction=0.03,
    #     label='WSPD m/s')
    plt.savefig(f"/Users/lmatak/Downloads/WRF_CHEM_CONTOURING/New_setup_1_dom/pics/fig_{file_num}.png",bbox_inches='tight')



# print('saved fig number ',file_num)
# plt.show()