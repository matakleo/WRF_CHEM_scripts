import os
import glob
import csv
import numpy as np
import cartopy.crs as crs
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.feature as cfeature
import matplotlib.colors as colors
from matplotlib import cm
from all_functions import Extract_by_name,Extract_the_shit2
# proj=crs.LambertConformal(central_longitude=-100.1, central_latitude=35.0,standard_parallels=[45,25])
proj=crs.PlateCarree()
# projection = ccrs.LambertConformal(central_longitude=-105,central_latitude=45,standard_parallels=[50,40])

fig, ax = plt.subplots(nrows=1, ncols=1,subplot_kw={'projection': proj},figsize=(15.3, 7.3))

filezzz=8

cmap=plt.get_cmap('Reds')
path = '/Users/lmatak/Downloads/paper_case/contors/'
extension = 'csv'
os.chdir(path)
result = glob.glob('*.{}'.format(extension))
print(result)

lats=[]

file = open(result[filezzz])
print(result[filezzz])
values_to_plot=[]
csvreader = csv.reader(file)
header=next(csvreader)
longs=header[1:]
for row in csvreader:
    lats.append(row[0])
    values_to_plot.append(row[1:])

longs=np.array(longs).astype(np.float)
lats=np.array(lats).astype(np.float)
values_to_plot=np.array(values_to_plot).astype(np.float)

# ax.stock_img()
ax.coastlines('110m', linewidth=0.8)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.OCEAN)
print(([longs[0],longs[-1],lats[-1],lats[0]]))
print('max=',np.amax(values_to_plot),'min=',np.amin(values_to_plot), 'mean=',np.mean(values_to_plot))
ax.set_extent([longs[-1],longs[0],lats[0],lats[-1]])

###get the measuring stations###

real_data_file='/Users/lmatak/Desktop/WRF_chem_scripts/wrf_chem_real_data/xlsx/measureing_locations.csv'

obs_stations_longitudes =[]
obs_stations_latitudes=[]
obs_stat_sim_lats=[]
obs_stat_sim_lons=[]
obs_stations_longitudes=Extract_the_shit2(real_data_file,obs_stations_longitudes,'LON')
obs_stations_latitudes=Extract_the_shit2(real_data_file,obs_stations_latitudes,'LAT')
obs_stat_sim_lons=Extract_the_shit2(real_data_file,obs_stat_sim_lons,'LON_sim')
obs_stat_sim_lats=Extract_the_shit2(real_data_file,obs_stat_sim_lats,'LAT_sim')
print(obs_stations_latitudes,obs_stations_longitudes)
ax.scatter(obs_stations_longitudes,obs_stations_latitudes,s=30,c='red')
ax.scatter(obs_stat_sim_lons,obs_stat_sim_lats,s=30,c='blue')




###get the measuring stations###

# ax.set_title(result[filezzz])
ax.set_title('Continental US')
im_cbar=ax.contourf(longs,lats,values_to_plot,225,transform=crs.PlateCarree(), 
        cmap=cmap) #,vmin=wmin_rad,vmax=wmax_rad,cmap=cmap2)

divnorm = colors.TwoSlopeNorm(vmin=0, vcenter=22, vmax=np.amax(values_to_plot))

cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=divnorm, cmap=cmap),
ax=ax, orientation='horizontal',  extend='both', 
            )

ax.text(0.95, -0.06, 'max='+str(np.amax(values_to_plot))+', min='+str(np.amin(values_to_plot))+', mean='+str(np.mean(values_to_plot)),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=15)


cbar1=plt.colorbar(im_cbar)


plt.show()

