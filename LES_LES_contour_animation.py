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



fig, ax = plt.subplots(nrows=1, ncols=2,subplot_kw={'projection': crs.PlateCarree()},figsize=(16.3, 8.3))


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
agl=50
time_idx=0

idxs=np.arange(0,12)

sim_Dir1 = '/Users/lmatak/Downloads/two_domain_PBLS/d01/'
sim_Dir2='/Users/lmatak/Downloads/two_domain_PBLS/d02/'
domains=['d01','d02']
os.chdir(sim_Dir1)
ncfiles1=[]
ncfiles1 = list_ncfiles(sim_Dir1, ncfiles1)
os.chdir(sim_Dir2)
ncfiles2=[]
ncfiles2=list_ncfiles(sim_Dir2, ncfiles2)



# for doms in domains:
#     Input_Dir=sim_Dir+doms
#     os.chdir(Input_Dir)
#     ncfiles1=[]
#     ncfiles1 = list_ncfiles(Input_Dir, ncfiles)
#     ncfiles2=[]
# print(ncfiles)
what_to_plot='PM2_5_DRY'

Data1=[]
Data2=[]
Data=[Data1,Data2]
# for idx in idxs:  
idx=0
for i in range(len(ncfiles1)):

    os.chdir(sim_Dir1)
    Data1 = Dataset(ncfiles1[i])
    os.chdir(sim_Dir2)
    Data2=Dataset(ncfiles2[i])
    print(ncfiles1[i])
    print(ncfiles2[i])
    height1 = getvar(Data1, "height_agl",time_idx)
    height2 = getvar(Data2, "height_agl",time_idx)
    plotting_var1=getvar(Data1,what_to_plot,timeidx=0)
    plotting_var2=getvar(Data2,what_to_plot,timeidx=0)
    # wspd = getvar(Data, "wspd", timeidx = idx)
    # height = getvar(Data, "height_agl",timeidx = idx)
    plotting_var1=interplevel(plotting_var1,height1,agl)
    plotting_var2=interplevel(plotting_var2,height2,agl)

    
    # wspd_500 = interplevel(wspd, height, agl)

    lvls=[]
    lats1, lons1 = latlon_coords(plotting_var1)
    lats2, lons2 = latlon_coords(plotting_var2)
    

    ax[0].set_extent([float(lons1[0][0]),float(lons1[-1][-1]),float(lats1[0][0]),float(lats1[-1][-1])])
    ax[0].contourf(to_np(lons1), to_np(lats1), to_np(plotting_var1), 255,
        transform=crs.PlateCarree(), 
        cmap=cmap)
    ax[0].set_title(titles[0])
    
    ax[1].set_extent([float(lons2[0][0]),float(lons2[-1][-1]),float(lats2[0][0]),float(lats2[-1][-1])])
    ax[1].contourf(to_np(lons2), to_np(lats2), to_np(plotting_var2), 255,
        transform=crs.PlateCarree(), 
        cmap=cmap)
    ax[1].set_title(titles[1])



    # print(obs_stations_latitudes,obs_stations_longitudes)
    # ax[i].scatter(obs_stations_longitudes,obs_stations_latitudes,s=55,c='red',transform=crs.PlateCarree(), )
    ax[0].scatter(obs_stat_sim_lons,obs_stat_sim_lats,s=55,c='blue',transform=crs.PlateCarree(), )
    ax[1].scatter(obs_stat_sim_lons,obs_stat_sim_lats,s=55,c='blue',transform=crs.PlateCarree(), )
    # if i >=1:
    lons = [float(lons2[0][0]), float(lons2[0][0]), float(lons2[-1][-1]), float(lons2[-1][-1])]
    lats = [float(lats2[-1][-1]), float(lats2[0][0]),float(lats2[0][0]),float(lats2[-1][-1])]
    ring = LinearRing(list(zip(lons, lats)))
    ax[0].add_geometries([ring], crs.PlateCarree(), facecolor='none', edgecolor='white',linewidth=3.5)

    norm1 = mpl.colors.Normalize(vmin=0, vmax=np.amax(plotting_var1))


#     plt.gca().add_patch(Rectangle((0.1,0.1),-96.808891, 33.779167,linewidth=12,edgecolor='r',facecolor='none'))

    cbar=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=cmap),
    cax=cax, orientation='horizontal',  extend='neither',
    label=what_to_plot+" at 50m")
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

# h,l=ax[0].get_legend_handles_labels()
# ax[0].legend(h,l)

