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

from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import cartopy.feature as cfeature
import copy

fig, ax = plt.subplots(nrows=1, ncols=2,subplot_kw={'projection': crs.PlateCarree()},figsize=(14.3, 8.3))

my_cmap1 = copy.copy(mpl.cm.get_cmap('twilight_shifted')) # copy the default cmap
my_cmap1.set_bad((0,0,0))
cmap=plt.get_cmap(
    'twilight_shifted')
cmap2=plt.get_cmap(
    'turbo'
)


dirs=['default'] #,'clz_0p01','clz_100']
dir_num=0

wspd_min=0
wspd_max=50

var='WSPD'
agl=70
time_idx=0
i=0
for dir in dirs[dir_num:dir_num+1]:
    ZNT=[]
    Input_Dir = '/Users/lmatak/Downloads/compare_clz_maria/'+dir
    # Input_Dir = '/Users/lmatak/Downloads/URBAN_SCHEMES/MYJ_BEM/'
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)
    print(Input_Dir)
    # print(ncfiles)

    idx=0

    Data = Dataset(ncfiles[0])
    LAI=np.array(getvar(Data, "LANDMASK", timeidx = idx))
    lakemask=np.array(getvar(Data, "LAKEMASK", timeidx = idx))
    ZNT=np.array(getvar(Data, "ZNT", timeidx = idx))
    print(ZNT.shape)
    ZNT[LAI>0]=0
    ZNT[lakemask>0]=0


    u10=getvar(Data, "U10", timeidx = idx)
    v10=getvar(Data, "V10", timeidx = idx)
    total_wind=np.sqrt(u10**2+v10**2)

    height = (getvar(Data, "height_agl",timeidx = idx))
    total_wind=np.sqrt(u10**2+v10**2)

    print('min znt=',float(np.min(ZNT)),'max znt=',float(np.max(ZNT)), 'avg znt=',float(np.mean(ZNT)))


    lats1, lons1 = latlon_coords(height[0])

    move_conts_to_right_longs=7
    lats_move=7



    (Eye_Slp, Eye_Idx, Eye_Xlat, Eye_Xlon) = hurricane_eye_3(Data, 0)

    print(float(lons1[0][0]))

    ax[i].set_extent([float(Eye_Xlon)-move_conts_to_right_longs, \
        float(Eye_Xlon)+move_conts_to_right_longs, \
            float(Eye_Xlat)-lats_move,float(Eye_Xlat)+lats_move])
    ax[i+1].set_extent([float(Eye_Xlon)-move_conts_to_right_longs,\
        float(Eye_Xlon)+move_conts_to_right_longs,\
            float(Eye_Xlat)-lats_move,float(Eye_Xlat)+lats_move])

            

    vmin=0
    
    vmax=0.005
    # vmax=0.03921752795577049
    # contor=ax[i].contourf(to_np(lons1),to_np(lats1), (ZNT),250, vmin=vmin,vmax=vmax,transform=crs.PlateCarree(), 
    #     cmap=cmap2,)
    contor=ax[i].pcolormesh(to_np(lons1),to_np(lats1), \
                    ZNT,norm=LogNorm(vmin=1e-06,vmax=0.01),cmap=my_cmap1,shading='auto'
                    ,snap='True',\
                    transform=crs.PlateCarree(), 
            )

    ax[i+1].contourf(to_np(lons1),to_np(lats1), (total_wind), 250,  vmin=wspd_min,vmax=wspd_max,     transform=crs.PlateCarree(), 
        cmap=cmap2)
    
    ax[i].set_title(dirs[dir_num])

    
    i+=1

norm1 = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
norm_log=mpl.colors.LogNorm()
norm2 = mpl.colors.Normalize(vmin=wspd_min, vmax=wspd_max)
print(norm_log)
# mpl.cm.ScalarMappable(norm=norm1, cmap=cmap2)
# cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap2),
# ax=ax[0], orientation='horizontal' , fraction=0.1, extend='min',
# label="SLP ")


cbar1=plt.colorbar(contor, ax=ax[0],orientation='horizontal', fraction=0.1
,extend='min')


cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=cmap2),
ax=ax[1], orientation='horizontal',  extend='max', fraction=0.1,
label="wspd ")
    
# fig.colorbar(Zo)


fig.tight_layout()

plt.show()