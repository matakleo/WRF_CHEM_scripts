
from audioop import avg
from netCDF4 import Dataset
from numpy.core.fromnumeric import shape, size, transpose
from wrf import getvar,interplevel,latlon_coords
import numpy as np
import math
import csv
import os
from all_functions import list_ncfiles, create_file


#check the output folder!!!!

# Input_Dir = '/project/momen/Lmatak/WRF_CHEM/PAPER_CASE/'
# Output_Dir = '/project/momen/Lmatak/WRF_CHEM/output_data/chem_contours/'
Output_Dir = '/Users/lmatak/Downloads/paper_case/outputs/'
Input_Dir = '/Users/lmatak/Downloads/paper_case/'

#what you wanna get:?
var="PM2_5_DRY"
#at what altitude?
alt=50

time_idxs=np.arange(0,23)
print(time_idxs)
os.chdir(Input_Dir)

########## list to hold the wrfout files ##########
ncfiles = []
ncfiles = list_ncfiles (Input_Dir, ncfiles)
avg_vals_atlanta=[]

print(ncfiles)

########## STARTS THE LOOP THROUGH THE OUTPUT FILES ##########              ####if changing Tiime_Idx var, make sure to exclued last ncfile!!!
for ncfile in ncfiles:
        list_of_vals=[]
        for time_idx in time_idxs:
                print(time_idx)


                try:
                        ########## load the data ##########
                        data = Dataset(ncfile)

                        height = getvar(data, "height_agl",time_idx)
                        get_contour_var = getvar(data, var,time_idx)
                        PM_vals=interplevel(get_contour_var,height,alt)
                        list_of_vals.append(PM_vals)
                except: 
                        print('there is no time_idx',time_idx,'in '+str(ncfile)+', moving on!')
                        continue
        list_of_vals=np.array(list_of_vals)

        avg_vals=list_of_vals.mean(axis=(0))
        avg_vals_atlanta.append(avg_vals[23][110])


####GET COORD DATA####
lats1, lons1 = latlon_coords(PM_vals)
lats=lats1[:,0]
lons=lons1[-1]





print(avg_vals.shape)

        ##############################
        # Exporting the simulated data #
        ##############################
print('##########################################################################################')
print('                                   FINISHED EXTRACTION!')
print('##########################################################################################')


########### create the output file      ###################
######################################
create_file (Output_Dir,var+'_daily')
Path = os.getcwd()
MyFile=open('%s.csv' %var,'w')
##write the var name, top left corner
MyFile.write (var + "_daily ,")

##write longitudes in first row
for val in avg_vals_atlanta:

##final longitude, swithc to lower row
        MyFile.write(str(val)+"\n")

                
# print(len(avg_vals[0]))
# row=0
# ##lats go row by row
# for latitude in lats[::-1]:

#         MyFile.write(str(float(latitude))+",")
#         for col in range(len(avg_vals[0])):
#                 #if final col of row, switch to next row!
#                 if col+1==len(avg_vals[0]):
#                         MyFile.write(str(avg_vals[row][col])+"\n")
#                         continue
#                 #otherwise just keep on writing
#                 MyFile.write(str(avg_vals[row][col])+",")

#         row+=1                

MyFile.close()
                                        
                               

