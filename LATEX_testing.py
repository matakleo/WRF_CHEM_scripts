
from all_functions import Extract_by_name,Extract_Track_Data,list_csv_files_0, calculate_distance_error,calculate_intensity_error,calculate_intensity_error_slp
import matplotlib.gridspec as gridspec
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from error_function_bars import gimme_errors


os.environ["PATH"]+=":/Library/TeX/texbin/"
print(os.environ["PATH"])
plt.rcParams.update({
    "text.usetex":True,
    "font.family":'Times New Roman'
})
t=np.linspace(0.0,1.0,100)
s=np.cos(4*np.pi*t)+2

fig,ax=plt.subplots(figsize=(6,4), tight_layout=True)
ax.plot(t,s)

# ax.set_xlabel(r'$K_{ m }\_lvl_{ 4 }m^{2}$YSU (\,\%) \,bla',fontsize=16)
ax.set_xlabel(r'$K_{ m }\_lvl_{ 4 }YSU \mathrm{(\,m^{2}s^{-1}) \,}bla$',fontsize=16)
plt.show()