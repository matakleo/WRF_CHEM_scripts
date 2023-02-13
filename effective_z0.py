from cmath import log
import matplotlib.pyplot as plt
import numpy as np
from all_functions import Extract_by_name, Extract_the_shit2
import glob
import os
from sklearn.linear_model import LinearRegression
all_ust=[]
all_z0=[]
number_of_pts=6
file_num=0
colors=['blue','orange','green']
months=['Mar'] #,'Feb','Mar','Apr','May','Jun',]
labels=['BEM_default','BEM_decrease','BEM_increase']
# labels=['SLUCM_def','SLUCM_ust0.1','SLUCM_ust10']

def mengs_approach(wind_speed_list,heights_list):
    x=wind_speed_list
    y=heights_list
    

    lin_reg_model=LinearRegression().fit(np.array(x).reshape(-1, 1), \
                                            np.log(y))
    roughness=((np.exp(lin_reg_model.predict(np.array([0]).reshape(-1,1)))[0]))
    wspd10=((np.log(10)-lin_reg_model.intercept_)/lin_reg_model.coef_)
    meng_ustr=(wspd10*0.41/np.log(10/roughness))
        #for plotting#
    line=np.linspace(-1,15,10,endpoint=False).reshape(-1, 1)
    fitted_ys=np.exp(lin_reg_model.predict(line.reshape(-1, 1)))
    return roughness,meng_ustr

def leos_approach(wind_speed_list,heights_list):
    x=wind_speed_list
    y=heights_list
    p = np.polyfit(x, np.log(y), 1)
    a = np.exp(p[1])
    b = p[0]
    ustar=0.4/b
    z0=a
         #for plotting#
    line=np.linspace(-1,15,10,endpoint=False).reshape(-1, 1)
    y_fitted = a * np.exp(b * line)

    return z0,ustar

for month in months:
    files=[]
    winds_list=[]
    height_list=[]
    
    dir='/Users/lmatak/Downloads/URBAN_SCHEMES_VERT_PROFILES/modifications/'+month+'/'
    # dir='/Users/lmatak/Downloads/URBAN_SCHEMES_VERT_PROFILES/SLUCM/'+month+'/'
    # dir='/Users/lmatak/Downloads/URBAN_SCHEMES_VERT_PROFILES/no_modification/'+month+'/'
    for file in glob.glob(dir+'*.csv'):
        files.append(file)
    # print(files)
    ustar_lst=[]
    z0_lst=[]
     #,'BEP','NO_URBAN',] #,'building_heights2','clz_0.0001','clz_0.000001'] #,'BouLac']
    # labels=['z0r_decrease','clz_0.000001','default','increased_building',]
    i=0
    for file in files[file_num:file_num+1]:
    # for file in files:
        # if i!=1:continue
        print(file)
        height_list=[]
        winds_list=[]

        height_list=np.array(Extract_by_name(file,height_list,'height'))
        winds_list=np.array(Extract_by_name(file,winds_list,'WSPD'))

        y = height_list[0:number_of_pts]
        x = winds_list[0:number_of_pts]

        z_0_meng,ust_meng=mengs_approach(x,y)
        z_0_leo,ust_leo=leos_approach(x,y)



        
#         plt.yscale("log")
#         plt.scatter(x,y,color=colors[i])

        print('%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('              Leo             ')
        print('ustar =',ust_leo,'z0=',z_0_leo)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('              Meng             ')
        print('ustar=',ust_meng,'z0=',z_0_meng)


#         ustar_lst.append(ustar)
#         z0_lst.append(z0)

#         i+=1
#     all_ust.append(ustar_lst)
#     all_z0.append(z0_lst)
# all_ust=np.array(all_ust)    
# all_z0=np.array(all_z0)
# print(all_ust)
# print(np.mean(all_ust,0))
# print(np.mean(all_z0,0))     
# x=[1,2,3]
# x=['decreased','default','increased']
# # plt.bar(x,np.mean(all_z0,0))
# # print(all_z0)
# # plt.legend(labels)
# # print(height_list[6])
# # print(np.log(height_list))
# plt.grid(visible=True, which='major', axis='y')
# # plt.yticks(height_list[:6])

# plt.ylabel('z (m)')
# plt.xlabel('wspd (m/s')
# plt.title(labels[file_num]+' '+month+' ---  '+'u*='+"%.2f" %ustar +' z0='+"%.5f" %z0)
# plt.show()

# os.chdir(dir)

