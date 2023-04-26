import os
import glob
import netCDF4
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
os.environ["PATH"]+=":/Library/TeX/texbin/"
print(os.environ["PATH"])
plt.rcParams.update({
    "text.usetex":True,
    "font.family":'Times New Roman'
})
size=16

fv=0.568

df_wspd = pd.read_csv('/Users/lmatak/Downloads/OneDrive_4_4-22-2023/2005/sws_28_08.csv')
df_rad=pd.read_csv('/Users/lmatak/Downloads/OneDrive_4_4-22-2023/2005/rads_28_8.csv')
# df_wspd.head()

# plot the desired columns from the merged dataframe
times_list=df_wspd['time']

merged_df = pd.merge(df_wspd, df_rad, on='time')

# plot the desired columns from the merged dataframe
# print(merged_df.head)
my_dict = {}
my_dict_vels={}

for i in range(int(max(merged_df['RDIST']))+1):
    my_dict[i] = []
    my_dict_vels[i]=[]
    print(i)

for i,j in zip(merged_df['RDIST'],merged_df['SWS']):
    # print(i,j)

    my_dict[int(i)].append(i)
    my_dict_vels[int(i)].append(j)
list_for_rads=[]
list_for_cs=[]
RosbyNum=[]
for key in my_dict.keys():
    RosbyNum.append(np.mean(my_dict_vels[key])/np.mean(my_dict[key])/fv)

    list_for_rads.append(np.mean(my_dict[key]))
    list_for_cs.append(np.mean(my_dict_vels[key]))
max_value = max(list_for_cs)
max_index = list_for_cs.index(max_value)
print(max_index)
# print((list_for_rads),(list_for_cs))
# plt.plot((list_for_rads),(list_for_cs))

plt.xticks(size=size-3)

plt.yticks(size=size-3)

# plt.plot( merged_df[merged_df['time'].isin(times_list)]['RDIST'],merged_df[merged_df['time'].isin(times_list)]['SWS'],)
plt.xlim(0,550)
# plt.hlines(10,0,600,color='red')
# plt.vlines(26,0,list_for_cs[26],color='cyan')
plt.ylabel(r'Rossby number',size=size)
plt.xlabel(r'Radial distance (km)',size=size)
plt.title('Hurricane Katrina',size=size)
# plt.figure()
plt.plot(list_for_rads[:],RosbyNum[:])
plt.xlim(-10,550)
plt.legend(['calculated from SFMR observed data'],fontsize=size)
# plt.vlines(26,0,RosbyNum[26],color='cyan')
# plt.show()
plt.savefig('/Users/lmatak/Downloads/ROSSBY_r.eps',dpi=350)