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


fig, ax = plt.subplots(nrows=1, ncols=2,subplot_kw={'projection': crs.PlateCarree()},figsize=(12.3, 7.3))


cmap=plt.get_cmap(
    'twilight_shifted')
cmap2=plt.get_cmap(
    'plasma'
)

agl=500

Input_Dir = '/Users/lmatak/Downloads/chem_out/'
os.chdir(Input_Dir)
ncfiles=[]
ncfiles = list_ncfiles(Input_Dir, ncfiles)

Data = Dataset(ncfiles[0])
height = getvar(Data, "height_agl")
z=getvar(Data,"z")
lvls=[]
chem_nh3=[]
chem_no2=[]
chem_hno3=[]
chem_o3=[]
chem_pm10=[]
chem_co=[]
chem_so2=[]
hno3=getvar(Data,"hno3")
no2=getvar(Data,"no2")
nh3=getvar(Data,"nh3")
o3=getvar(Data,'o3')
pm10=getvar(Data,'PM10')
co=getvar(Data,'co')
so2=getvar(Data,'so2')
# co3=getvar(Data,'co3')
# print(np.average(z)

o3_agl=interplevel(o3,height,agl)
co_agl=interplevel(co,height,agl)


ax[0].stock_img()
ax[0].coastlines('50m', linewidth=0.8)
ax[0].add_feature(cfeature.LAND)
ax[0].add_feature(cfeature.OCEAN)
ax[1].stock_img()
ax[1].coastlines('50m', linewidth=0.8)
ax[1].add_feature(cfeature.LAND)
ax[1].add_feature(cfeature.OCEAN)

lats1, lons1 = latlon_coords(o3_agl)
slp_coord_lat= float(lats1[[100]][0][0])
slp_coord_long=float(lons1[0][[100]])

ax[0].set_extent([slp_coord_long+15,slp_coord_long-15,slp_coord_lat-15,slp_coord_lat+15])
ax[1].set_extent([slp_coord_long+15,slp_coord_long-15,slp_coord_lat-15,slp_coord_lat+15])
# Get the cartopy mapping object
cart_proj = get_cartopy(o3_agl)
ax[0].contourf(to_np(lons1), to_np(lats1), to_np(o3_agl), 255, 
    transform=crs.PlateCarree(), 
    cmap=cmap)
ax[1].contourf(to_np(lons1), to_np(lats1), to_np(co_agl), 255, 
    transform=crs.PlateCarree(), 
    cmap=cmap)
norm1 = mpl.colors.Normalize(vmin=0, vmax=np.amax(o3))
norm2 = mpl.colors.Normalize(vmin=0, vmax=np.amax(co))

cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap),
ax=ax[0], orientation='horizontal',  extend='both',
label="03 ppmv")
cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=cmap2),
ax=ax[1], orientation='horizontal',  extend='both',
label="co ppmv")

    






h,l=ax[0].get_legend_handles_labels()
ax[0].legend(h,l)

plt.show()