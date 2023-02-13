import matplotlib.pyplot as plt
import numpy as np
from all_functions import Extract_by_name, Extract_the_shit2
import glob
import os
files=[]
winds_list=[]
height_list=[]
number_of_pts=11
month='Mar'
dir='/Users/lmatak/Downloads/URBAN_SCHEMES_VERT_PROFILES/modifications/'+month+'/'
# dir='/Users/lmatak/Downloads/URBAN_SCHEMES_VERT_PROFILES/no_modification/'+month+'/'
# dir='/Users/lmatak/Downloads/URBAN_SCHEMES_VERT_PROFILES/SLUCM/'+month+'/'
for file in glob.glob(dir+'*.csv'):
    files.append(file)
print(files)
# labels=['BEM_def','BEM_decrease','BEM_increase',]
labels=['BEM_DEFAULT','cd_low','cd_high'] 
# labels=['z0r_decrease','building_decrease','default','ustar_0.01','z0r_increase',]
i=0
for file in files:
    print(file)
    height_list=[]
    winds_list=[]
    height_list=Extract_by_name(file,height_list,'height')
    
    winds_list=Extract_by_name(file,winds_list,'WSPD')
    plt.yscale('log')
    # print(winds_list)
    # if i!=0:
    #     plt.semilogy(winds_list[0:6],(height_list[0:6]),linewidth=1.4,marker='x')
    # else:plt.semilogy(winds_list[0:8],(height_list[0:8]),linewidth=2, color='black',zorder=-1)
    plt.plot(winds_list[0:number_of_pts],(height_list[0:number_of_pts]),linewidth=1.4,marker='x')
    i+=1
plt.legend(labels)
# print(height_list[6])
# print(np.log(height_list))
plt.grid(visible=True, which='major', axis='y')
# plt.yticks(height_list[:6])
plt.xlabel('wspd m/s')
plt.ylabel('height m')
plt.title(month)
plt.show()

os.chdir(dir)



for i in range(62,63): print(i)