
from audioop import avg
from netCDF4 import Dataset
from numpy.core.fromnumeric import shape, size, transpose
from wrf import getvar,interplevel,latlon_coords
import numpy as np
import math
import csv
import os
from all_functions import list_ncfiles, create_file
import glob


#check the output folder!!!!

# Input_Dir = '/project/momen/Lmatak/WRF_CHEM/PAPER_CASE/'
# Output_Dir = '/project/momen/Lmatak/WRF_CHEM/output_data/chem_contours/'
Output_Dir = '/project/momen/Lmatak/WRF_CHEM/output_files/'
Input_Dir = '/project/momen/Lmatak/WRF_CHEM/PAPER_CASE/wrf_run/'

#what you wanna get:?
var="PM2_5_DRY"
#at what altitude?
alt=50

time_idx=0
os.chdir(Input_Dir)
ncfiles = []
########## list to hold the wrfout files ##########
for file in glob.glob(Input_Dir+'wrfout_d02*'):
    ncfiles.append(file)


print(ncfiles)
list_of_vals=[]
########## STARTS THE LOOP THROUGH THE OUTPUT FILES ##########              ####if changing Tiime_Idx var, make sure to exclued last ncfile!!!
for ncfile in ncfiles:
        



        try:
                ########## load the data ##########
                data = Dataset(ncfile)

                height = getvar(data, "height_agl",time_idx)
                get_contour_var = getvar(data, var,time_idx)
                PM_vals=interplevel(get_contour_var,height,alt)
                list_of_vals.append(PM_vals)
        except: 
                print('something went wrong with '+str(ncfile)+', moving on!')
                continue




        ##############################
        # Exporting the simulated data #
        ##############################
print('##########################################################################################')
print('                                   FINISHED EXTRACTION!')
print('##########################################################################################')


########### create the output file      ###################
######################################
create_file (Output_Dir,var+'_hourly')
Path = os.getcwd()
MyFile=open('%s.csv' %var,'w')
##write the var name, top left corner
MyFile.write (var + "_hourly ,")

##write longitudes in first row
for val in list_of_vals:

##final longitude, swithc to lower row
        MyFile.write(str(val)+",")

                
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
                                        
                               

