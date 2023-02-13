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

# fig, ax = plt.subplots(nrows=2, ncols=2,subplot_kw={'projection': crs.PlateCarree()},figsize=(14.3, 8.3))

my_cmap1 = copy.copy(mpl.cm.get_cmap('bwr')) # copy the default cmap
my_cmap1.set_bad((0,0,0))
cmap=plt.get_cmap(
    'twilight_shifted')
cmap2=plt.get_cmap(
    'turbo'
)

CAMS1_pos=([64],[73])
CAMS55_pos=([61],[70])
CAMS35_pos=([55],[80])
CAMS695_pos=([59],[63])
CAMS416_pos=([56],[67])



dirs=['MYJ_BEM']#,'MYJ_BEM'] #,'clz_0p01','clz_100']
dir_num=0
i=0

row=0
for dir in dirs:
    ZNT=[]
    Input_Dir = '/Users/lmatak/Downloads/URBAN_SCHEMES/MYJ/'+dir
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)
    print('the directory is: ',Input_Dir)
    print('----------------------------')

    idx=0

    Data = Dataset(ncfiles[0])
    print('the ncfile is: ',ncfiles[0])
    print('----------------------------')
    LAI=np.array(getvar(Data, "LANDMASK", timeidx = idx))
    lakemask=np.array(getvar(Data, "LAKEMASK", timeidx = idx))
    wspd=np.array(getvar(Data, "wspd", timeidx = idx))
    U=np.array(getvar(Data, "U", timeidx = idx))
    V=np.array(getvar(Data, "V", timeidx = idx))
    TEMP=np.array(getvar(Data, "AKHS", timeidx = idx))
    height = (getvar(Data, "height_agl",timeidx = idx))


    u10=getvar(Data, "U10", timeidx = idx)
    v10=getvar(Data, "V10", timeidx = idx)
    total_wind=np.sqrt(u10**2+v10**2)

    visina=[]
    visina2=[]
    brzina=[]
    brzina2=[]
    # brzina2=[float(np.mean(total_wind))]
    for i in range(0,10):
        visina=[]
        brzina=[]
        for j in range(54,65):
            for k in range(63,80):
                print('i',i,'j',j,'k',k)
                print(float(height[i][j][k]))
                visina.append(float(height[i][j][k]))
                brzina.append(float(wspd[i][j][k]))
        
        visina2.append(np.mean(visina))
        brzina2.append(np.mean(brzina))

plt.plot(brzina2,visina2)
plt.yticks(visina2)
plt.show()

    

#     height = (getvar(Data, "height_agl",timeidx = idx))


#     print('min znt=',float(np.min(ZNT)),'max znt=',float(np.max(ZNT)), 'avg znt=',float(np.mean(ZNT)))


#     lats1, lons1 = latlon_coords(height[0])

#     (Eye_Slp, Eye_Idx, Eye_Xlat, Eye_Xlon) = hurricane_eye_3(Data, 0)



#     # contor=ax[row,i].pcolormesh(to_np(lons1),to_np(lats1), \
#     #                 ZNT,norm=LogNorm(vmin=ZNT.min(),vmax=ZNT.max()),cmap=my_cmap1,shading='auto'
#     #                 ,snap='True',\
#     #                 transform=crs.PlateCarree(), 
#     #         )
#     ax[row,i].contourf(to_np(lons1),to_np(lats1), (ZNT), 250,  vmin=ZNT.min(),vmax=ZNT.max(),     transform=crs.PlateCarree(), 
#         cmap=cmap2)

#     ax[row,i+1].contourf(to_np(lons1),to_np(lats1), (total_wind), 250,  vmin=total_wind.min(),vmax=total_wind.max(),     transform=crs.PlateCarree(), 
#         cmap=cmap2)
    
#     ax[row,i].set_title(dirs[dir_num])
#     ax[row,i+1].set_title(dirs[dir_num])
#     dir_num+=1
#     row+=1

    


# norm1 = mpl.colors.Normalize(vmin=ZNT.min(), vmax=ZNT.max())
# norm2 = mpl.colors.Normalize(vmin=total_wind.min(), vmax=total_wind.max())


# # cbar1=plt.colorbar(contor, ax=ax[0,0],orientation='vertical', fraction=0.1
# # ,extend='min',label='z0')
# # cbar1=plt.colorbar(contor, ax=ax[1,0],orientation='vertical', fraction=0.1
# # ,extend='min',label='z0')

# cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap2),
# ax=ax[0,0], orientation='vertical',  extend='max', fraction=0.1,
# label="SFC EXCH COEFF FOR MOMENTUM ")
# cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap2),
# ax=ax[1,0], orientation='vertical',  extend='max', fraction=0.1,
# label="SFC EXCH COEFF FOR MOMENTUM ")


# cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=cmap2),
# ax=ax[0,1], orientation='vertical',  extend='max', fraction=0.1,
# label="SFC EXCH COEFF FOR HEAT ")
# cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=cmap2),
# ax=ax[1,1], orientation='vertical',  extend='max', fraction=0.1,
# label="SFC EXCH COEFF FOR HEAT ")
    
# # # fig.colorbar(Zo)


# # fig.tight_layout()

# plt.show()