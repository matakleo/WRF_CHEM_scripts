import xarray as xr
import numpy as np
from wrf import ll_to_xy
from netCDF4 import Dataset
# Load the WRF output file into a xarray dataset
ds = xr.open_dataset('/Users/lmatak/Downloads/wes-coldens/wrfout_for_locations')
data='/Users/lmatak/Downloads/wes-coldens/wrfout_for_locations'
data=Dataset(data)
# Extract the latitude and longitude data arrays
lats = ds['XLAT'].values
lons = ds['XLONG'].values


# Given latitude and longitude coordinates
given_lat = 29.767996
given_lon = -95.220582

print(ll_to_xy(data,given_lat,given_lon))

# # Calculate the Euclidean distance
# dists = np.sqrt((lats - given_lat)**2 + (lons - given_lon)**2)

# # Find the index of the minimum distance
# min_index = np.argmin(dists)

# # Flatten the arrays to 1D
# lats = lats.flatten()
# lons = lons.flatten()

# # Get the closest grid point
# closest_lat = lats[min_index]
# closest_lon = lons[min_index]

# # print(min_index)
# print(lats.shape[0])

# print(np.unravel_index(min_index, lats.shape[0]))

# # Extract the data for the closest grid point
# # data = ds.sel(south_north=closest_lat, west_east=closest_lon, method='nearest')