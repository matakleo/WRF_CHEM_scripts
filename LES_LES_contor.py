from turtle import right
from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)
from all_functions import Extract_Track_Data,list_ncfiles,Extract_the_shit2
from cartopy.mpl.gridliner import LongitudeFormatter, LATITUDE_FORMATTER
from cartopy.feature import NaturalEarthFeature
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from netCDF4 import Dataset
import cartopy.crs as crs
import numpy as np

from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import cartopy.feature as cfeature


fig, ax = plt.subplots(nrows=1, ncols=4,subplot_kw={'projection': crs.PlateCarree()},figsize=(18.3, 9.3),sharey='row')


cmap=plt.get_cmap(
    'twilight_shifted')
cmap2=plt.get_cmap(
    'Blues'
)


titles=['NO_URBAN','SLUCM','BEP','BEM']
dirs=['NO_URBAN','SLUCM','BEP','BEM']
var='blues_r'
agl=50
time_idx=0
i=0
for dir in dirs:
    ZNT=[]
    Input_Dir = '/Users/lmatak/Downloads/URBAN_SCHEMES/MYJ/MYJ_'+dir+'/'
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)
    print(Input_Dir)
    print(ncfiles)

    idx=0

    Data = Dataset(ncfiles[0])
    ZNT=getvar(Data, "U10", timeidx = idx)
    # ZNT=ZNT[0][:-1]
    

    height = (getvar(Data, "height_agl",timeidx = idx))
    # print(height)
    print('znt==',ZNT.shape)

    # ZNT=interplevel(ZNT,height,agl)
    lats1, lons1 = latlon_coords(height[0])
    print(float(np.amax(ZNT)))
    ax[i].set_extent([float(lons1[0][0]),float(lons1[-1][-1]),float(lats1[0][0]),float(lats1[-1][-1])])
    print(type(lons1))
#     # # Get the cartopy mapping object
    print(lats1.shape,lons1.shape,ZNT.shape)
    ax[i].contourf(to_np(lons1),to_np(lats1), (ZNT), 255,
        transform=crs.PlateCarree(), 
        cmap=cmap2)
    
    ax[i].set_title(titles[i])

    real_data_file='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data/xlsx/measureing_locations.csv'

    obs_stations_longitudes =[]
    obs_stations_latitudes=[]
    obs_stat_sim_lats=[]
    obs_stat_sim_lons=[]
    obs_stations_longitudes=Extract_the_shit2(real_data_file,obs_stations_longitudes,'LON')
    obs_stations_latitudes=Extract_the_shit2(real_data_file,obs_stations_latitudes,'LAT')
    # print(obs_stations_latitudes,obs_stations_longitudes)
    # ax[i].scatter(obs_stations_longitudes,obs_stations_latitudes,s=55,c='blue',transform=crs.PlateCarree(), )
    i+=1
norm1 = mpl.colors.Normalize(vmin=0, vmax=np.amax(ZNT))
# mpl.cm.ScalarMappable(norm=norm1, cmap=cmap2)
cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap2),
ax=ax[1], orientation='horizontal',  extend='both', fraction=0.1,
label="U10")
    
# fig.colorbar(Zo)




# h,l=ax[0].get_legend_handles_labels()
# ax[0].legend(h,l)

plt.show()