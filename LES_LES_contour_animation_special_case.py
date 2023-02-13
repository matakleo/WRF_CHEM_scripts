from turtle import right
from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)
from all_functions import Extract_Track_Data,list_ncfiles,Extract_the_shit2
from cartopy.mpl.gridliner import LongitudeFormatter, LATITUDE_FORMATTER
from cartopy.feature import NaturalEarthFeature
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import glob
from netCDF4 import Dataset
import cartopy.crs as crs
import numpy as np
import imageio
from matplotlib.patches import Rectangle
from natsort import natsorted
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import cartopy.feature as cfeature
from shapely.geometry.polygon import LinearRing








fig, ax = plt.subplots(nrows=1, ncols=1 ,subplot_kw={'projection': crs.PlateCarree()},figsize=(16.3, 8.3))


#get observ stations positions data#
real_data_file='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data/xlsx/measureing_locations.csv'

obs_stations_longitudes =[]
obs_stations_latitudes=[]
obs_stat_sim_lats=[]
obs_stat_sim_lons=[]
obs_stations_longitudes=Extract_the_shit2(real_data_file,obs_stations_longitudes,'LON')
obs_stations_latitudes=Extract_the_shit2(real_data_file,obs_stations_latitudes,'LAT')
obs_stat_sim_lons=Extract_the_shit2(real_data_file,obs_stat_sim_lons,'LON_sim')
obs_stat_sim_lats=Extract_the_shit2(real_data_file,obs_stat_sim_lats,'LAT_sim')

cax = plt.axes([0.25, 0.27, 0.5, 0.025])


cmap=plt.get_cmap(
    'twilight_shifted')
cmap2=plt.get_cmap(
    'plasma'
)


titles=['domain 1','domain 2','domain 3','domain 4']
max_wspd=0
agl=500
time_idx=0

idxs=np.arange(0,12)

Input_Dir = '/Users/lmatak/Downloads/'
os.chdir(Input_Dir)
ncfiles=[]
ncfiles = list_ncfiles(Input_Dir, ncfiles)
print(ncfiles)
idx=0

for i in range(0,7):

    Data = Dataset(ncfiles[i])
    print(ncfiles[i])

    wspd = getvar(Data, "wspd", timeidx = idx)
    height = getvar(Data, "height_agl",timeidx = idx)
    wspd_500 = interplevel(wspd, height, agl)

    lvls=[]
    lats1, lons1 = latlon_coords(wspd_500)

    ax.set_extent([float(lons1[0][0]),float(lons1[-1][-1]),float(lats1[0][0]),float(lats1[-1][-1])])

    # # Get the cartopy mapping object
    cart_proj = get_cartopy(wspd_500)
    ax.contourf(to_np(lons1), to_np(lats1), to_np(wspd_500), 255, 
        transform=crs.PlateCarree(), 
        cmap=cmap)
    # ax.set_title(titles[i])



    # print(obs_stations_latitudes,obs_stations_longitudes)
    ax.scatter(obs_stations_longitudes,obs_stations_latitudes,s=55,c='red',transform=crs.PlateCarree(), )
    ax.scatter(obs_stat_sim_lons,obs_stat_sim_lats,s=55,c='blue',transform=crs.PlateCarree(), )



#     plt.gca().add_patch(Rectangle((0.1,0.1),-96.808891, 33.779167,linewidth=12,edgecolor='r',facecolor='none'))
    norm1 = mpl.colors.Normalize(vmin=0, vmax=np.amax(wspd_500))


    cbar=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap),
    cax=cax, orientation='horizontal',  extend='neither',
    label="wspd at 500m")
    plt.savefig(f"/Users/lmatak/Desktop/WRF_chem_scripts/boundary_contours_snapshots/fig_{i}.png",bbox_inches='tight')
    print(f"done with fig_{i}")

filenames=[]
for name in glob.glob('/Users/lmatak/Desktop/WRF_chem_scripts/boundary_contours_snapshots/fig_*'):
    filenames.append(name)
filenames=natsorted(filenames)
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('/Users/lmatak/Desktop/WRF_chem_scripts/boundary_contours_snapshots/movie.gif', images, duration=0.2)

print(f"saved as movie.gif")


