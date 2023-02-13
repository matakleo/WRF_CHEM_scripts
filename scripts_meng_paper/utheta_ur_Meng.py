from re import X
from turtle import right
from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)

from all_functions import Extract_Track_Data,list_ncfiles
from cartopy.mpl.gridliner import LongitudeFormatter, LATITUDE_FORMATTER
from cartopy.feature import NaturalEarthFeature
import matplotlib as mpl
from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from netCDF4 import Dataset
import cartopy.crs as crs
import numpy as np
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import cartopy.feature as cfeature
import csv
import matplotlib.colors as colors
# Example of making your own norm.  Also see matplotlib.colors.
# From Joe Kington: This one gives two different linear ramps:

os.environ["PATH"]+=":/Library/TeX/texbin/"
# print(os.environ["PATH"])
plt.rcParams.update({
    "text.usetex":True,
    "font.family":'Times New Roman'
})
size=17




fig, ax = plt.subplots(nrows=4, ncols=3,figsize=(13.3, 10.3),sharex='col',sharey='row',tight_layout='True',)

bottom = cm.get_cmap('Reds', 128)
top = cm.get_cmap('Blues_r', 128)
newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       bottom(np.linspace(0, 1, 128))))
newcmp = ListedColormap(newcolors, name='OrangeBlue')


##here set 0 deg or 90 deg... 0 is 1, 90 is 2
#Lorenzo either 1 or 2..
#Maria YSU = 2
#dor MYJ 4, YSU 3
#Iota MYJ 1

cmap1=cm.get_cmap('Reds', 256)

cmap2=newcmp
wmin_tan,wmax_tan,wmin_rad,wmax_rad=0,0,0,0
PBLS=['YSU','YSU','MYJ']


####----------------------HERE MAKE THE CHANGE---------------------#####
####----------------------HERE MAKE THE CHANGE---------------------#####
# HNS=['Maria','Dorian'] 
HNS=['Dorian','Katrina']
####----------------------HERE MAKE THE CHANGE---------------------#####
####----------------------HERE MAKE THE CHANGE---------------------#####

# if HNS[0]=='Maria':
#     ncfile_num=2
#     fig_name='Mari_Dori'
# else:
#     ncfile_num=1
#     fig_name='Lore_Igor'

ncfile_num=3


CLS=['changeClz_0p0100','changeClz_1p0000','changeClz_100p0000']
Input_Dir='/Users/lmatak/Downloads/Meng_wrfout_vert_contors/wtf_vert_contours/'

title_names=[r'Clz = 0.01','Default',r'Clz = 100']


row_count=0
col_count=0

