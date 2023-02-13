from numpy.core.function_base import linspace
from all_functions import Extract_by_name,Extract_Coordinates_2,Extract_Track_Data
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
#from Func_Map_Setting import map_setting
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig, ax = plt.subplots(constrained_layout=True)
Times = [0,0,6, 12, 18, 24, 30, 36, 42, 48]

csv_file1='/Users/lmatak/Downloads/leo/maria_8km_Clz_0p01.csv'
csv_file2='/Users/lmatak/Downloads/leo/maria_8km_Clz_0p0001.csv'

Wind_Speed = []
# Wind_Speed_simulation = flatten_the_curve(Extract_by_name (csv_file, Wind_Speed, 'All_Max_WND_SPD_10'))
Wind_Speed_simulation = Extract_by_name (csv_file1, Wind_Speed, 'All_Max_WND_SPD_10')
print(Wind_Speed_simulation)
ax.plot(Wind_Speed_simulation,label='Clz_0p01',color='cyan')
ax.set_xticklabels(Times)
Wind_Speed_simulation2=[]
Wind_Speed_simulation2 = Extract_by_name (csv_file2, Wind_Speed_simulation2, 'All_Max_WND_SPD_10')
print(Wind_Speed_simulation)
ax.plot(Wind_Speed_simulation2,label='Clz_0p0001',color='blue')
plt.legend()
plt.show()
# ax12.plot(Times[0:len(Eye_Lats)], Wind_Speed_simulation[0:len(Eye_Lats)], color = colors[c] , linestyle=line_stylez[PBL_counter],
# linewidth='2', marker='.', markersize='10',label=(PBL+' hpbl - '+CLS[cls_counter]))
# ax12.set_xlabel('Times')
# ax12.set_title('Wind intensity [m/s]')
