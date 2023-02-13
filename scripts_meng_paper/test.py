import math
import numpy as np
import matplotlib.pyplot as plt
xkzm=100

u=np.arange(0,50,0.1)
v=u

wspd=[]
upper_limit=20
lower_limit=10
c_lz=10
znt_to_plot=[]
znt=0.03
zntc=znt
print(1/(upper_limit-lower_limit))
##10 to 15
for i in range(len(u)):
    
    








    
    if (math.sqrt(u[i]**2+v[i]**2)) > upper_limit or (math.sqrt(u[i]**2+v[i]**2)) < lower_limit:
        znt_to_plot.append(zntc)
        wspd.append(math.sqrt(u[i]**2+v[i]**2))
        # print('vel is:',math.sqrt(u[i]**2+v[i]**2),'znt is ',zntc)
        continue
    else:
            print('here?')
            if c_lz<1:

                # zntc=max(((1+(1/(upper_limit-lower_limit))*(c_lz-1)*(math.sqrt(u[i]**2+v[i]**2)-lower_limit))*znt),c_lz*zntc)

                zntc=((1+(1/(upper_limit-lower_limit))*(c_lz-1)*(math.sqrt(u[i]**2+v[i]**2)-lower_limit))*znt)

            else:
                zntc=min(((1+(1/(upper_limit-lower_limit))*(c_lz-1)*(math.sqrt(u[i]**2+v[i]**2)-lower_limit))*znt),c_lz*zntc)
            print('vel is:',math.sqrt(u[i]**2+v[i]**2),'znt is ',zntc)
            znt_to_plot.append(zntc)
            wspd.append(math.sqrt(u[i]**2+v[i]**2))
plt.scatter(wspd,znt_to_plot)
plt.xlabel('wspd')
plt.ylabel('Z0')
plt.show()

# zntc=max(((1+(0.1*c_lz-0.1)*(wsp10-lower_limit))*znt),c_lz*zntc)

# cl=['changeClz_0p0001','changeClz_0p0100','changeClz_100p0000','changeClz_1p0000']
# plt.bar(cl,[21.5518762,	20.1469185,	10.7462473,	16.8238346])

# plt.show()




# for i in range(len(u)):
#     znt=0.03
#     if (math.sqrt(u[i]**2+v[i]**2) > 15.0):
#         # if c_lz<1:
#         znt=c_lz*znt
#     elif (math.sqrt(u[i]**2+v[i]**2) < 10.0):
#         znt=znt
#     else:

#         #     znt=max(((1+0.1*(c_lz-1)*(math.sqrt(u[i]**2+v[i]**2)-5.0))*znt),c_lz*znt)
#         # else:
#         #     znt=min(((1+0.1*(c_lz-1)*(math.sqrt(u[i]**2+v[i]**2)-5))*znt),c_lz*znt)
#     znt_to_plot.append(znt)
#     wspd.append(math.sqrt(u[i]**2+v[i]**2))
# plt.plot(wspd,znt_to_plot)
# plt.xlabel('wspd')
# plt.ylabel('Z0')

# plt.show()





# for i in range(len(u)):
#     znt=0.03
#     if (math.sqrt(u[i]**2+v[i]**2) > 10.0):
#         if c_lz<1:

#             znt=max(((1+0.1*(c_lz-1)*(math.sqrt(u[i]**2+v[i]**2)-5.0))*znt),c_lz*znt)
#         else:
#             znt=min(((1+0.1*(c_lz-1)*(math.sqrt(u[i]**2+v[i]**2)-5))*znt),c_lz*znt)
#     znt_to_plot.append(znt)
#     wspd.append(math.sqrt(u[i]**2+v[i]**2))
# plt.plot(wspd,znt_to_plot)
# plt.xlabel('wspd')
# plt.ylabel('Z0')

# plt.show()

