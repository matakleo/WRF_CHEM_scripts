from ssl import PEM_cert_to_DER_cert
from turtle import right
from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)
from all_functions import Extract_Track_Data,list_ncfiles
from cartopy.mpl.gridliner import LongitudeFormatter, LATITUDE_FORMATTER
from cartopy.feature import NaturalEarthFeature
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from netCDF4 import Dataset
import cartopy.crs as crs
import numpy as np
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import cartopy.feature as cfeature

proj=crs.LambertConformal(central_longitude=-100.1, central_latitude=35.0)
fig, ax = plt.subplots(nrows=1, ncols=2,subplot_kw={'projection': proj},figsize=(15.3, 7.3))

cmap=plt.get_cmap('Reds')
# cmap=plt.get_cmap(
#     'twilight_shifted')
# cmap=plt.get_cmap(
#     'plasma'
# )

var="PM2_5_DRY"

titles=['chem opt=10','chem opt=170']
max_PM=0
agl=100
time_idx=0
Input_Dir = '/Users/lmatak/Downloads/paper_case/'
os.chdir(Input_Dir)
ncfiles=[]
ncfiles = list_ncfiles(Input_Dir, ncfiles)
for i in range(len(ncfiles[0:1])):
    Data = Dataset(ncfiles[i])
    # print(ncfiles[i])
    height = getvar(Data, "height_agl",time_idx)
    PM = getvar(Data, var,time_idx)

    PM_vals=interplevel(PM,height,agl)
    if np.amax(PM_vals)>max_PM:
        max_PM=np.amax(PM_vals)
    # co_agl=interplevel(co,height,agl)

    print(PM_vals[23][110])
    # np.where(PM_vals[XLONG])
    # ax[i].stock_img()
#     ax[i].coastlines('110m', linewidth=0.8)
#     ax[i].add_feature(cfeature.LAND)
#     # ax[0].add_feature(cfeature.STATES)
#     # ax[i].add_feature(cfeature.OCEAN)

#     lats1, lons1 = latlon_coords(PM_vals)

#     print(([float(lons1[0][0]),float(lons1[0][-1]),float(lats1[0][0]),float(lats1[-1][0])]))
#     ax[i].set_extent([float(lons1[0][0]),float(lons1[0][-1]),float(lats1[0][0]),float(lats1[-1][0])])

#     cart_proj = get_cartopy(PM_vals[43:50])
#     # ax[i].plot(cart_proj)
#     # print(to_np(lons1))
#     ax[i].contourf(to_np(lons1), to_np(lats1), to_np(PM_vals), 255, 
#         transform=cart_proj, 
#         cmap=cmap)  #crs.PlateCarree()
# #     ax[i].set_title(titles[i])
# #     gl = ax[i].gridlines(crs=crs.PlateCarree(), draw_labels=True,
# #                         linewidth=0.2, color='black', alpha=0.2, linestyle='--')
# #     gl.top_labels = False
# #     gl.right_labels = False
# #     gl.xlabel_style= {'size': 12, 'color': 'black'}  
# #     gl.ylabel_style= {'size': 12, 'color': 'black'}
# # # ax[1].contourf(to_np(lons1), to_np(lats1), to_np(co_agl), 255, 
# # #     transform=crs.PlateCarree(), 
# # #     cmap=cmap)
# # norm1 = mpl.colors.Normalize(vmin=0, vmax=max_PM)
# # cax = plt.axes([0.125, 0.1, 0.75, 0.025])
# # cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap),
# # cax=cax, orientation='horizontal',  extend='both',
# # label=var+" @"+str(agl)+"m")
# # cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=cmap2),
# # ax=ax[1], orientation='horizontal',  extend='both',
# # label="co ppmv")

    





# # h,l=ax[0].get_legend_handles_labels()
# # ax[0].legend(h,l)

# plt.show()