
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)
from all_functions import Extract_Track_Data,list_ncfiles,Extract_the_shit2
import matplotlib as mpl
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from netCDF4 import Dataset
import cartopy.crs as crs
import numpy as np

import copy

from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import cartopy.feature as cfeature



os.environ["PATH"]+=":/Library/TeX/texbin/"
print(os.environ["PATH"])
plt.rcParams.update({
    "text.usetex":True,
    "font.family":'Times New Roman'
})



def vertical_exch_profile(wspd_min,wspd_max):
    Input_Dir = '/Users/lmatak/Desktop/some_wrfout_files/five_to_ten_layer/Dorian_8km_NoTurb_MYJ_hpbl_lvl_3/'
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)

    wspd=[]
    idx=0

    Data = Dataset(ncfiles[0])

    LAI=np.array(getvar(Data, "LANDMASK", timeidx = idx))

    wspd=np.array(getvar(Data, "wspd", timeidx = idx))
    height=np.array(getvar(Data, "height", timeidx = idx))

    wspd_surface=wspd[0,:,:]
    wspd_surface_1d=wspd_surface.flatten()
    print(LAI.flatten().shape)

    vert_exch=[]
    altitude=[]

    xkzm=np.array(getvar(Data, "AKMKL", timeidx = idx))

    U10_2D = np.array(getvar(Data, "U10", idx))
    V10_2D = np.array(getvar(Data, "V10", idx))
    U10_1D = U10_2D.flatten()
    V10_1D = V10_2D.flatten()
    WND_SPD_10 = U10_1D
    LAI1D=LAI.flatten()
    print('LAI avg',np.mean(LAI1D))
    # Calculate the wind intensity at each point of the map.
    for i in range (WND_SPD_10.size - 1):
            WND_SPD_10[i] = np.sqrt((U10_1D[i]**2)+(V10_1D[i]**2))
    top_100_idx = np.argsort(WND_SPD_10)[-100:]        
    wspd_u10_v10=np.sqrt(U10_2D**2+V10_2D**2)
    wspd_u10_v10=wspd_u10_v10.flatten()

    LANDMASK=np.array(getvar(Data, "LANDMASK", timeidx = idx))
    LANDMASK1D=LANDMASK.flatten()


    for i in range(0,11):
        xkzm2d=xkzm[i,:,:]
        xkzm1d=xkzm2d.flatten()
        height2d=height[i,:,:]
        height1d=height2d.flatten()
        altitude.append(np.average(height1d))
        vert_exch.append(np.average(xkzm1d[(LANDMASK1D==0) & (wspd_u10_v10>=wspd_min) & (wspd_u10_v10<=wspd_max)]))
        # vert_exch.append(np.average(xkzm1d[LAI1D==0 ]))

        # altitude.append(np.average(height1d[top_100_idx]))
        # vert_exch.append(np.average(xkzm1d[top_100_idx]))
    # print('for wmin',wspd_min,' and wmax',wspd_max)
    # print(wspd_surface_1d<3)
    # print('THIS IS LVL 3:',altitude)
    # print(vert_exch)

    return vert_exch


