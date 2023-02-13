
import os
from all_functions import list_ncfiles , Calculate_Distance_Haversine, create_file,hurricane_eye_3
import numpy as np
from wrf import getvar
from netCDF4 import Dataset




#choose ['Lorenzo'] #,'Dorian','Iota','Lorenzo','Igor','Maria']
HNS = ['Katrina','Maria','Dorian','Igor','Lorenzo',]
# Choose between : '2km', '4km', '8km', '16km', '32km'
GSS = ['8km']
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TMS = ['NoTurb']
# Choose between : 'YSU', 'MYJ', 'ACM2'
PBLS = ['MYJ']
# Choose between : 'cLh0p2', 'cLh0p5', 'cLh1p0', 'cLh1p5'

CLS         = ['changeClz_0p0001','changeClz_0p0100','changeClz_100p0000','changeClz_1p0000']
# Set the input directory.
Input_Dir    = '/project/momen/Lmatak/WRF_COAWST/Hurricanes/cases_10_to_20/'
Output_Dir = '/project/momen/Lmatak/WRF_COAWST/outputs/'

# Choose between: '0', '1', '2', '3', '4', '5'
Time_idxs = [0]
#Choose a radius interval
QUAD_select=5
cv =  lambda x: np.std(x) / np.mean(x)

# Check the simulations to be working on.
variance_to_write=[]
for HN in HNS:
        variance_per_hur=[]
        for CL in CLS:
                variance_per_clz=[]
                Hurricane_Setting = 'WRFONLY_NoTurb_8km_isftcflx_1_' + CL
                Input_Dir_1 = Input_Dir + HN + '/8km/' + Hurricane_Setting
                ncfiles = []
                print(Input_Dir_1)
                ncfiles = list_ncfiles (Input_Dir_1, ncfiles)
                os.chdir(Input_Dir_1)
         
                for ncfile in ncfiles[0:1]:
                        wspd_vals_list=[]
                        
                        file=Dataset(ncfile)

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

                        for i in range(len(Lons)):
                                for j in range(len(Lats)):
                                        distance_from_eye=Calculate_Distance_Haversine(Lats[int(j)]\
                                        ,Lons[(int(i))],Eye_Xlat,Eye_Xlon)

                                        if (distance_from_eye >=50 or distance_from_eye<=400):
                                                wspd_vals_list.append(total_wspd[int(j),int(i)])
                        
                        variance_per_clz.append(cv(wspd_vals_list))
                        print('variance per clz = ',variance_per_clz)
                        
                variance_per_hur.append(np.mean(variance_per_clz))
                print(('variance per hur = ',variance_per_hur))
        variance_to_write.append(variance_per_hur)
print('var to write b4 averaging:',variance_to_write)
variance_to_write=np.mean(variance_to_write,0)
print('var to write after averaging:',variance_to_write)

# Exporting the data in a csv format.
create_file (Output_Dir, 'assymetry')
create_file (Output_Dir + 'assymetry/', 'assymetry_file')


MyFile=open("coeff_of_var_file.csv",'w')
MyFile.write ("Clz_0p0001, Clz_0p0100, Clz_100p0000, Clz_1p0000" + "\n")
for n in range (len(variance_to_write)):
        MyFile.write ((str(variance_to_write[n])) + ',' )



