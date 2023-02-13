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

wspd=np.arange(4,15,0.1)
starting_km=50
exch_plot=[]
for wspd_mag in wspd:
    if wspd_mag>5:
        exch_value=(np.maximum((10-wspd_mag)/5*starting_km,0))
    else:exch_value=(starting_km)
        # print(exch_value)
    exch_plot.append(exch_value)
    print(wspd_mag,exch_value)
plt.scatter(wspd,exch_plot)
plt.xlabel('wspd')
plt.ylabel('eddy exch coeff')
plt.show()
            

