from cmath import nan
from turtle import right
from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)
from all_functions import Extract_Track_Data,list_ncfiles,Extract_the_shit2
from cartopy.mpl.gridliner import LongitudeFormatter, LATITUDE_FORMATTER
from cartopy.feature import NaturalEarthFeature
import matplotlib as mpl
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from netCDF4 import Dataset
import cartopy.crs as crs
import numpy as np

import copy

from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import cartopy.feature as cfeature



os.environ["PATH"]+=":/Library/TeX/texbin/"
print(os.environ["PATH"])
plt.rcParams.update({
    "text.usetex":True,
    "font.family":'Times New Roman'
})


my_cmap1 = copy.copy(mpl.cm.get_cmap('twilight_shifted')) # copy the default cmap
my_cmap1.set_bad((0,0,0))
my_log_cmap=copy.copy(mpl.cm.get_cmap('twilight_shifted')) # copy the default cmap
my_cmap2 = copy.copy(mpl.cm.get_cmap('turbo')) # copy the default cmap
my_cmap2.set_bad((0,0,0))




fig, ax = plt.subplots(nrows=2, ncols=2,subplot_kw={'projection': crs.PlateCarree()},figsize=(12.3, 8.3),dpi=500)


cmap=plt.get_cmap(
    'twilight_shifted')
cmap2=plt.get_cmap(
    'turbo'
)


dirs=['clz_1p0_second_file_katrina','clz_0p01_second_file_katrina_10_to_20',] #,'clz_0p01','clz_100']
dir_num=0

wspd_min=10
wspd_max=55

var='WSPD'
agl=70
time_idx=0
row=0
i=0
for dir in dirs:
    ZNT=[]
    Input_Dir = '/Users/lmatak/Downloads/clz_cases/'+dir
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)
    print(Input_Dir)

    wspd=[]
    idx=0

    Data = Dataset(ncfiles[0])
    LAI=np.array(getvar(Data, "LANDMASK", timeidx = idx))
    lakemask=np.array(getvar(Data, "LAKEMASK", timeidx = idx))
    ZNT=np.array(getvar(Data, "ZNT", timeidx = idx))
    print(ZNT.shape)
    print(LAI.shape)
    ZNT[LAI>0]=nan
    ZNT[lakemask>0]=nan

    u10=getvar(Data, "U10", timeidx = idx)
    v10=getvar(Data, "V10", timeidx = idx)
    total_wind=np.sqrt(u10**2+v10**2)


    wspd=getvar(Data, "wspd", timeidx = idx)
    ust=getvar(Data, "UST", timeidx = idx)
    height = (getvar(Data, "height_agl",timeidx = idx))
    
    wspd=np.array(interplevel(wspd,height,agl))
    wspd[(LAI>0) | (lakemask>0)]=0
    total_wind=np.array(total_wind)
    ZNT[(total_wind<10)]=nan
    total_wind[(total_wind<10)]=nan
    
    lats1, lons1 = latlon_coords(height[0])

    move_conts_to_right_longs=10
    lats_move=4.5
    ax[row,i].set_extent([float(lons1[0][0])+14, \
        float(lons1[-1][-1])-move_conts_to_right_longs, \
            float(lats1[0][0])+lats_move,float(lats1[-1][-1])-lats_move])
    ax[row,i+1].set_extent([float(lons1[0][0])+14,\
        float(lons1[-1][-1])-move_conts_to_right_longs,\
            float(lats1[0][0])+lats_move,float(lats1[-1][-1])-lats_move])

        ####################################
    ### SET THE ZNT MIN AND MAX FOR PLOTTING ###
        ####################################
    
    vmin=0
    vmax=np.max(ZNT)
    print('znt min ',np.min(ZNT),'znt max',np.max(ZNT))
    
    # FOR LOG SCALE#
    contor=ax[row,i].pcolormesh(to_np(lons1),to_np(lats1), \
                 ZNT,norm=LogNorm(vmin=1e-5/16,vmax=0.00285),cmap=my_cmap1,shading='auto'
                 ,snap='True',\
                 transform=crs.PlateCarree(), 
        )
    
    ###FOR LINEAR###
    # contor=ax[row,i].contourf(to_np(lons1),to_np(lats1), \
    #              ZNT,2500,vmin=1e-7,vmax=0.00285/4,cmap=my_cmap1,
    #              transform=crs.PlateCarree(),
                  
    #     )
    
    ax[row,i+1].contourf(to_np(lons1),to_np(lats1), (total_wind), 250,  vmin=wspd_min,vmax=wspd_max,     transform=crs.PlateCarree(), 
        cmap=my_cmap2,)
    ax[row,i+1].background_patch.set_facecolor('black')    
    ax[row,i].background_patch.set_facecolor('black')  

    
    
    # ax[row,i].set_title(dirs[dir_num])

    
    row+=1