for HN in HNS:
    if HN=='Katrina': ncfile_num=4

    for cl in CLS:
        var_tan='/WRFONLY_NoTurb_8km_isftcflx_1_'+str(cl)+'/Tangential_Data/'
        var_rad='/WRFONLY_NoTurb_8km_isftcflx_1_'+str(cl)+'/Radial_Data/'
        Input_Dir_tan=Input_Dir+HN+var_tan
        Input_Dir_rad=Input_Dir+HN+var_rad


        ##plot the tangential
        os.chdir(Input_Dir_tan)
        ncfiles=[]
        ncfiles = list_ncfiles (Input_Dir_tan, ncfiles)



        file = open(ncfiles[ncfile_num])

        csvreader = csv.reader(file)
        header = next(csvreader)
        header=np.array(header[1:-1]).astype(np.float)
        zero_idx= np.where(header==0)
        zero_idx=int(zero_idx[0])
        # print(ncfiles)
        # print(ncfiles[ncfile_num])
        # print(header[zero_idx:])
        rows = []
        z=[]
        last_idx=-1
        # if PBL=='YSU':
        #     last_idx=-2
        for row in csvreader:
            
            z.append(row[0])
            # rows.append(row[zero_idx+1:last_idx])
            rows.append(row[1:-2])
    
        
        z=np.array(z).astype(np.float)
        rows=np.array(rows).astype(np.float)
        
        
        if np.amax(rows)>=wmax_tan:wmax_tan=np.amax(rows)
        if np.amin(rows)<=wmin_tan:wmin_tan=np.amin(rows)
        # print(rows.shape)
        # print(HN+' ,'+cl+' ,row: ',row_count,' ,col: ',col_count)
        print('len of x:',len(header[zero_idx:]),' len of y:',len(z),' len of z: ',len(rows[0]))
        im_cbar1=ax[row_count,col_count].contourf(to_np(header[zero_idx:]),to_np(z),to_np(rows),255,vmin=wmin_tan,vmax=wmax_tan,cmap=cmap1,)

        ax[row_count,col_count].set_xticks([0,25,50,75,100,125,150,175,200])
        ax[row_count,col_count].set_yticks([500,1000,1500,2000])

        ax[row_count+1,col_count].set_xticks([0,25,50,75,100,125,150,175,200])
        ax[row_count+1,col_count].set_yticks([500,1000,1500,2000])



        # plot the radial
        os.chdir(Input_Dir_rad)
        ncfiles=[]
        ncfiles = list_ncfiles (Input_Dir_tan, ncfiles)
        file = open(ncfiles[ncfile_num])
        # print(file)
        csvreader = csv.reader(file)
        header = next(csvreader)
        header=np.array(header[1:-1]).astype(np.float)
        zero_idx= np.where(header==0)
        zero_idx=int(zero_idx[0])
        # print(zero_idx)
        # print(header[zero_idx:])
        rows = []
        z=[]
        for row in csvreader:
            
            z.append(row[0])
            rows.append(row[1:-2])
    
        
        z=np.array(z).astype(np.float)
        rows=np.array(rows).astype(np.float)
        # print(rows[0])
        # print(col_count,np.amin(rows))
        if np.amax(rows)>=wmax_rad:wmax_rad=np.amax(rows)
        if np.amin(rows)<=wmin_rad:wmin_rad=np.amin(rows)

        im_cbar2=ax[row_count+1,col_count].contourf(to_np(header[zero_idx:]),to_np(z),to_np(rows),255,vmin=wmin_rad,vmax=wmax_rad,cmap=cmap2)

        if row_count==0 or 2:
            ax[row_count,col_count].set_title(HN+' '+title_names[col_count])
        
        # if col_count==1:
        #     ax[row_count,col_count].set_title(HN+' '+title_names[col_count]+' '+PBL+r' $u_{ \theta }$',size=size)
        #     ax[row_count+1,col_count].set_title(HN+' '+title_names[col_count]+' '+PBL+r' $u_{ r }$',size=size)
        # else:
        #     ax[row_count,col_count].set_title(HN+r'\_'+title_names[col_count]+r'\_'+PBL+r' $u_{ \theta }$',size=size)
        #     ax[row_count+1,col_count].set_title(HN+r'\_'+title_names[col_count]+r'\_'+PBL+r' $u_{ r }$',size=size)

        
        
        # ax[row_count+1,col_count].set_title(HN+'_'+title_names[col_count]+'_'+PBL+'_ur',size=9)


        col_count+=1
        # print('wmax tan=',wmax_tan)
        # print('row count=',row_count,' col count= ',col_count)
        if col_count==3:    
            # if wmin_tan<0:
            #     wmin_tan=-5
            if wmin_tan>=0:
                vcenter=wmin_tan+1
                vmin=0
            else:
                vcenter=0
                vmin=wmin_tan
            print('vmin= ',wmin_tan,' vmax= ',wmax_tan)
            divnorm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=wmax_tan)
            # print('wmax_tan, wmin_tan = ',wmax_tan,wmin_tan)
            # norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
            cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=divnorm, cmap=cmap2),
            ax=ax[row_count,2], orientation='vertical',  extend='both', 
            )
            cbar1.ax.tick_params(labelsize=size-4) 
            cbar1.set_label(r'Tangential Wind Speed $\mathrm{(\,ms^{-1}) \,}$', size=size-5.5)

            print('wmin_rad=',wmin_rad)
            divnorm = colors.TwoSlopeNorm(vmin=wmin_rad, vcenter=0, vmax=wmax_rad)

        
            cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=divnorm, cmap=cmap2),
            ax=ax[row_count+1,2], orientation='vertical',  extend='both',
            label=r'Radial Wind Speed $\mathrm{(\,ms^{-1}) \,}$')
            cbar2.ax.tick_params(labelsize=size-4) 
            cbar2.set_label(r'Radial Wind Speed $\mathrm{(\,ms^{-1}) \,}$', size=size-5.5)
            col_count=0
            row_count+=2
            wmin_tan,wmax_tan,wmin_rad,wmax_rad=0,0,0,0

                

ax[0,0].set_ylabel('Height (m)', size=size)
ax[1,0].set_ylabel('Height (m)', size=size)
ax[2,0].set_ylabel('Height (m)', size=size)
ax[3,0].set_ylabel('Height (m)', size=size)

ax[0,0].yaxis.set_tick_params(labelsize=size-2)
ax[1,0].yaxis.set_tick_params(labelsize=size-2)
ax[2,0].yaxis.set_tick_params(labelsize=size-2)
ax[3,0].yaxis.set_tick_params(labelsize=size-2)




ax[3,0].set_xlabel('Radius (km)', size=size)
ax[3,1].set_xlabel('Radius (km)', size=size)
ax[3,2].set_xlabel('Radius (km)', size=size)

ax[3,0].xaxis.set_tick_params(labelsize=size-2)
ax[3,1].xaxis.set_tick_params(labelsize=size-2)
ax[3,2].xaxis.set_tick_params(labelsize=size-2)


# ax[1,0].annotate(HNS[0], xy=(0.05, 0.8), xycoords='figure fraction',
#         xytext=(0, 0), textcoords='offset points',
#         ha="right", va="top",size=12,
#         rotation = 90
#         )

# print('saved as: fig17tan_and_rad_contors'+fig_name+'.png')
# plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/fig17tan_and_rad_contors'+fig_name+'.png',bbox_inches='tight')
plt.show()






# h,l=ax[0].get_legend_handles_labels()
# ax[0].legend(h,l)
