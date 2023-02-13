from cmath import nan
from turtle import right
from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)
from all_functions import Calculate_Distance_Haversine, Extract_Track_Data, hurricane_eye_3,list_ncfiles,Extract_the_shit2
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

fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(14.3, 8.3))

my_cmap1 = copy.copy(mpl.cm.get_cmap('twilight_shifted')) # copy the default cmap
my_cmap1.set_bad((0,0,0))
cmap=plt.get_cmap(
    'twilight_shifted')
cmap2=plt.get_cmap(
    'turbo'
)

cmap_discrete = (mpl.colors.ListedColormap(['grey', 'blue','red', 'blue', 'grey'])
        .with_extremes(over='cyan', under='cyan'))


dirs=['Igor_0p0001'] #,'clz_0p01','clz_100']
dir_num=0

wspd_min=0
wspd_max=50
for_scatter=[]
var='WSPD'
agl=70
time_idx=0
radius=0
i=0
radius_dict={}
for dir in dirs[dir_num:dir_num+1]:
    ZNT=[]
    Input_Dir = '/Users/lmatak/Downloads/dorian_contours/MENGS_outs/dorian_100p0/'+dir
    # Input_Dir = '/Users/lmatak/Downloads/URBAN_SCHEMES/MYJ_BEM/'
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)
    print(Input_Dir)
    # print(ncfiles)

    idx=0
    
    Data = Dataset(ncfiles[0])
    (Eye_Slp, Eye_Idx, Eye_Xlat, Eye_Xlon) = hurricane_eye_3(Data, 0)
    LAI=np.array(getvar(Data, "LANDMASK", timeidx = idx))
    lakemask=np.array(getvar(Data, "LAKEMASK", timeidx = idx))
    ZNT=np.array(getvar(Data, "slp", timeidx = idx))
    print(ZNT.shape)
    # ZNT[LAI>0]=0
    # ZNT[lakemask>0]=0
    u10=getvar(Data, "U10", timeidx = idx)
    v10=getvar(Data, "V10", timeidx = idx)
    print(u10.shape[0])
    # latitude
    total_wind=np.array(np.sqrt(u10**2+v10**2))
    for l in range(u10.shape[0]):
        #longitude
        for j in range(u10.shape[1]):
            distu= Calculate_Distance_Haversine(u10[l,j].XLAT,u10[l,j].XLONG,Eye_Xlat,Eye_Xlon)

            if (distu>=50 and distu<=400):
                print('Distance: ',distu)
                print('indices ',l,j, 'out of ',(u10.shape[0]),(u10.shape[1]))
                print('intensity: ',total_wind[l,j])
                print('u10^2 ',float(u10[l,j])**2,'v10^2 ',float(v10[l,j])**2)
                print('----------------')
                
                if (int((distu))) in radius_dict:            
                    radius_dict[ (int((distu))) ].append(total_wind[l,j])
                #DECLARE new key, and append the value
                else:
                #DECLARE key as a list, so you can append, and eventually average it
                        radius_dict[ (int((distu))) ]=[]
                        radius_dict[ (int((distu))) ].append(total_wind[l,j])
             
     

for key in sorted(radius_dict.keys()):
    print('key:',key)
    # print('to append:',radius_dict[key])
    for_scatter.append((radius_dict[key]))

print(for_scatter)
for_scatter = list(np.concatenate(for_scatter).flat)
print(for_scatter)
mean_wspd=np.mean(for_scatter)
print('mean ,',mean_wspd)
print('std dev= ',np.std(for_scatter))
# print('items ,',radius_dict.items())
print(np.arange(0,len(for_scatter),1))
ax.scatter(np.arange(0,len(for_scatter),1),for_scatter,s=1.4)
ax.axhline(y = mean_wspd,xmin=0,xmax=len(for_scatter), color = 'r', label = 'STD DEV')
ax.axhline(y = mean_wspd-np.std(for_scatter),xmin=0,xmax=len(for_scatter), color = 'g', label = 'MEAN')
ax.axhline(y = mean_wspd+np.std(for_scatter),xmin=0,xmax=len(for_scatter), color = 'g', label = 'STD DEV')
yticks=[0,mean_wspd-np.std(for_scatter),mean_wspd,mean_wspd+np.std(for_scatter),np.max(for_scatter)]
xticks=[0,10,20,100,273]
ax.set_xticks(xticks,minor=False,)
ax.set_yticks(yticks,  minor=False,)
ax.set_title(dir)

fig.tight_layout()
plt.show()

#     height = (getvar(Data, "height_agl",timeidx = idx))


#     print('min znt=',float(np.min(ZNT)),'max znt=',float(np.max(ZNT)), 'avg znt=',float(np.mean(ZNT)))


#     lats1, lons1 = latlon_coords(height[0])

#     move_conts_to_right_longs=7
#     lats_move=7
#     print(type(total_wind))
#     print(total_wind.shape)
    
#     # total_wind=total_wind[total_wind!=0]
#     var=np.var(total_wind[total_wind!=0])
#     mean=np.mean(total_wind[total_wind!=0])
#     stddev=np.std((total_wind[total_wind!=0]))
#     cv=stddev/mean
#     print('variance: ',var)
#     print('mean: ', mean)
#     print('stddev: ',stddev)
#     print('cv: ',cv)
#     vmin=0
#     bounds=[0,stddev,mean-1,mean+1,mean+stddev,55]

#     # bounds=[0,10,20,30,40,50]
#     vmax=np.max(abs(u10))
#     wspd_max=55 
#     # vmax=0.03921752795577049
    
#     contor=ax[i].contourf(to_np(lons1),to_np(lats1), (abs(u10)),250, vmin=vmin,vmax=vmax,transform=crs.PlateCarree(), 
#         cmap=my_cmap1,)
    
#     contor2=ax[i+1].contourf(to_np(lons1),to_np(lats1), (total_wind), vmin=wspd_min,vmax=wspd_max,levels=bounds,     transform=crs.PlateCarree(), 
#        cmap=cmap_discrete, )
    
#     ax[i].set_title(dirs[dir_num])

    
#     i+=1


  

# norm1 = mpl.colors.Normalize(vmin=vmin, vmax=vmax)



# cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap2),
# ax=ax[0], orientation='horizontal' , fraction=0.1, extend='min',
# label="SLP ")




# norm_discrete = mpl.colors.BoundaryNorm(bounds, cmap.N)  


# # bounds = [1, 2, 4, 7, 8]
# # norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
# # fig.colorbar(
# #     mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
# #     cax=ax,
# #     extend='both',
# #     ticks=bounds,
# #     spacing='proportional',
# #     orientation='horizontal',
# #     label='Discrete intervals, some other units',
# # )

# cbar2=fig.colorbar(contor2,
    
# ax=ax[1], orientation='horizontal',  extend='both',ticks=bounds,spacing='uniform', fraction=0.1,
# label="wspd ")
    
# # fig.colorbar(Zo)





# plt.show()