###for log##
cbar1=plt.colorbar(contor, ax=ax[0,0],orientation='vertical', fraction=0.1
,extend='min')
print('Im here',cbar1.ax.get_yticklabels())
cbar1.ax.tick_params(labelsize=24)
cbar1.set_label(label=r'$Z_{ 0 } \mathrm{(\,m) \,} $',size=24,)
cbar1=plt.colorbar(contor, ax=ax[1,0],orientation='vertical', fraction=0.1
,extend='min',)
cbar1.ax.tick_params(labelsize=24)
cbar1.set_label(label=r'$Z_{ 0 }  \mathrm{(\,m) \,}$',size=24,)
####
####for linear####
# norm1 = mpl.colors.Normalize(vmin=1e-8, vmax=0.00285/4)
# cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1), \
#      ax=ax[0,0],orientation='vertical',extend='max', fraction=0.1
# )
# cbar1.set_label(label=r'$Z_{ 0 }$',size=15,)
# cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1), \
#      ax=ax[1,0],orientation='vertical',extend='max', fraction=0.1
# )
# cbar1.set_label(label=r'$Z_{ 0 }$',size=15,)

norm2 = mpl.colors.Normalize(vmin=wspd_min, vmax=wspd_max)
# print(norm_log)

cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=my_cmap2),
ax=ax[0,1], orientation='vertical',  extend='max', fraction=0.1,

)
cbar2.ax.tick_params(labelsize=24)
# r'$\mathrm{(\,ms^{-1}) \,}$'
cbar2.set_label(label=r"Surface wind speed $\mathrm{(\,ms^{-1}) \,}$",size=24)
cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=my_cmap2),
ax=ax[1,1], orientation='vertical',  extend='max', fraction=0.1,
label="Wind intensity m/s")
cbar2.ax.tick_params(labelsize=24)
cbar2.set_label(label=r"Surface wind speed $\mathrm{(\,ms^{-1}) \,}$",size=24)
# fig.colorbar(Zo)

bbox_args = dict(boxstyle="round4", fc="0.9")



ax[0,0].annotate('a)', xy=(0.1, 0.95), xycoords='axes fraction',
             xytext=(0, -10), textcoords='offset points',
             ha="right", va="top",size=28,
             color='white'
             )
ax[0,1].annotate('b)', xy=(0.1, 0.95), xycoords='axes fraction',
             xytext=(0, -10), textcoords='offset points',
             ha="right", va="top",size=28,
             color='white'
             )
ax[1,0].annotate('c)', xy=(0.1, 0.95), xycoords='axes fraction',
             xytext=(0, -10), textcoords='offset points',
             ha="right", va="top",size=28,
             color='white'
             )
ax[1,1].annotate('d)', xy=(0.1, 0.95), xycoords='axes fraction',
             xytext=(0, -10), textcoords='offset points',
             ha="right", va="top",size=28,
             color='white'
             )



ax[0,0].set_title(r'Default case', size=28)
ax[0,1].set_title(r'Default case', size=28)
ax[1,0].set_title(r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.01', size=28)
ax[1,1].set_title(r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.01', size=28)
fig.tight_layout()

# h,l=ax[0].get_legend_handles_labels()
# ax[0].legend(h,l)
plt.savefig('/Users/lmatak/Desktop/Megn_paper_figs/CLZ_katrina.pdf',bbox_inches='tight')

# plt.show()