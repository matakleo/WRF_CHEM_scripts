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

fig, ax = plt.subplots(nrows=1, ncols=2,subplot_kw={'projection': crs.PlateCarree()},figsize=(16.3, 8.3))

my_cmap1 = copy.copy(mpl.cm.get_cmap('twilight_shifted')) # copy the default cmap
my_cmap1.set_bad((0,0,0))

os.environ["PATH"]+=":/Library/TeX/texbin/"
print(os.environ["PATH"])
plt.rcParams.update({
    "text.usetex":True,
    "font.family":'Times New Roman'
})
dirs=['Default','Reduced_PBL']
label_names=['Default PBL Depth','Reduced PBL Depth']
dir_num=0
i=0
file_in_dir=0
height_lvl=0
# var_to_plot='TKE'
var_to_plot='wspd'

text_size=25

csfont = {'fontname':'Times New Roman'}

total_counter=0
row=0
for file_num in range(0,7):
    for idx in range(0,6):
# for file_num in range(0,1):
#     for idx in range(0,1):
        col=0
        dir_num=0

        for dir in dirs:
            if total_counter==0:
                gl = ax[col].gridlines(crs=crs.PlateCarree(), draw_labels=True,
                    linewidth=0.2, color='black', alpha=0.2, linestyle='--')
                gl.top_labels = False
                gl.right_labels = False
                gl.xlabel_style= {'size': text_size, 'color': 'black'}  
                gl.ylabel_style= {'size': text_size, 'color': 'black'}
            
            print('ncfile num:',file_num,'/7')
            print('time idx num:',idx,'/5')
            print('dir :',dir)

            ZNT=[]
            Input_Dir = '/Users/lmatak/Downloads/CONTORS_FOR_POSTER/'+dir
            # Input_Dir = '/Users/lmatak/Downloads/URBAN_SCHEME_CONTOURING/different_times/'+dir
            os.chdir(Input_Dir)
            ncfiles=[]
            ncfiles = list_ncfiles(Input_Dir, ncfiles)
            print('the directory is: ',Input_Dir)         
            Data = Dataset(ncfiles[file_num])
            print('the ncfile is: ',ncfiles[file_num])
            print('----------------------------')
            LAI=np.array(getvar(Data, "LANDMASK", timeidx = idx))
            lakemask=np.array(getvar(Data, "LAKEMASK", timeidx = idx))
            ZNT=np.array(getvar(Data, "U10", timeidx = idx))



            wspd=np.array(getvar(Data, "wspd", timeidx = idx))
            # ust=np.array(getvar(Data, "tke", timeidx = idx))
            MASKING=np.array(getvar(Data, "LU_INDEX", timeidx = idx))
            u10=getvar(Data, "U10", timeidx = idx)
            v10=getvar(Data, "V10", timeidx = idx)

            total_wind=np.sqrt(u10**2+v10**2)
            vmin_set=0
            vmax_set=45


            height = (getvar(Data, "height_agl",timeidx = idx))
            lats1, lons1 = latlon_coords(height[0])
            height=int(np.mean(height[height_lvl]))
            # total_wind[MASKING!=13]=nan
            
            ax[col].stock_img()

            ax[col].contourf(to_np(lons1),to_np(lats1), (total_wind), 50,  vmin=vmin_set,vmax=vmax_set,     transform=crs.PlateCarree(), 
                cmap=my_cmap1)    
            ax[col].set_extent([-85,-72,8,20])    

            #TITLE%

            # ax[col].set_title(label_names[dir_num]+' snapshot= '+str(file_num))
            # ax[col].background_patch.set_facecolor('grey')  
            
            dir_num+=1
            col+=1

            
        plt.subplots_adjust(bottom=0.2,)
        
        norm1 = mpl.colors.Normalize(vmin=vmin_set,vmax=vmax_set)

                        #xstart ystart xend yend#
        # if file_num==0:
        if total_counter==0:
            cax = plt.axes([0.1, 0.090, 0.85, 0.051])      
            cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1),
            cax=cax, orientation='horizontal',  extend='max', fraction=0.03,
            )

            ax[0].set_title('Default PBL Depth', **csfont,size=text_size)
            # ax[0,2].set_title(r'Increased PBL height' ,size=size)
            ax[1].set_title('Reduced PBL Depth',**csfont,size=text_size)
            cbar1.ax.tick_params(labelsize=text_size) 
            cbar1.set_label(r'Wind Speed $\mathrm{(\,ms^{-1}) \,}$', size=text_size)

        plt.savefig(f"/Users/lmatak/Desktop/leo_python_scripts/Poster_figs/created_figs/for_animation/DENVER_anim_fig_{total_counter}.png",bbox_inches='tight')
        total_counter+=1
        print('saved fig number ',total_counter)



   


# plt.show()