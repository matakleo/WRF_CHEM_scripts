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
size=18

df_wspd = pd.read_csv('/Users/lmatak/Downloads/OneDrive_4_4-22-2023/2005/wspd.csv')
df_rad=pd.read_csv('/Users/lmatak/Downloads/OneDrive_4_4-22-2023/2005/rad_29_8.csv')
# df_wspd.head()

# print( df_wspd.head())
# print(df_wspd['time'])
# time_list_idx=df_wspd['time']
# print(len(time_list_idx))
# indices_to_keep=time_list_idx

# df_wspd.set_index('time', inplace=True)
# df_rad=df_rad.loc[df_rad.index.isin(indices_to_keep)]
# df_rad.reset_index(inplace=True)
# print(df_rad.head())
# print(len(df_rad['RDIST']),len(df_wspd['SWS']))
# # plt.plot(df_rad,df_wspd)

# merge the dataframes on the common column "time"


# plot the desired columns from the merged dataframe
times_list=df_wspd['time']

merged_df = pd.merge(df_wspd, df_rad, on='time')

# plot the desired columns from the merged dataframe
# print(merged_df.head)
my_dict = {}
my_dict_vels={}

for i in merged_df['RDIST']:
    my_dict[i] = []
    my_dict_vels[i]=[]

for i,j in zip(merged_df['RDIST'],merged_df['SWS']):
    # print(i,j)

    my_dict[(i)].append(i)
    my_dict_vels[(i)].append(j)
list_for_rads=[]
list_for_cs=[]
for key in my_dict.keys():
    print(my_dict[key][0])
    list_for_rads.append(my_dict[key][0])
    list_for_cs.append(my_dict_vels[key][0])
# print((list_for_rads),(list_for_cs))
plt.plot((list_for_rads),(list_for_cs))

plt.xticks(size=size-3)

plt.yticks(size=size-3)
# plt.plot( merged_df[merged_df['time'].isin(times_list)]['RDIST'],merged_df[merged_df['time'].isin(times_list)]['SWS'],)
plt.xlim(0,600)
plt.hlines(10,0,600,color='red')
plt.ylabel(r'Wind Speed $\mathrm{(m\,s^{-1}) \,}$',size=size)
plt.xlabel(r'Radial distance (km)',size=size)
plt.title('SFMR Data',size=size)
plt.show()
# plt.savefig('/Users/lmatak/Downloads/OneDrive_4_4-22-2023/2005/wspd_r.eps',dpi=350)