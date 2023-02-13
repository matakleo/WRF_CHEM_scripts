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

fig, ax = plt.subplots(nrows=2, ncols=2,subplot_kw={'projection': crs.PlateCarree()},figsize=(14.3, 8.3))

my_cmap1 = copy.copy(mpl.cm.get_cmap('bwr')) # copy the default cmap
my_cmap1.set_bad((0,0,0))
cmap=plt.get_cmap(
    'bwr')
cmap2=plt.get_cmap(
    'bwr'
)


dirs=['test12','test21',]#'clz_1000','clz_100']
dir_num=0
i=0

three_dom_lats=np.array([29.771469116210938,29.739097595214844,29.67430877685547,29.717498779296875,29.68511199951172])
three_dom_lons=np.array([-95.22166442871094,-95.25896453857422,-95.1346435546875,-95.34598541259766,-95.29625701904297])
mid_downtown_lon=-95.3621823
mid_downtown_lat=29.7585786
mid_downtown=[-95.3621823,29.7585786]
# print(np.sort(poly_corners,0))

three_dom_lats=np.array([29.67430877685547,29.771469116210938,29.739097595214844,29.68511199951172,29.717498779296875])
three_dom_lons=np.array([-95.1346435546875,-95.22166442871094,-95.25896453857422,-95.29625701904297,-95.34598541259766])
poly_corners = np.zeros((len(three_dom_lats), 2), np.float64)
# print(poly_corners)
poly_corners[:,0] = three_dom_lons
poly_corners[:,1] = three_dom_lats



row=0
for dir in dirs:
    ZNT=[]
    Input_Dir = '/Users/lmatak/Downloads/URBAN_SCHEME_CONTOURING/'+dir
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)
    print('the directory is: ',Input_Dir)
    idx=0

    Data = Dataset(ncfiles[0])
    print('the ncfile is: ',ncfiles[0])
    print('----------------------------')
    LAI=np.array(getvar(Data, "LANDMASK", timeidx = idx))
    lakemask=np.array(getvar(Data, "LAKEMASK", timeidx = idx))
    ZNT=np.array(getvar(Data, "U10", timeidx = idx))
    TEMP=np.array(getvar(Data, "AKHS", timeidx = idx))

    
    wspd=np.array(getvar(Data, "wspd", timeidx = idx))
    
    u10=getvar(Data, "U10", timeidx = idx)
    v10=getvar(Data, "V10", timeidx = idx)
    total_wind=np.sqrt(u10**2+v10**2)
    # total_wind=TEMP
    height = (getvar(Data, "height_agl",timeidx = idx))
    total_wind=wspd[0]
    # interp_wspd=interplevel(wspd,height,500)
    print('min wspd=',float(np.min(total_wind)),'max wspd=',float(np.max(total_wind)), 'avg total_wind=',float(np.mean(total_wind)))


    lats1, lons1 = latlon_coords(height[0])

    (Eye_Slp, Eye_Idx, Eye_Xlat, Eye_Xlon) = hurricane_eye_3(Data, 0)



    # contor=ax[row,i].pcolormesh(to_np(lons1),to_np(lats1), \
    #                 ZNT,norm=LogNorm(vmin=ZNT.min(),vmax=ZNT.max()),cmap=my_cmap1,shading='auto'
    #                 ,snap='True',\
    #                 transform=crs.PlateCarree(), 
    #         )
    ax[row,i].contourf(to_np(lons1),to_np(lats1), (ZNT), 250,  vmin=ZNT.min(),vmax=5,     transform=crs.PlateCarree(), 
        cmap=cmap2)
    
    ax[row,i].scatter(mid_downtown_lon,mid_downtown_lat,s=55,c='red',transform=crs.PlateCarree())
    # ax[row,i].scatter()


    
    # ax[row,i+1].contourf(to_np(lons1),to_np(lats1), (total_wind), 250,  vmin=total_wind.min()+2,vmax=total_wind.max()-3,     transform=crs.PlateCarree(), 
    #     cmap=cmap2)
    ax[row,i+1].contourf(to_np(lons1),to_np(lats1), (total_wind), 250,  vmin=3,vmax=7,     transform=crs.PlateCarree(), 
        cmap=cmap2)    
    ax[row,i+1].scatter(three_dom_lons,three_dom_lats,s=55,c='blue',transform=crs.PlateCarree())
    ax[row,i].set_title(dirs[dir_num])
    ax[row,i+1].set_title(dirs[dir_num])
    dir_num+=1
    row+=1

    


norm1 = mpl.colors.Normalize(vmin=ZNT.min(), vmax=5 )#ZNT.max())
norm2 = mpl.colors.Normalize(vmin=3, vmax=7)


# cbar1=plt.colorbar(contor, ax=ax[0,0],orientation='vertical', fraction=0.1
# ,extend='min',label='z0')
# cbar1=plt.colorbar(contor, ax=ax[1,0],orientation='vertical', fraction=0.1
# ,extend='min',label='z0')

cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap2),
ax=ax[0,0], orientation='vertical',  extend='max', fraction=0.1,
label="U10 m ")
cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap2),
ax=ax[1,0], orientation='vertical',  extend='max', fraction=0.1,
label="U10 m ")


cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=cmap2),
ax=ax[0,1], orientation='vertical',  extend='max', fraction=0.1,
label="surface wspd ")
cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=cmap2),
ax=ax[1,1], orientation='vertical',  extend='max', fraction=0.1,
label="surface wspd ")


# ax[0,0].add_patch(mpatches.Rectangle(xy=mid_downtown, width=0.3, height=0.15,
#                                     facecolor='black',
#                                     alpha=0.4,
#                                     transform=crs.PlateCarree())
#                  )
# ax[0,1].add_patch(mpatches.Rectangle(xy=[-95.384, 29.648], width=0.3, height=0.15,
#                                     facecolor='black',
#                                     alpha=0.4,
#                                     transform=crs.PlateCarree())
#                  )  
# ax[1,1].add_patch(mpatches.Rectangle(xy=[-95.384, 29.648], width=0.3, height=0.15,
#                                     facecolor='black',
#                                     alpha=0.4,
#                                     transform=crs.PlateCarree())
#                  )          
# ax[1,0].add_patch(mpatches.Rectangle(xy=[-95.384, 29.648], width=0.3, height=0.15,
#                                     facecolor='black',
#                                     alpha=0.4,
#                                     transform=crs.PlateCarree())
#                  )                           

# poly = Polygon(poly_corners, closed=True, ec='blue', fill=True, lw=3, fc=None, transform=crs.PlateCarree())
# ax[1,1].add_patch(poly)
# ax[0,1].add_geometries([polygon1], crs=crs.PlateCarree(), facecolor='b', edgecolor='red', alpha=0.8)

# ax[1,1].add_patch(polygon1,transform=)   
# # fig.colorbar(Zo)


# fig.tight_layout()

# ax[0,0].annotate('MgII', xy=(-95.0, 69.5), xycoords='data', annotation_clip=False)
# ax[0,0].annotate('local max', xy=(0, 0),  xycoords='figure',
#             xytext=(0, 0), textcoords='figure fraction',
#             arrowprops=dict(facecolor='black', shrink=0.05),
#             horizontalalignment='right', verticalalignment='top',
#             )
plt.show()