import netCDF4
import os
import glob
for file in glob.glob(os.getcwd()+'/wrfchemi*'):
    print (file)
           
    ncfile = netCDF4.Dataset(file, mode='r+')
    var = ncfile.variables['E_PM_10'][:]
    var[var < 0] = 0
    ncfile.variables['E_PM_10'][:] = var
    ncfile.close()

