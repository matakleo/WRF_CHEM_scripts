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


fig, ax = plt.subplots(nrows=1, ncols=2)



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
# print(np.average(z)
for i in range(len(nh3)):
    lvls.append(np.average(z[i]))
    chem_nh3.append(np.average(nh3[i]))
    chem_no2.append(np.average(no2[i]))
    chem_hno3.append(np.average(hno3[i]))
    chem_o3.append(np.average(o3[i]))
    chem_co.append(np.average(co[i]))
    chem_so2.append(np.average(so2[i]))

print(len(chem_nh3),len(chem_no2),len(z))
ax[0].plot(chem_nh3,lvls,label='NH3')
ax[0].plot(chem_no2,lvls,label='NO2')
ax[0].plot(chem_hno3,lvls,label='HNO3')
ax[0].plot(chem_so2,lvls,label='SO2')

h,l=ax[0].get_legend_handles_labels()
ax[0].legend(h,l)
ax[1].plot(chem_co,lvls,label='CO')
ax[1].plot(chem_o3,lvls,label='O3')
plt.legend()
plt.show()