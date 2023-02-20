
from audioop import avg
from netCDF4 import Dataset
from numpy.core.fromnumeric import shape, size, transpose
from wrf import getvar,interplevel,latlon_coords,ll_to_xy
import numpy as np
import math
import csv
import os

from xarray import Coordinate
from all_functions import list_ncfiles, create_file
import glob


def find_nearest(array, value):
    array = np.asarray(array)
    # print(np.abs(array - value))
    idx = (np.abs(array - value)).argmin()
    return idx


#check the output folder!!!!

Input_Dir = '/Users/lmatak/Downloads/wes-coldens/'

#what you wanna get:?
var="PM2_5_DRY"
#at what altitude?
alt=50


# ###FOR LES DOMAIN FOUR, BIG PME####
# CAMS1_pos=([250],[297])
# CAMS55_pos=([235],[283])
# CAMS35_pos=([205],[334])
# CAMS695_pos=([227],[249])
# CAMS416_pos=([213],[268])


## FOR SINGLE DOMAIN RUNS ##
CAMS1_pos=([49],[49])
CAMS55_pos=([49],[49])
CAMS35_pos=([49],[50])
CAMS695_pos=([49],[49])
CAMS416_pos=([49],[49])
downtown_pos=([49],[49])
cams53_pos= ([49],[49])
cams169_pos=([49],[49])
cams403_pos=([49],[49])




### this is for four domain run!
# CAMS1_pos=([120],[72])
# CAMS55_pos=([105],[58])
# CAMS35_pos=([75],[109])
# CAMS695_pos=([97],[24])
# CAMS416_pos=([83],[43])

# theser are for three domain run:

CAMS1_pos=([64],[73])
CAMS55_pos=([61],[70])
CAMS35_pos=([55],[80])
CAMS695_pos=([59],[63])
CAMS416_pos=([56],[67])
# downtown_pos=([63],[62])
cams53_pos= ([57],[51])
cams169_pos=([58],[70])
cams1052_pos=([68],[60])

# these are for two domain run

# CAMS1_pos=([67],[69])
# CAMS55_pos=([67],[69])
# CAMS35_pos=([66],[71])
# CAMS695_pos=([66],[67])
# CAMS416_pos=([66],[68])
# cams53_pos= ([66],[65])
# cams169_pos=([66],[69])
# cams403_pos=([67],[69])

CAMS_POSITIONS=[CAMS1_pos,CAMS55_pos,CAMS35_pos,CAMS695_pos,CAMS416_pos,cams53_pos,cams169_pos,cams1052_pos] 


time_idx=0
os.chdir(Input_Dir)
ncfiles = []
########## list to hold the wrfout files ##########
for file in glob.glob(Input_Dir+'wrfout_d03*'):
    ncfiles.append(file)



cams404_lat=29.807438
cams404_lon=-95.293630

cams1052_lat=29.814390
cams1052_lon=-95.387817

cams695_lat=29.7176
cams695_lon=-95.3414

cams53_lat=29.695747
cams53_lon=-95.499222

cams409_lat=29.623961
cams409_lon=-95.474341

cams8_lat=29.901036
cams8_lon=-95.326137

cams416_lat=29.686389
cams416_lon=-95.294722

cams1_lat=29.767996
cams1_lon=-95.220582


cams603_lat=29.764788
cams603_lon=-95.178538

cams403_lat=29.733741
cams403_lon=-95.257605

cams167_lat=29.734281
cams167_lon=-95.238417

cams1029_lat=29.719358
cams1029_lon=-95.259497

cams169_lat=29.706111
cams169_lon=-95.261111

cams670_lat=29.701944
cams670_lon=-95.257222

cams1020_lat=29.684360
cams1020_lon=-95.253598

cams1049_lat=29.703208
cams1049_lon=-95.221947

cams=3
cams_names=['cams1','cams55','cams35','cams695','cams416','cams53','cams169','cams1052'] #
cams_lats=[cams404_lat,cams1052_lat,cams695_lat,cams53_lat,cams409_lat,cams8_lat,cams416_lat,cams1_lat,\
    cams603_lat,cams403_lat,cams167_lat,cams1029_lat,cams169_lat,cams670_lat,cams1020_lat,cams1049_lat]
cams_longs=[cams404_lon,cams1052_lon,cams695_lon,cams53_lon,cams409_lon,cams8_lon,cams416_lon,cams1_lon,\
    cams603_lon,cams403_lon,cams167_lon,cams1029_lon,cams169_lon,cams670_lon,cams1020_lon,cams1049_lon]#



mid_downtown_lon=-95.3621823
mid_downtown_lat=29.7585786











for ncfile in ncfiles:
    print('ncfile = '+ncfile)

    ########## load the data ##########
    data = Dataset(ncfile)
    height = getvar(data, "height_agl",time_idx)
    T2=getvar(data,'T2',0)


    ## HERE YOU FIND THE POSITIONS OF THE CAMS MEASURE POSITION
    ## READ THE NUMBER FROM THE PRINT STATEMENTS, THEY ARE POSITIONS IN DOMAIN!
    ## UPDATE ON CARYA FOR EXTRACTION!!
    ## number at T2.XLONG[X] doesn't even matter..
    ## just enter here which camsx_long and camsx_lat you're looking for, and it will spit out 
    ## inteeger positions
    ## The positioning is right, so left column is left column and right column is right column!
    for cams in range(len(cams_lats)):
        print(cams_names[cams]+' lat=',int(find_nearest(T2.XLAT,cams_lats[cams])/len(T2.XLAT)), cams_names[cams]+' lon=',find_nearest(T2.XLONG[10],cams_longs[cams])) 

        print(cams_names[cams],np.array(ll_to_xy(data,cams_lats[cams],cams_longs[cams]))[1],np.array(ll_to_xy(data,cams_lats[cams],cams_longs[cams]))[0])
    # print(cams_names[cams]+' lon=',find_nearest(T2.XLONG[10],cams_longs[cams]))
    
    #THIS print statement is optional, if you wanna comapre with excel positions
i=0
for cams_pos in CAMS_POSITIONS:
    # print(cams_pos)
    print(float(T2[cams_pos].XLONG)-cams_longs[i],float(T2[cams_pos].XLAT-cams_lats[i]))
    # print(float(T2[cams_pos].XLONG),',',float(T2[cams_pos].XLAT))
    i+=1

    # three_dom_lats=[29.587852478027344,29.425567626953125,29.100189208984375,29.31720733642578,29.15448760986328]
    # three_dom_lons=[-94.98545837402344,-95.17194366455078,-94.55033874511719,-95.60706329345703,-95.3584213256836]
   

