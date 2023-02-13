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




fig, ax = plt.subplots(nrows=2, ncols=2,subplot_kw={'projection': crs.PlateCarree()},figsize=(11.3, 10.3),dpi=500)
fig.subplots_adjust(hspace=0.01)

cmap=plt.get_cmap(
    'twilight_shifted')
cmap2=plt.get_cmap(
    'turbo'
)


dirs=['Iota_ysu_default','Iota_ysu_250']
dir_num=0

wspd_min=0
wspd_max=55

hpbl_min=0
hpbl_max=1350


agl=70
time_idx=5
row=0
i=0
for dir in dirs:
    ZNT=[]
    Input_Dir = '/Users/lmatak/Downloads/FIRST_PAPER_CODE_CHANGES/'+dir
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)
    print(Input_Dir)

    wspd=[]
    idx=5

    Data = Dataset(ncfiles[0])

    u10=getvar(Data, "U10", timeidx = idx)
    v10=getvar(Data, "V10", timeidx = idx)
    total_wind=np.sqrt(u10**2+v10**2)

    hpbl=np.array(getvar(Data, "PBLH", timeidx = idx))

    height = (getvar(Data, "height_agl",timeidx = idx))
    
    total_wind=np.array(total_wind)

  
    lats1, lons1 = latlon_coords(height[0])

    # move_conts_to_right_longs=10
    # lats_move=4.5
    # ax[row,i].set_extent([float(lons1[0][0])+14, \
    #     float(lons1[-1][-1])-move_conts_to_right_longs, \
    #         float(lats1[0][0])+lats_move,float(lats1[-1][-1])-lats_move])
    # ax[row,i+1].set_extent([float(lons1[0][0])+14,\
    #     float(lons1[-1][-1])-move_conts_to_right_longs,\
    #         float(lats1[0][0])+lats_move,float(lats1[-1][-1])-lats_move])

        ####################################
    ### SET THE ZNT MIN AND MAX FOR PLOTTING ###
        ####################################
    

  
    # FOR LOG SCALE#
    # contor=ax[row,i].pcolormesh(to_np(lons1),to_np(lats1), \
    #              ZNT,norm=LogNorm(vmin=1e-5/16,vmax=0.00285),cmap=my_cmap1,shading='auto'
    #              ,snap='True',\
    #              transform=crs.PlateCarree(), 
    #     )
    
    ##FOR LINEAR###
    contor=ax[row,i].contourf(to_np(lons1),to_np(lats1), (hpbl) ,255,vmin=hpbl_min,vmax=hpbl_max,cmap=my_cmap1,
                 transform=crs.PlateCarree(),
                  
        )
    
    ax[row,i+1].contourf(to_np(lons1),to_np(lats1), (total_wind), 255,  vmin=wspd_min,vmax=wspd_max,     transform=crs.PlateCarree(), 
        cmap=my_cmap2,)
    ax[row,i+1].background_patch.set_facecolor('black')    
    ax[row,i].background_patch.set_facecolor('black')  

    
    
    # ax[row,i].set_title(dirs[dir_num])

    
    row+=1

###for log##
# cbar1=plt.colorbar(contor, ax=ax[0,0],orientation='vertical', fraction=0.1
# ,extend='min')
# print('Im here',cbar1.ax.get_yticklabels())
# cbar1.ax.tick_params(labelsize=17)
# cbar1.set_label(label=r'$z _{ 0 }$  $\mathrm{ (\,m) \,} $',size=22 ,)
# cbar1=plt.colorbar(contor, ax=ax[1,0],orientation='vertical', fraction=0.1
# ,extend='min',)
# cbar1.ax.tick_params(labelsize=17)
# cbar1.set_label(label=r'$z_{ 0 }$  $\mathrm{ (\,m) \,}$',size=22,)
####
###for linear####
norm1 = mpl.colors.Normalize(vmin=hpbl_min, vmax=hpbl_max)
cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1), \
     ax=ax[0,0],orientation='vertical',extend='max', fraction=0.1
)
cbar1.ax.tick_params(labelsize=20)
cbar1.set_label(label=r'PBL height (m)',size=20,)
cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1), \
     ax=ax[1,0],orientation='vertical',extend='max', fraction=0.1
)
cbar1.ax.tick_params(labelsize=20)
cbar1.set_label(label=r'PBL height (m)',size=20,)

# cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1), \
#      ax=ax[2,0],orientation='vertical',extend='max', fraction=0.1
# )
# cbar1.ax.tick_params(labelsize=20)
# cbar1.set_label(label=r'PBL height (m)',size=20,)

norm2 = mpl.colors.Normalize(vmin=wspd_min, vmax=wspd_max)
# print(norm_log)

cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=my_cmap2),
ax=ax[0,1], orientation='vertical',  extend='max', fraction=0.1,)
cbar2.ax.tick_params(labelsize=20)
# r'$\mathrm{(\,ms^{-1}) \,}$'
cbar2.set_label(label=r"Surface wind speed $\mathrm{(m \:s^{-1}) \,}$",size=20)

cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=my_cmap2),
ax=ax[1,1], orientation='vertical',  extend='max', fraction=0.1,
label="Wind intensity m/s")
cbar2.ax.tick_params(labelsize=20)
cbar2.set_label(label=r"Surface wind speed $\mathrm{(m\: s^{-1}) \,}$",size=20)

# cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=my_cmap2),
# ax=ax[2,1], orientation='vertical',  extend='max', fraction=0.1,
# label="Wind intensity m/s")
# cbar2.ax.tick_params(labelsize=20)
# cbar2.set_label(label=r"Surface wind speed $\mathrm{(m\: s^{-1}) \,}$",size=20)
# fig.colorbar(Zo)


### TITLES ####



ax[0,0].set_title(r'a) Default case',size=20)
ax[0,1].set_title(r'b) Default case',size=20)

ax[1,0].set_title(r'c) PBL Height = 250m',size=20)
ax[1,1].set_title(r'd) PBL Height = 250m',size=20)



# ax[2,0].set_title(r'e) PBL Height = 1000m',size=20)
# ax[2,1].set_title(r'f) PBL Height = 1000m',size=20)


bbox_args = dict(boxstyle="round4", fc="0.9")


#             ### annotations on the left
# ax[0,0].annotate('h = 250m', xy=(-0.1, 0.65), xycoords='axes fraction',
# xytext=(0, -10), textcoords='offset points',
# ha="right", va="top",size=20, rotation = 90,
# color='black'
# )        

# ax[1,0].annotate('Default case', xy=(-0.1, 0.75), xycoords='axes fraction',
# xytext=(0, -10), textcoords='offset points',
# ha="right", va="top",size=20, rotation = 90,
# color='black'

# )    


# ax[2,0].annotate('h = 1000m', xy=(-0.1, 0.65), xycoords='axes fraction',
# xytext=(0, -10), textcoords='offset points',
# ha="right", va="top",size=20, rotation = 90,
# color='black'
# )    

# #### sublot indicies ####

# ax[0,0].annotate('a)', xy=(0.11, 0.95), xycoords='axes fraction',
#              xytext=(0, -10), textcoords='offset points',
#              ha="right", va="top",size=28,
#              color='black'
#              )







# ax[0,1].annotate('b)', xy=(0.12, 0.95), xycoords='axes fraction',
#              xytext=(0, -10), textcoords='offset points',
#              ha="right", va="top",size=28,
#              color='black'
#              )
# ax[1,0].annotate('c)', xy=(0.1, 0.95), xycoords='axes fraction',
#              xytext=(0, -10), textcoords='offset points',
#              ha="right", va="top",size=28,
#              color='black'
#              )
# ax[1,1].annotate('d)', xy=(0.12, 0.95), xycoords='axes fraction',
#              xytext=(0, -10), textcoords='offset points',
#              ha="right", va="top",size=28,
#              color='black'
#              )

# ax[2,0].annotate('e)', xy=(0.1, 0.95), xycoords='axes fraction',
# xytext=(0, -10), textcoords='offset points',
# ha="right", va="top",size=28,
# color='black'
# )

# ax[2,1].annotate('f)', xy=(0.12, 0.95), xycoords='axes fraction',
# xytext=(0, -10), textcoords='offset points',
# ha="right", va="top",size=28,
# color='black'
# )


fig.tight_layout()

# h,l=ax[0].get_legend_handles_labels()
# ax[0].legend(h,l)
plt.savefig('/Users/lmatak/Desktop/contours_paper_fig.png',bbox_inches='tight')

# plt.show()