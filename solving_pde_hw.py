import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def tridiag(a, b, c, N):
    ''''''
    #  Returns a tridiagonal matrix A=tridiag(v, d, w) of dimension N x N.
    ''''''

    e = np.ones(N) # array [1,1,...,1] of length N
    # # print(a*np.diag(e[1:],-2))
    # # print(b*np.diag(e,-1))
    # # print(c*np.diag(e))
    # print(a*np.diag(e[1:],-2)+b*np.diag(e[1:],-1)+c*np.diag(e[1:]))

    # A[0,0]=1
    # A=a*np.diag(e[1:],-2)+b*np.diag(e,-1)+c*np.diag(e)
    # print(A)
    
    A = a*np.diag(e[1:],-1)+b*np.diag(e)+c*np.diag(e[1:],1)
    return A

def f(x):
    #should represent the forcing term, for simplicity I justs leave it as f(x,t)=x
    return 10*x
def IC():
    #to make the IC chaneable, however best left at 0!
    return 0
def Uleft():
    #the boundary condition at left side, I set it to arbitrary 2
    return 1


##SPATIAL DOMAIN##
##################
L=1   #length of domain
n=100  #number of points
v=0.0001    #advectin
D=10**(-6)   #diffusion
k=-1.67*10**(-5)   #reaction
alpha=0.5   #alpha in space discretization
dx=L/(n-1)  #dx
x=np.linspace(0,L,n)  #grid_points in space [x1,x2,x3,xi..xN]
# print(dx)

# F=f(x)    #forcing term 2*f(x)
F=np.zeros(n)



## TIME PARAMETERS ##
####################
theta=0.5     #time varyin parameter
tend =2*3600     #the length of time simulation, takes I think more than 8h to beome steady state
N = 1*3600 # Number of intervals in the t-direction, should be more than 1s to be stable
Dt = tend/N #Dt
t = np.linspace(0,tend,N+1) # Gridpoints in the t-direction, N+1 due to initial condition

##tri-diagonal matrix entries##
a=-D/dx**2-v*(1-alpha)/2/dx  # parameter a
b=k-v*alpha/dx+2*D/dx**2    #paramater b
c=v*alpha/dx + (1-alpha)*v/2/dx - D/dx**2   #parameter c

##make the tridiagonal matrix##
A=(tridiag(a,b,c,n))

#update the tridiagonal A matrix in final row:
A[-1,-3]=0
A[-1,-2]=a+c
A[-1,-1]=b
print(np.around(A,decimals=1))
#make the ones matrix
EYE=np.eye(n+1,N+1)
#update the forcing term for second equation -- BC
F[0]=F[0]-a*Uleft()
print(np.around(F,decimals=1))



Uone=np.linalg.inv(A).dot(F)
# print('solution matrix U',Uone)
# for i in range(len(Uone)):
#     Uone[i]=Uone[i]/Uleft()
# plt.plot(x,Uone)
# plt.show()

# Array to store the solution
U = np.zeros((n+1,N+1))
U[:,0] = IC() # Initial condition U_{i,0} = f(x_i)
U[0, 1:] = Uleft()
# U[:,1]=Uone

##K to be used for time marching Ku^n+1=b
K=np.eye(n)+theta*A*Dt





for time_step in range(N-1):
    # print('time_step is ',time_step)
    if time_step==0:
        Utmp=U[1:,1]=Uone
    # else:
    Utmp=np.linalg.inv(K).dot(Utmp-(1-theta)*Dt*A.dot(Utmp)+F)
    # print(Utmp)
    U[1:,time_step+2]=Utmp
    if time_step%500==0:
        
        # print('PLOTTING')
        plt.plot(x,Utmp,label='time = '+str(time_step)+'s')
        # print('b')
    # Utmp[0]=2

# plt.plot(U[:,-1])
plt.legend()
plt.show()
# plt.ylim(0, 2.5)
# plt.plot(x,U[:-1,-1])
# plt.show()


# print(np.around(U,decimals=1))