def vertical_exch_profile_default(wspd_min,wspd_max):
    Input_Dir = '/Users/lmatak/Desktop/some_wrfout_files/five_to_ten_layer/Dorian_8km_NoTurb_MYJ_hpbl_1.0/'
    os.chdir(Input_Dir)
    ncfiles=[]
    ncfiles = list_ncfiles(Input_Dir, ncfiles)

    wspd=[]
    idx=0

    Data = Dataset(ncfiles[0])

    LAI=np.array(getvar(Data, "LANDMASK", timeidx = idx))

    wspd=np.array(getvar(Data, "wspd", timeidx = idx))
    height=np.array(getvar(Data, "height", timeidx = idx))

    wspd_surface=wspd[0,:,:]
    wspd_surface_1d=wspd_surface.flatten()
    print(LAI.flatten().shape)
    LAI1D=LAI.flatten()

    LANDMASK=np.array(getvar(Data, "LANDMASK", timeidx = idx))
    LANDMASK1D=LANDMASK.flatten()
    vert_exch=[]
    altitude=[]

    xkzm=np.array(getvar(Data, "AKMKL", timeidx = idx))

    U10_2D = np.array(getvar(Data, "U10", idx))
    V10_2D = np.array(getvar(Data, "V10", idx))
    U10_1D = U10_2D.flatten()
    V10_1D = V10_2D.flatten()
    WND_SPD_10 = U10_1D
    # Calculate the wind intensity at each point of the map.
    for i in range (WND_SPD_10.size - 1):
            WND_SPD_10[i] = np.sqrt((U10_1D[i]**2)+(V10_1D[i]**2))
    top_100_idx = np.argsort(WND_SPD_10)[-100:]        

    wspd_u10_v10=np.sqrt(U10_2D**2+V10_2D**2)
    wspd_u10_v10=wspd_u10_v10.flatten()

    for i in range(0,11):
        xkzm2d=xkzm[i,:,:]
        xkzm1d=xkzm2d.flatten()
        height2d=height[i,:,:]
        height1d=height2d.flatten()
        altitude.append(np.average(height1d))
        # vert_exch.append(np.average(xkzm1d[LAI1D==0]))
        vert_exch.append(np.average(xkzm1d[(LANDMASK1D==0) & (wspd_u10_v10>=wspd_min) & (wspd_u10_v10<=wspd_max)]))

        # altitude.append(np.average(height1d[top_100_idx]))
        # vert_exch.append(np.average(xkzm1d[top_100_idx]))
    # print('THIS IS DEFAULT:',altitude)
    # print(vert_exch)

    return vert_exch    
eleven=np.arange(0,11,1)
print(vertical_exch_profile(10,11))
default_case=vertical_exch_profile_default(3,4)
three_to_five_vert_exch=vertical_exch_profile(3,4)
seven_to_eight_vert_exch=vertical_exch_profile(7,8)
nine_to_ten_vert_exch=vertical_exch_profile(10,15)
five_to_six_vert_exch=vertical_exch_profile(5,6)
eight_to_nine_vert_exch=vertical_exch_profile(8,9)

plt.plot(default_case,eleven,marker='x',label='default')
plt.plot(three_to_five_vert_exch,eleven,marker='o',label='3 - 4')
plt.plot(five_to_six_vert_exch,eleven,marker='o',label='5 - 6')
plt.plot(seven_to_eight_vert_exch,eleven,marker='o',label='7 - 8')
plt.plot(eight_to_nine_vert_exch,eleven,marker='o',label='8 - 9')
plt.plot(nine_to_ten_vert_exch,eleven,marker='x',label='9 - 10')
plt.legend()
plt.show()


# plt.show()
    # print(xkzm2d)


#     u10=getvar(Data, "U10", timeidx = idx)
#     v10=getvar(Data, "V10", timeidx = idx)
#     total_wind=np.sqrt(u10**2+v10**2)

#     height = (getvar(Data, "height_agl",timeidx = idx))
#     print(np.mean(height[2,:,:]))
#     # wspd[(LAI>0) | (lakemask>0)]=0
#     total_wind=np.array(total_wind)
#     # xkzm[(total_wind<5)]=nan
#     # total_wind[(total_wind<10)]=nan
  
#     lats1, lons1 = latlon_coords(height[0])

#     move_conts_to_right_longs=5
#     lats_move=7
#     # ax[row,i].set_extent([float(lons1[0][0])+14, \
#     #     float(lons1[-1][-1])-move_conts_to_right_longs, \
#     #         float(lats1[0][0])+lats_move,float(lats1[-1][-1])-lats_move])
#     # ax[row,i+1].set_extent([float(lons1[0][0])+14,\
#     #     float(lons1[-1][-1])-move_conts_to_right_longs,\
#     #         float(lats1[0][0])+lats_move,float(lats1[-1][-1])-lats_move])

