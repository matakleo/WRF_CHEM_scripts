import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# Open WRF input file
file_path = '/Users/lmatak/Downloads/all/WRF_CHEM_CONTOURING/Jun_wrfinps/wrfinput_d03'
file = nc.Dataset(file_path)

# Extract variables (assuming temperature and wind speed variables are named 'T' and 'U' respectively)
temp = file.variables['T'][:]
wind_speed = file.variables['U'][:]

# Get latitude and longitude values
lat = file.variables['XLAT'][:]
lon = file.variables['XLONG'][:]

# Close file
file.close()

# Plot temperature
plt.contourf(lon, lat, temp[0,:,:], cmap='coolwarm')
plt.colorbar()
plt.title('Temperature')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Plot wind speed
plt.contourf(lon, lat, wind_speed[0,:,:], cmap='coolwarm')
plt.colorbar()
plt.title('Wind Speed')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()