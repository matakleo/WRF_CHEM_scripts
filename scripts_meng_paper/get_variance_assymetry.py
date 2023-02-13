import numpy as np
from all_functions import Calculate_Distance_Haversine, hurricane_eye_3
from wrf import getvar,interplevel
from netCDF4 import Dataset
from collections import OrderedDict
import matplotlib.pyplot as plt
import statistics
file='/Users/lmatak/Downloads/wrfout_d01_2019_dorian'
file=Dataset(file)



u10=np.array(getvar (file, 'U10'))
v10=np.array(getvar (file, 'V10'))
total_wspd=np.sqrt(u10**2+v10**2)
line_of_wspds=[]
# slp=getvar(file,'SLP',0)
Lats = np.array(getvar (file, 'XLAT')[:,0])
Lons = np.array(getvar (file, 'XLONG')[0,:])

(Eye_Slp, Eye_Idx, Eye_Xlat, Eye_Xlon) = hurricane_eye_3(file, 0)
eye_lon_idx=Eye_Idx[1]
eye_lat_idx=Eye_Idx[0]

wspd_vals_list=[]



for i in range(len(Lons)):
        for j in range(len(Lats)):


                distance_from_eye=Calculate_Distance_Haversine(Lats[int(j)]\
                ,Lons[(int(i))],Eye_Xlat,Eye_Xlon)

                if (distance_from_eye >=50 or distance_from_eye<=400):
                    wspd_vals_list.append(total_wspd[int(j),int(i)])
                    
print(np.var(wspd_vals_list))
                          