#     plot_max=50
#     plot_min=0

#     ##FOR LINEAR###
#     contor=ax[row,i].contourf(to_np(lons1),to_np(lats1), \
#                  xkzm2d,25,vmin=plot_min,vmax=plot_max,cmap=my_cmap1,
#                  transform=crs.PlateCarree(),
                  
#         )
    
#     ax[row,i+1].contourf(to_np(lons1),to_np(lats1), (total_wind), 25,  vmin=wspd_min,vmax=wspd_max,     transform=crs.PlateCarree(), 
#         cmap=my_cmap2,)
#     ax[row,i+1].background_patch.set_facecolor('black')    
#     ax[row,i].background_patch.set_facecolor('black')  

    
    
#     row+=1


# norm1 = mpl.colors.Normalize(vmin=plot_min, vmax=plot_max)
# cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1), \
#      ax=ax[0,0],orientation='vertical',extend='max', fraction=0.1
# )
# cbar1.set_label(label=r'EDDY COEFF',size=15,)
# # cbar1=fig.colorbar(mpl.cm.ScalarMappable(norm=norm1, cmap=my_cmap1), \
# #      ax=ax[1,0],orientation='vertical',extend='max', fraction=0.1
# # )
# # cbar1.set_label(label=r'$Z_{ 0 }$',size=15,)

# norm2 = mpl.colors.Normalize(vmin=wspd_min, vmax=wspd_max)
# # print(norm_log)

# cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=my_cmap2),
# ax=ax[0,1], orientation='vertical',  extend='max', fraction=0.1,

# )
# cbar2.ax.tick_params(labelsize=15)
# # r'$\mathrm{(\,ms^{-1}) \,}$'
# cbar2.set_label(label=r"Surface wind speed $\mathrm{(\,ms^{-1}) \,}$",size=15)
# cbar2=fig.colorbar(mpl.cm.ScalarMappable(norm=norm2, cmap=my_cmap2),
# ax=ax[1,1], orientation='vertical',  extend='max', fraction=0.1,
# label="Wind intensity m/s")
# cbar2.ax.tick_params(labelsize=15)
# cbar2.set_label(label=r"Surface wind speed $\mathrm{(\,ms^{-1}) \,}$",size=15)
# # fig.colorbar(Zo)

# bbox_args = dict(boxstyle="round4", fc="0.9")



# ax[0,0].annotate('a)', xy=(0.1, 0.95), xycoords='axes fraction',
#              xytext=(0, -10), textcoords='offset points',
#              ha="right", va="top",size=28,
#              color='white'
#              )
# ax[0,1].annotate('b)', xy=(0.1, 0.95), xycoords='axes fraction',
#              xytext=(0, -10), textcoords='offset points',
#              ha="right", va="top",size=28,
#              color='white'
#              )
# ax[1,0].annotate('c)', xy=(0.1, 0.95), xycoords='axes fraction',
#              xytext=(0, -10), textcoords='offset points',
#              ha="right", va="top",size=28,
#              color='white'
#              )
# ax[1,1].annotate('d)', xy=(0.1, 0.95), xycoords='axes fraction',
#              xytext=(0, -10), textcoords='offset points',
#              ha="right", va="top",size=28,
#              color='white'
#              )



# ax[0,0].set_title(r'Default case', size=20)
# ax[0,1].set_title(r'Default case', size=20)
# ax[1,0].set_title(r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.01', size=20)
# ax[1,1].set_title(r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.01', size=20)
# fig.tight_layout()

# # h,l=ax[0].get_legend_handles_labels()
# # ax[0].legend(h,l)
# # plt.savefig('/Users/lmatak/Desktop/CLZ_katrina.png',bbox_inches='tight')

# plt.show()